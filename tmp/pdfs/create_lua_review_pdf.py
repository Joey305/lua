from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

OUT = "output/pdf/lua-casanova-web-approval.pdf"
W, H = A4
INK = HexColor("#16202C")
PAPER = HexColor("#FAF8F5")
SAND = HexColor("#C89B7B")
SAND_LIGHT = HexColor("#EBDFD4")
LINE = HexColor("#DED9D3")
MARGIN = 48


def label(c, text, x, y):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x, y, text.upper())


def field(c, name, x, y, width, height=22, multiline=False, value=""):
    c.setStrokeColor(LINE)
    c.setFillColor(white)
    flags = "multiline" if multiline else ""
    c.acroForm.textfield(
        name=name, x=x, y=y-height, width=width, height=height,
        value=value, borderStyle="solid", borderWidth=.7, borderColor=LINE,
        fillColor=white, textColor=INK, forceBorder=True, fontName="Helvetica",
        fontSize=9, fieldFlags=flags,
    )


def checkbox(c, name, text, x, y):
    c.acroForm.checkbox(name=name, x=x, y=y-9, size=11, buttonStyle="check",
                        borderWidth=.7, borderColor=INK, fillColor=white,
                        textColor=INK, forceBorder=True)
    c.setFillColor(INK)
    c.setFont("Helvetica", 8.5)
    c.drawString(x+18, y-1, text)


def text(c, value, x, y, size=9, leading=13, color=INK, max_width=None):
    c.setFillColor(color)
    c.setFont("Helvetica", size)
    words = value.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if max_width and stringWidth(test, "Helvetica", size) > max_width:
            c.drawString(x, y, line)
            y -= leading
            line = word
        else:
            line = test
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def header(c, page, title, background=True):
    c.resetTransforms()
    if background:
        c.setFillColor(PAPER)
        c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Times-Italic", 25)
    c.drawString(MARGIN, H-52, "Lúa Casanova")
    c.setFont("Helvetica-Bold", 6.8)
    c.drawString(MARGIN+2, H-64, "ABOGADA  |  WEB REVIEW")
    c.setStrokeColor(SAND)
    c.line(MARGIN, H-78, W-MARGIN, H-78)
    c.setFillColor(SAND)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(W-MARGIN, H-55, title.upper())
    c.setFillColor(HexColor("#7A858C"))
    c.setFont("Helvetica", 7)
    c.drawString(MARGIN, 26, "Lúa Casanova · Website review & approval")
    c.drawRightString(W-MARGIN, 26, f"{page} / 4")


def section_title(c, number, title, y):
    c.setFillColor(SAND)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(MARGIN, y, number)
    c.setFillColor(INK)
    c.setFont("Times-Bold", 20)
    c.drawString(MARGIN+27, y-4, title)
    return y-31


def make_pdf():
    c = canvas.Canvas(OUT, pagesize=A4, pageCompression=1)
    c.setTitle("Lúa Casanova - Website review and approval")
    # Page 1
    header(c, 1, "Review pack")
    y = 690
    y = section_title(c, "01", "A quick review, in one place.", y)
    y = text(c, "This form gathers the decisions, details and assets needed to make the website accurate, personal and ready to share. Please tick what is approved, add any changes, and return the completed PDF.", MARGIN, y, 10, 15, max_width=470)
    y -= 19
    c.setFillColor(SAND_LIGHT); c.roundRect(MARGIN, y-86, W-2*MARGIN, 86, 5, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Times-Bold", 16); c.drawString(MARGIN+17, y-25, "How to use this document")
    text(c, "1. Review the current website direction.  2. Fill in the open fields.  3. Tick approvals or leave notes where something needs changing.  4. Return it together with any requested files or links.", MARGIN+17, y-46, 9, 14, max_width=450)
    y -= 119
    label(c, "Your name", MARGIN, y); field(c, "reviewer_name", MARGIN, y-6, 220)
    label(c, "Date", 300, y); field(c, "review_date", 300, y-6, 120)
    y -= 61
    label(c, "Overall decision", MARGIN, y)
    checkbox(c, "overall_approved", "Approved as presented", MARGIN, y-19)
    checkbox(c, "overall_changes", "Approved with changes noted below", MARGIN+185, y-19)
    y -= 54
    label(c, "Your overall notes or priorities", MARGIN, y)
    field(c, "overall_notes", MARGIN, y-7, W-2*MARGIN, 68, multiline=True)
    y -= 99
    c.setStrokeColor(LINE); c.line(MARGIN, y, W-MARGIN, y)
    y -= 25
    text(c, "What is already in the site: calm editorial visual language, mobile navigation, service pages, contact form, location context and legal-information placeholders. Nothing in this pack publishes the site or changes its legal content.", MARGIN, y, 8.5, 13, HexColor("#59646C"), max_width=480)
    header(c, 1, "Review pack", background=False)
    c.showPage()

    # Page 2
    header(c, 2, "Accuracy & copy")
    y = 690
    y = section_title(c, "02", "Confirm the essentials.", y)
    text(c, "Please confirm the information that appears in the header, footer, contact page and search metadata. Correct anything that is no longer accurate.", MARGIN, y, 9.5, 14, max_width=480)
    y -= 34
    for name, caption, current in [
        ("phone", "Telephone", "657 528 018"),
        ("email", "Email", "lcasanova@icavigo.org"),
        ("address", "Office address", "Rúa de Urzáiz, 31, 4D · 36201 Vigo, Galicia"),
        ("hours", "Office hours", "Mon-Fri 09:00-14:00 · Mon-Thu 16:30-19:00"),
    ]:
        label(c, caption, MARGIN, y)
        field(c, name, MARGIN, y-6, W-2*MARGIN, value=current)
        y -= 52
    checkbox(c, "appointment_copy", "Keep the wording: Atención con cita previa · Vigo y Galicia.", MARGIN, y)
    y -= 34
    label(c, "Corrections or additional copy notes", MARGIN, y)
    field(c, "copy_notes", MARGIN, y-7, W-2*MARGIN, 60, multiline=True)
    y -= 91
    c.setFillColor(SAND_LIGHT); c.rect(MARGIN, y-60, W-2*MARGIN, 60, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 8); c.drawString(MARGIN+14, y-18, "LEGAL / BUSINESS DETAILS")
    text(c, "Please send or confirm the final professional, business and legal details still marked as TODO before launch. These should be reviewed by Lúa or the appropriate adviser.", MARGIN+14, y-34, 8.5, 12, max_width=450)
    header(c, 2, "Accuracy & copy", background=False)
    c.showPage()

    # Page 3
    header(c, 3, "Assets & links")
    y = 690
    y = section_title(c, "03", "The finishing details.", y)
    text(c, "These items are optional where noted, but they make the site feel complete and ensure visitors can find the right information.", MARGIN, y, 9.5, 14, max_width=480)
    y -= 37
    label(c, "Professional portrait - please provide a high-resolution image", MARGIN, y)
    field(c, "portrait_delivery", MARGIN, y-6, W-2*MARGIN, 22)
    y -= 52
    label(c, "Confirmed Google Maps link", MARGIN, y)
    field(c, "maps_link", MARGIN, y-6, W-2*MARGIN, 22)
    y -= 52
    label(c, "LinkedIn link (optional)", MARGIN, y)
    field(c, "linkedin_link", MARGIN, y-6, W-2*MARGIN, 22)
    y -= 52
    label(c, "Contact form recipient / service configuration", MARGIN, y)
    field(c, "form_configuration", MARGIN, y-6, W-2*MARGIN, 22)
    y -= 53
    checkbox(c, "portrait_understood", "I understand that the current About-page image is a temporary placeholder.", MARGIN, y)
    y -= 35
    checkbox(c, "recommendations_hold", "Keep recommendations unpublished until a review process and approved content are provided.", MARGIN, y)
    y -= 41
    label(c, "Notes on recommendations, services, imagery or anything else", MARGIN, y)
    field(c, "asset_notes", MARGIN, y-7, W-2*MARGIN, 75, multiline=True)
    y -= 108
    c.setStrokeColor(SAND); c.setLineWidth(1.2); c.line(MARGIN, y, MARGIN+56, y)
    text(c, "Preferred asset delivery: email or shared folder link. Please label images clearly and only send material you have permission to use.", MARGIN, y-19, 8.5, 12, HexColor("#59646C"), max_width=450)
    header(c, 3, "Assets & links", background=False)
    c.showPage()

    # Page 4
    header(c, 4, "Approval")
    y = 690
    y = section_title(c, "04", "Final checks before handoff.", y)
    text(c, "Tick each item once it is confirmed. Any unchecked item can remain open - it simply gives us a clear next-action list.", MARGIN, y, 9.5, 14, max_width=480)
    y -= 43
    checks = [
        ("approve_design", "I approve the current visual direction and website tone."),
        ("approve_copy", "I have reviewed the on-page copy and submitted needed corrections."),
        ("approve_details", "I have confirmed contact, office and business details."),
        ("approve_links", "I have supplied or confirmed the relevant Maps and LinkedIn links."),
        ("approve_form", "I have confirmed the contact-form recipient/service configuration."),
        ("approve_reviews", "I understand recommendations will remain unpublished until separately approved."),
    ]
    for name, sentence in checks:
        checkbox(c, name, sentence, MARGIN, y)
        y -= 31
    y -= 11
    label(c, "Open items and requested changes", MARGIN, y)
    field(c, "final_open_items", MARGIN, y-7, W-2*MARGIN, 78, multiline=True)
    y -= 113
    label(c, "Approval name", MARGIN, y); field(c, "approval_name", MARGIN, y-6, 220)
    label(c, "Date", 300, y); field(c, "approval_date", 300, y-6, 120)
    y -= 59
    c.setFillColor(INK); c.setFont("Times-Italic", 15); c.drawString(MARGIN, y, "Thank you - clarity now makes the final site feel like yours.")
    header(c, 4, "Approval", background=False)
    c.showPage()
    c.save()


if __name__ == "__main__":
    make_pdf()
