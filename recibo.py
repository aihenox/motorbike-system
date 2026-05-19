from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

# ==========================================
# GENERAR RECIBO MODERNO
# ==========================================
def generar_recibo(id_ticket, placa, tipo, hora):

    placa = placa.upper()

    # ==========================================
    # FORMATO FECHA
    # ==========================================
    try:
        fecha = datetime.fromisoformat(hora)
        hora_formato = fecha.strftime("%d/%m/%y %H:%M")
    except:
        hora_formato = hora

    # ==========================================
    # CREAR CARPETA
    # ==========================================
    if not os.path.exists("recibos"):
        os.makedirs("recibos")

    archivo = f"recibos/recibo_{id_ticket}.pdf"

    # ==========================================
    # TAMAÑO TICKET POS
    # ==========================================
    ancho = 80 * mm
    alto = 170 * mm

    c = canvas.Canvas(archivo, pagesize=(ancho, alto))

    y = alto - 12

    # ==========================================
    # LOGO
    # ==========================================
    try:
        logo = ImageReader("logo.png")

        c.drawImage(
            logo,
            4,
            y - 88,
            width=ancho - 8,
            height=82,
            preserveAspectRatio=True,
            mask='auto'
        )

        y -= 105

    except:
        y -= 10

    # ==========================================
    # ENCABEZADO
    # ==========================================
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(ancho / 2, y, "MOTORBIKE PARQUEADERO")

    y -= 13

    c.setFont("Helvetica", 8)

    c.drawCentredString(ancho / 2, y, "NIT: PENDIENTE")
    y -= 10

    c.drawCentredString(ancho / 2, y, "Cra 11 Calle 22 Esquina")
    y -= 10

    c.drawCentredString(ancho / 2, y, "3207081059 - 3217343167")

    # ==========================================
    # LINEA
    # ==========================================
    y -= 12

    c.setLineWidth(0.4)
    c.line(8, y, ancho - 8, y)

    # ==========================================
    # RECIBO
    # ==========================================
    y -= 18

    c.setFont("Helvetica-Bold", 11)

    c.drawCentredString(
        ancho / 2,
        y,
        f"RECIBO No. {id_ticket}"
    )

    # ==========================================
    # CODIGO BARRAS
    # ==========================================
    y -= 34

    barcode = code128.Code128(
        str(id_ticket),
        barHeight=22,
        barWidth=0.6
    )

    barcode.drawOn(
        c,
        (ancho - barcode.width) / 2,
        y
    )

    # NUMERO BAJO CODIGO
    y -= 10

    c.setFont("Helvetica", 8)

    c.drawCentredString(
        ancho / 2,
        y,
        str(id_ticket)
    )

    # ==========================================
    # DATOS VEHICULO
    # ==========================================
    y -= 22

    c.setFont("Helvetica-Bold", 10)

    c.drawString(12, y, "PLACA:")
    c.setFont("Helvetica", 10)
    c.drawRightString(ancho - 12, y, placa)

    y -= 14

    c.setFont("Helvetica-Bold", 10)

    c.drawString(12, y, "TIPO:")
    c.setFont("Helvetica", 10)
    c.drawRightString(ancho - 12, y, tipo)

    y -= 14

    c.setFont("Helvetica-Bold", 10)

    c.drawString(12, y, "INGRESO:")
    c.setFont("Helvetica", 9)
    c.drawRightString(ancho - 12, y, hora_formato)

    # ==========================================
    # LINEA
    # ==========================================
    y -= 16

    c.line(8, y, ancho - 8, y)

    # ==========================================
    # REGLAMENTO
    # ==========================================
    y -= 16

    c.setFont("Helvetica-Bold", 10)

    c.drawCentredString(
        ancho / 2,
        y,
        "REGLAMENTO"
    )

    reglamento = [
        "• El vehículo se entrega al portador del presente recibo.",
        "",
        "• No aceptamos órdenes telefónicas ni escritas.",
        "",
        "• Retirado el vehículo no se aceptan reclamos posteriores.",
        "",
        "• No respondemos por objetos dejados dentro del vehículo.",
        "",
        "• Asegure correctamente su vehículo."
    ]

    y -= 15

    c.setFont("Helvetica", 7.5)

    for linea in reglamento:

        c.drawString(10, y, linea)

        y -= 9

    # ==========================================
    # FOOTER
    # ==========================================
    y -= 5

    c.line(8, y, ancho - 8, y)

    y -= 12

    c.setFont("Helvetica-Bold", 8)

    c.drawCentredString(
        ancho / 2,
        y,
        "GRACIAS POR SU VISITA"
    )

    c.save()