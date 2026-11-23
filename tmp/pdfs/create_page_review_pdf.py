from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white

OUT='output/pdf/lua-casanova-page-by-page-review.pdf'; W,H=A4; M=48
INK=HexColor('#16202C'); PAPER=HexColor('#FAF8F5'); SAND=HexColor('#C89B7B'); PALE=HexColor('#EBDFD4'); LINE=HexColor('#DED9D3')
pages=[('Inicio','/', 'Primera impresión, mensaje principal, servicios destacados y ubicación.'),('Servicios','/servicios','Áreas de práctica, alcance de los servicios y cualquier lenguaje que prefiera ajustar.'),('Sobre mí','/sobre-mi','Presentación profesional, enfoque, valores y el retrato temporal.'),('Contacto','/contacto','Datos de contacto, horario, cita previa y experiencia del formulario.'),('Información legal','/aviso-legal','Aviso legal, privacidad y cookies: confirmar o aportar contenido revisado.')]
base='https://lua-e983a9ceab31.herokuapp.com'
def header(c,n,title):
 c.resetTransforms(); c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0);c.setFillColor(INK);c.setFont('Times-Italic',25);c.drawString(M,H-52,'Lúa Casanova');c.setFont('Helvetica-Bold',7);c.drawString(M,H-64,'ABOGADA  |  WEB REVIEW');c.setStrokeColor(SAND);c.line(M,H-78,W-M,H-78);c.setFillColor(SAND);c.setFont('Helvetica-Bold',8);c.drawRightString(W-M,H-55,title.upper());c.setFillColor(HexColor('#7A858C'));c.setFont('Helvetica',7);c.drawString(M,26,'Lúa Casanova · Page-by-page review');c.drawRightString(W-M,26,f'{n} / 8')
def text(c,s,x,y,size=10,lead=15):
 c.setFillColor(INK);c.setFont('Helvetica',size);words=s.split();line=''
 for w in words:
  t=(line+' '+w).strip()
  if c.stringWidth(t,'Helvetica',size)>470:c.drawString(x,y,line);y-=lead;line=w
  else:line=t
 c.drawString(x,y,line);return y-lead
def field(c,name,x,y,w,h=24,multi=False):
 c.acroForm.textfield(name=name,x=x,y=y-h,width=w,height=h,borderColor=LINE,fillColor=white,textColor=INK,fontName='Helvetica',fontSize=9,forceBorder=True,fieldFlags='multiline' if multi else '')
def check(c,name,label,x,y):
 c.acroForm.checkbox(name=name,x=x,y=y-9,size=11,borderColor=INK,fillColor=white,forceBorder=True);c.setFillColor(INK);c.setFont('Helvetica',9);c.drawString(x+18,y-1,label)
def page(c,n,name,path,focus):
 header(c,n,name);y=690;c.setFillColor(SAND);c.setFont('Helvetica-Bold',8);c.drawString(M,y,'PAGE REVIEW');c.setFillColor(INK);c.setFont('Times-Bold',24);c.drawString(M,y-31,name);y-=65;text(c,'Click the button below to review this live page. Then confirm what works and tell us exactly what you would like changed.',M,y);y-=46
 c.setFillColor(INK);c.roundRect(M,y-38,235,30,4,fill=1,stroke=0);c.setFillColor(white);c.setFont('Helvetica-Bold',9);c.drawCentredString(M+117,y-27,'OPEN LIVE PAGE ↗');c.linkURL(base+path,(M,y-38,M+235,y-8),relative=0);c.setFillColor(HexColor('#59646C'));c.setFont('Helvetica',8);c.drawString(M+250,y-27,base+path);y-=75
 c.setFillColor(PALE);c.roundRect(M,y-68,W-2*M,68,4,fill=1,stroke=0);c.setFillColor(INK);c.setFont('Helvetica-Bold',8);c.drawString(M+15,y-20,'WHAT TO REVIEW');text(c,focus,M+15,y-38,9,13);y-=100
 check(c,f'{n}_approved','Approved as presented',M,y);check(c,f'{n}_changes','I would like changes - notes below',M+190,y);y-=42
 c.setFillColor(INK);c.setFont('Helvetica-Bold',8);c.drawString(M,y,'COPY, DETAILS OR DESIGN CHANGES');field(c,f'{n}_notes',M,y-7,W-2*M,125,True);y-=162
 c.setFont('Helvetica-Bold',8);c.drawString(M,y,'MISSING ASSETS, LINKS OR INFORMATION FOR THIS PAGE');field(c,f'{n}_assets',M,y-7,W-2*M,70,True);c.showPage()
def domains(c,n,items):
 header(c,n,'Domains & final notes');y=690;c.setFillColor(SAND);c.setFont('Helvetica-Bold',8);c.drawString(M,y,'DOMAIN IDEAS');c.setFillColor(INK);c.setFont('Times-Bold',23);c.drawString(M,y-31,'Choose a name to check.')
 y=text(c,'These are SEO-relevant, easy-to-understand options for a Vigo-based lawyer. Availability and trademark status must be checked with a registrar before purchase.',M,y-62);y-=22
 for d in items:
  check(c,'domain_'+d.replace('.','_'),d,M,y);y-=31
 y-=10;c.setFillColor(INK);c.setFont('Helvetica-Bold',8);c.drawString(M,y,'PREFERRED DOMAIN / OTHER IDEA');field(c,f'preferred_domain_{n}',M,y-7,W-2*M);y-=52;c.drawString(M,y,'FINAL NOTES OR PRIORITIES');field(c,f'final_notes_{n}',M,y-7,W-2*M,85,True);c.showPage()
def needs(c):
 header(c,8,'Needs from Lúa');y=690;c.setFillColor(SAND);c.setFont('Helvetica-Bold',8);c.drawString(M,y,'FINAL INPUTS');c.setFillColor(INK);c.setFont('Times-Bold',23);c.drawString(M,y-31,'What we still need from you.');y=text(c,'Please tick each item when provided or confirmed.',M,y-62);y-=22
 for key,label in [('portrait','Professional portrait (high-resolution, approved for web use)'),('business','Verified legal and business details still marked TODO'),('linkedin','Confirmed LinkedIn link, if desired'),('reviews','Approved review process and content, if recommendations will be used'),('form','Contact-form recipient / service configuration')]:check(c,'need_'+key,label,M,y);y-=34
 c.setFont('Helvetica-Bold',8);c.drawString(M,y,'LINKS, FILES OR QUESTIONS');field(c,'needs_notes',M,y-7,W-2*M,120,True);c.showPage()
c=canvas.Canvas(OUT,pagesize=A4);c.setTitle('Lúa Casanova - Page-by-page website review')
for i,(a,b,d) in enumerate(pages,1):page(c,i,a,b,d)
domains(c,6,['luacasanovaabogada.es','luacasanovaabogada.com','abogadaluacasanova.es','abogadaluacasanova.com','luacasanovavigo.es','luacasanovavigo.com','luacasanovalegal.es','luacasanovalegal.com','luacasanovagomez.es','luacasanovagomez.com'])
domains(c,7,['luacasanovaderecho.es','luacasanovalaboral.es','abogadalua.es','abogadalua.com','abogadaluavigo.es','abogadaluavigo.com','despacholuacasanova.es','abogadacasanovavigo.es','abogadalaboralcivilvigo.es','abogadalaboralcivilvigo.com'])
needs(c);c.save()
