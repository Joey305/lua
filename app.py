import os
from datetime import datetime

from dotenv import load_dotenv
import requests
from flask import Flask, render_template, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("Nombre y apellidos", validators=[DataRequired(message="Indica tu nombre."), Length(max=100)])
    email = EmailField("Correo electrónico", validators=[DataRequired(message="Indica tu correo."), Email(message="Revisa el correo electrónico."), Length(max=120)])
    phone = StringField("Teléfono", validators=[DataRequired(message="Indica un teléfono de contacto."), Length(max=30)])
    subject = StringField("¿En qué podemos ayudarte?", validators=[DataRequired(message="Resume el asunto."), Length(max=150)])
    message = TextAreaField("Cuéntanos brevemente tu caso", validators=[DataRequired(message="Escribe un breve mensaje."), Length(min=20, max=3000, message="El mensaje debe tener entre 20 y 3000 caracteres.")])
    privacy = BooleanField("He leído y acepto la política de privacidad.", validators=[DataRequired(message="Debes aceptar la política de privacidad.")])


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-change-this-secret"),
        SITE_URL=os.getenv("SITE_URL", "http://localhost:5000").rstrip("/"),
        CONTACT_RECIPIENT=os.getenv("CONTACT_RECIPIENT", ""),  # TODO: configure recipient email
        FORMSPREE_ENDPOINT=os.getenv("FORMSPREE_ENDPOINT", ""),  # Formspree form endpoint
        MAPS_URL=os.getenv("GOOGLE_MAPS_URL", ""),  # TODO: configure Google Maps URL
        LINKEDIN_URL=os.getenv("LINKEDIN_URL", ""),  # TODO: configure verified LinkedIn URL
    )
    # Use shared Redis storage for this limiter when the app runs on multiple instances.
    limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

    @app.context_processor
    def inject_site_data():
        return {"current_year": datetime.now().year, "site": app.config}

    def page(template, title, description, **kwargs):
        return render_template(template, title=title, description=description, **kwargs)

    @app.get("/")
    def home():
        return page("home.html", "Abogada en Vigo | Lúa Casanova", "Abogada en Vigo especializada en derecho civil y laboral. Asesoramiento cercano, claro y riguroso en toda Galicia.")

    @app.get("/servicios")
    def services():
        return page("services.html", "Servicios jurídicos | Lúa Casanova", "Asesoramiento jurídico en derecho laboral y civil en Vigo y Galicia.")

    @app.get("/sobre-mi")
    def about():
        return page("about.html", "Sobre mí | Lúa Casanova, Abogada", "Conoce el enfoque cercano, honesto y riguroso de Lúa Casanova, abogada en Vigo.")

    @app.route("/contacto", methods=["GET", "POST"])
    @limiter.limit("5 per hour", methods=["POST"])
    def contact():
        form = ContactForm()
        submitted = False
        if form.validate_on_submit():
            endpoint = app.config["FORMSPREE_ENDPOINT"]
            if not endpoint:
                form.message.errors.append("El servicio de formularios no está configurado todavía. Llámenos al 657 528 018.")
            else:
                payload = {
                    "name": form.name.data,
                    "email": form.email.data,
                    "phone": form.phone.data,
                    "subject": form.subject.data,
                    "message": form.message.data,
                    "privacy_consent": "accepted",
                    "_subject": "Nueva consulta desde la web de Lúa Casanova",
                }
                try:
                    response = requests.post(
                        endpoint,
                        data=payload,
                        headers={
                            "Accept": "application/json",
                            "Origin": app.config["SITE_URL"],
                            "Referer": f'{app.config["SITE_URL"]}/contacto',
                        },
                        timeout=10,
                    )
                    if response.ok:
                        submitted = True
                        form = ContactForm(formdata=None)
                    else:
                        app.logger.warning("Form submission service rejected a request: %s", response.status_code)
                        form.message.errors.append("No se ha podido enviar la consulta. Inténtelo de nuevo o llámenos al 657 528 018.")
                except requests.RequestException:
                    app.logger.exception("Form submission service unavailable")
                    form.message.errors.append("No se ha podido enviar la consulta. Inténtelo de nuevo o llámenos al 657 528 018.")
        return page("contact.html", "Contacto | Lúa Casanova, Abogada", "Solicita una consulta con Lúa Casanova, abogada en Vigo.", form=form, submitted=submitted)

    @app.get("/recomendaciones")
    def recommendations():
        return page("recommendations.html", "Recomendaciones | Lúa Casanova", "Recomendaciones de clientes de Lúa Casanova, abogada en Vigo.")

    @app.get("/aviso-legal")
    def legal_notice():
        return page("legal.html", "Aviso legal | Lúa Casanova", "Aviso legal del sitio web de Lúa Casanova, abogada.", kind="Aviso legal")

    @app.get("/privacidad")
    def privacy():
        return page("legal.html", "Política de privacidad | Lúa Casanova", "Política de privacidad de Lúa Casanova, abogada.", kind="Política de privacidad")

    @app.get("/cookies")
    def cookies():
        return page("legal.html", "Política de cookies | Lúa Casanova", "Política de cookies de Lúa Casanova, abogada.", kind="Política de cookies")

    @app.get("/robots.txt")
    def robots():
        return app.response_class("User-agent: *\nAllow: /\nSitemap: " + app.config["SITE_URL"] + "/sitemap.xml\n", mimetype="text/plain")

    @app.get("/sitemap.xml")
    def sitemap():
        endpoints = ["home", "services", "about", "contact", "recommendations", "legal_notice", "privacy", "cookies"]
        urls = [app.config["SITE_URL"] + url_for(endpoint) for endpoint in endpoints]
        return render_template("sitemap.xml", urls=urls), 200, {"Content-Type": "application/xml"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
