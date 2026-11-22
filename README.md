# Lúa Casanova — sitio web profesional

Sitio web corporativo de **Lúa Casanova Gómez**, abogada en Vigo. La aplicación presenta los servicios jurídicos de la firma, su enfoque profesional y un canal de contacto para consultas.

Está desarrollado con Flask y plantillas Jinja, con una interfaz responsive y contenidos en español.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Joey305/lua)

## Características

- Páginas de inicio, servicios, sobre mí, recomendaciones y contacto.
- Áreas de práctica: derecho laboral y derecho civil.
- Formulario de contacto con protección CSRF, validación en servidor y límite de solicitudes por IP.
- Envío de consultas mediante Formspree.
- Páginas de aviso legal, privacidad y cookies.
- `robots.txt` y sitemap XML generados desde la aplicación.
- Diseño adaptable a móvil, tableta y escritorio.

## Tecnologías

- Python 3
- Flask
- Jinja
- Flask-WTF y WTForms
- Flask-Limiter
- HTML, CSS y JavaScript

## Ejecutar el proyecto en local

### 1. Crear y activar un entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar las variables de entorno

Copia `.env.example` a `.env` y completa los valores necesarios:

```env
SECRET_KEY=una-clave-larga-y-aleatoria
SITE_URL=http://127.0.0.1:5000
FORMSPREE_ENDPOINT=https://formspree.io/f/TU_IDENTIFICADOR
GOOGLE_MAPS_URL=
LINKEDIN_URL=
```

> No subas el archivo `.env` ni claves, credenciales o identificadores de producción a un repositorio público.

### 4. Iniciar el servidor

```bash
flask --app app run --debug
```

Abre [http://127.0.0.1:5000](http://127.0.0.1:5000) en el navegador.

## Configuración

| Variable | Uso |
| --- | --- |
| `SECRET_KEY` | Protege las sesiones y los formularios CSRF. Usa un valor largo y aleatorio en producción. |
| `SITE_URL` | URL pública y canónica del sitio; se utiliza para el sitemap, `robots.txt` y el formulario. |
| `FORMSPREE_ENDPOINT` | Endpoint de Formspree que recibe las consultas del formulario. |
| `GOOGLE_MAPS_URL` | Enlace verificado a la ubicación profesional, si se desea mostrar. |
| `LINKEDIN_URL` | Perfil profesional de LinkedIn; se oculta si no se configura. |

## Despliegue

### Heroku

El proyecto incluye los archivos necesarios para Heroku:

- `Procfile`: inicia la aplicación con Gunicorn y escucha en el puerto asignado por Heroku.
- `.python-version`: fija Python 3.13 y permite recibir actualizaciones de seguridad de la misma versión.
- `app.json`: permite el despliegue con el botón **Deploy to Heroku** y genera `SECRET_KEY` automáticamente.

Después de publicar el repositorio en `https://github.com/Joey305/lua`, puedes usar el botón anterior o crear la aplicación desde la línea de comandos:

```bash
heroku create nombre-de-tu-app
heroku config:set SITE_URL=https://nombre-de-tu-app.herokuapp.com
heroku config:set FORMSPREE_ENDPOINT=https://formspree.io/f/TU_IDENTIFICADOR
git push heroku main
```

En el panel de Heroku, comprueba **Settings → Config Vars** y establece `SITE_URL` con la URL HTTPS final. Sin este valor, el sitemap, `robots.txt` y las cabeceras del formulario conservarán la URL local de desarrollo. Configura `FORMSPREE_ENDPOINT` antes de habilitar las consultas desde la web.

Para otros entornos de producción, utiliza Gunicorn detrás de HTTPS y configura las variables de entorno desde la plataforma de alojamiento. Si se ejecutan varias instancias de la aplicación, configura Flask-Limiter con almacenamiento Redis compartido para que los límites de solicitudes se apliquen de forma coherente.

Antes de publicar, revisa y completa los datos pendientes de las páginas legales, la información profesional, los enlaces externos y los contenidos de contacto.

## Estructura del proyecto

```text
.
├── app.py              # Aplicación Flask y rutas
├── Procfile            # Comando de inicio para Heroku
├── app.json            # Manifiesto para Deploy to Heroku
├── .python-version     # Versión de Python para Heroku
├── requirements.txt    # Dependencias de Python
├── static/             # Estilos, JavaScript e iconos
└── templates/          # Plantillas HTML Jinja
```

## Licencia

Todos los derechos reservados. El contenido, la identidad visual y los materiales de este sitio no pueden reutilizarse sin autorización expresa.
