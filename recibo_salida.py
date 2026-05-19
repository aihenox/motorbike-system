from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os


def generar_recibo_salida(
    id_ticket,
    placa,
    tipo,
    hora_ingreso,
    hora_salida,
    tiempo,
    valor
):

    placa = placa.upper()

    if not os.path.exists("recibos"):
        os.makedirs("recibos")

    archivo = f"recibos/salida_{id_ticket}.pdf"

    ancho = 80 * mm
    alto = 190 * mm

    c = canvas.Canvas(archivo, pagesize=(ancho, alto))

    y = alto - 15

    # =====================================================
    # LOGO
    # =====================================================
    try:

        logo = ImageReader("static/img/logo.png")

        c.drawImage(
            logo,
            10,
            y - 55,
            width=ancho - 20,
            height=50,
            preserveAspectRatio=True,
            mask='auto'
        )

        y -= 62

    except:

        y -= 10

    # =====================================================
    # ENCABEZADO
    # =====================================================
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(ancho / 2, y, "MOTORBIKE PARQUEADERO")

    y -= 15

    c.setFont("Helvetica", 9)
    c.drawCentredString(ancho / 2, y, "Cra 11 Calle 22 Esquina")

    y -= 12

    c.drawCentredString(
        ancho / 2,
        y,
        "3207081059 - 3217343167"
    )

    # =====================================================
    # LINEA
    # =====================================================
    y -= 12
    c.line(10, y, ancho - 10, y)

    # =====================================================
    # TITULO
    # =====================================================
    y -= 20

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(ancho / 2, y, "RECIBO DE SALIDA")

    # =====================================================
    # TICKET
    # =====================================================
    y -= 18

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(ancho / 2, y, f"TICKET No: {id_ticket}")

    # =====================================================
    # CODIGO BARRAS
    # =====================================================
    y -= 35

    barcode = code128.Code128(
        str(id_ticket),
        barHeight=25
    )

    barcode.drawOn(
        c,
        (ancho - barcode.width) / 2,
        y
    )

    # =====================================================
    # DATOS
    # =====================================================
    y -= 42

    c.setFont("Helvetica-Bold", 11)

    c.drawString(12, y, f"PLACA: {placa}")

    y -= 15

    c.drawString(12, y, f"TIPO: {tipo}")

    y -= 15

    c.drawString(12, y, f"ENTRADA:")

    y -= 12

    c.setFont("Helvetica", 10)
    c.drawString(15, y, hora_ingreso)

    y -= 18

    c.setFont("Helvetica-Bold", 11)
    c.drawString(12, y, f"SALIDA:")

    y -= 12

    c.setFont("Helvetica", 10)
    c.drawString(15, y, hora_salida)

    y -= 18

    c.setFont("Helvetica-Bold", 11)
    c.drawString(12, y, f"TIEMPO:")

    y -= 12

    c.setFont("Helvetica", 10)
    c.drawString(15, y, tiempo)

    # =====================================================
    # TOTAL
    # =====================================================
    y -= 22

    c.line(10, y, ancho - 10, y)

    y -= 22

    c.setFont("Helvetica-Bold", 16)

    c.drawCentredString(
        ancho / 2,
        y,
        f"TOTAL: ${valor:,}"
    )

    # =====================================================
    # MENSAJE
    # =====================================================
    y -= 30

    c.setFont("Helvetica", 9)

    c.drawCentredString(
        ancho / 2,
        y,
        "Gracias por utilizar nuestro servicio"
    )

    y -= 12

    c.drawCentredString(
        ancho / 2,
        y,
        "Motorbike Parqueadero"
    )

    c.save()
