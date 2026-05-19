import os

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode import createBarcodeDrawing

from config import Config


# ==========================================
# PDF INGRESO
# ==========================================
def generar_pdf_ingreso(
    ticket,
    placa,
    tipo,
    hora_ingreso
):

    carpeta = Config.RECIBOS_FOLDER

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    nombre_pdf = f"recibo_ingreso_{ticket}.pdf"

    ruta_pdf = os.path.join(
        carpeta,
        nombre_pdf
    )

    ancho = 226
    alto = 500

    c = canvas.Canvas(
        ruta_pdf,
        pagesize=(ancho, alto)
    )

    y = alto - 15

    ruta_logo = os.path.join(
        Config.BASE_DIR,
        "app",
        "static",
        "img",
        "logo.png"
    )

    if os.path.exists(ruta_logo):

        logo = ImageReader(ruta_logo)

        c.drawImage(
            logo,
            35,
            y - 95,
            width=155,
            height=85,
            preserveAspectRatio=True,
            mask='auto'
        )

    y -= 105

    c.setFont("Helvetica-Bold", 8)

    c.drawCentredString(
        ancho / 2,
        y,
        "Cra 11 Calle 22 Esquina"
    )

    y -= 12

    c.drawCentredString(
        ancho / 2,
        y,
        "3207081059 - 3217343167"
    )

    y -= 12

    c.drawCentredString(
        ancho / 2,
        y,
        "NIT: PENDIENTE"
    )

    y -= 18

    c.line(15, y, 210, y)

    y -= 22

    c.setFillColorRGB(0, 0, 0)

    c.rect(
        20,
        y - 8,
        185,
        20,
        fill=1
    )

    c.setFillColorRGB(1, 1, 1)

    c.setFont("Helvetica-Bold", 11)

    c.drawCentredString(
        ancho / 2,
        y - 1,
        "RECIBO DE INGRESO"
    )

    y -= 35

    barcode = createBarcodeDrawing(
        "Code128",
        value=str(ticket),
        barHeight=25,
        barWidth=1,
        humanReadable=False
    )

    barcode_width = barcode.width

    barcode_x = (ancho - barcode_width) / 2

    barcode.drawOn(
        c,
        barcode_x,
        y
    )

    y -= 40

    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica-Bold", 9)

    c.drawString(
        18,
        y,
        "RECIBO No:"
    )

    c.setFont("Helvetica-Bold", 18)

    c.drawRightString(
        200,
        y,
        f"{ticket:06}"
    )

    y -= 22

    c.line(15, y, 210, y)

    y -= 22

    c.setFont("Helvetica", 10)

    c.drawString(18, y, "Placa:")

    c.setFont("Helvetica-Bold", 13)

    c.drawRightString(
        200,
        y,
        placa
    )

    y -= 26

    c.setFont("Helvetica", 10)

    c.drawString(18, y, "Tipo:")

    c.setFont("Helvetica-Bold", 13)

    c.drawRightString(
        200,
        y,
        tipo.upper()
    )

    y -= 26

    c.setFont("Helvetica", 10)

    c.drawString(18, y, "Entrada:")

    c.setFont("Helvetica-Bold", 10)

    c.drawRightString(
        200,
        y,
        hora_ingreso.strftime("%d/%m/%Y %H:%M")
    )

    y -= 20

    c.line(15, y, 210, y)

    y -= 22

    c.setFillColorRGB(0, 0, 0)

    c.rect(
        40,
        y - 8,
        145,
        18,
        fill=1
    )

    c.setFillColorRGB(1, 1, 1)

    c.setFont("Helvetica-Bold", 9)

    c.drawCentredString(
        ancho / 2,
        y - 1,
        "REGLAMENTO"
    )

    y -= 24

    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica", 6)

    reglas = [

        "• El vehículo se entrega al portador.",
        "• No aceptamos órdenes telefónicas.",
        "• No aceptamos reclamos posteriores.",
        "• No respondemos por objetos.",
        "• No respondemos por hurto.",
        "• No respondemos por incendios.",
        "• Asegure bien su vehículo.",
        "• No respondemos por terceros."
    ]

    for regla in reglas:

        c.drawString(
            12,
            y,
            regla
        )

        y -= 12

    c.save()

    return ruta_pdf

# ==========================================
# PDF SALIDA
# ==========================================
def generar_pdf_salida(
    ticket,
    placa,
    tipo,
    valor,
    hora_ingreso,
    hora_salida
):

    carpeta = Config.RECIBOS_FOLDER

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    nombre_pdf = f"recibo_salida_{ticket}.pdf"

    ruta_pdf = os.path.join(
        carpeta,
        nombre_pdf
    )

    ancho = 226
    alto = 760

    c = canvas.Canvas(
        ruta_pdf,
        pagesize=(ancho, alto)
    )

    # ==========================================
    # POSICION INICIAL
    # ==========================================
    y = alto - 10

    # ==========================================
    # LOGO
    # ==========================================
    ruta_logo = os.path.join(
        Config.BASE_DIR,
        "app",
        "static",
        "img",
        "logo.png"
    )

    if os.path.exists(ruta_logo):

        logo = ImageReader(ruta_logo)

        c.drawImage(
            logo,
            35,
            y - 90,
            width=155,
            height=85,
            preserveAspectRatio=True,
            mask='auto'
        )

    # ==========================================
    # TITULO
    # ==========================================
    y -= 105

    c.setFillColorRGB(0, 0, 0)

    c.roundRect(
        15,
        y - 8,
        195,
        24,
        4,
        fill=1
    )

    c.setFillColorRGB(1, 1, 1)

    c.setFont(
        "Helvetica-Bold",
        14
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "RECIBO DE SALIDA"
    )

    # ==========================================
    # CODIGO BARRAS
    # ==========================================
    y -= 58

    barcode = createBarcodeDrawing(
        "Code128",
        value=str(ticket).zfill(5),
        barHeight=38,
        barWidth=1.1,
        humanReadable=False
    )

    barcode_width = barcode.width

    barcode_x = (ancho - barcode_width) / 2

    barcode.drawOn(
        c,
        barcode_x,
        y
    )

    # ==========================================
    # LINEA
    # ==========================================
    y -= 28

    c.setDash(4, 3)

    c.line(
        8,
        y,
        218,
        y
    )

    c.setDash()

    # ==========================================
    # RECIBO NO
    # ==========================================
    y -= 38

    c.setFillColorRGB(0, 0, 0)

    c.setFont(
        "Helvetica-Bold",
        11
    )

    c.drawString(
        18,
        y,
        "RECIBO No:"
    )

    c.setFont(
        "Helvetica-Bold",
        32
    )

    c.drawRightString(
        205,
        y,
        str(ticket).zfill(5)
    )

    # ==========================================
    # LINEA NEGRA
    # ==========================================
    y -= 32

    c.setLineWidth(1)

    c.line(
        15,
        y,
        210,
        y
    )

    # ==========================================
    # FUNCION FILAS
    # ==========================================
    y -= 40

    def fila(
        label,
        valor_texto
    ):

        nonlocal y

        # LABEL
        c.setFillColorRGB(0, 0, 0)

        c.setFont(
            "Helvetica-Bold",
            10
        )

        c.drawString(
            18,
            y,
            label
        )

        # VALOR
        c.setFont(
            "Helvetica-Bold",
            10
        )

        c.drawRightString(
            205,
            y,
            str(valor_texto)
        )

        # LINEA
        y -= 16

        c.setDash(1, 3)

        c.line(
            15,
            y,
            210,
            y
        )

        c.setDash()

        y -= 22

    # ==========================================
    # DATOS
    # ==========================================
    fila(
        "PLACA:",
        placa
    )

    fila(
        "TIPO:",
        tipo.upper()
    )

    fila(
        "FECHA INGRESO:",
        hora_ingreso.strftime("%d/%m/%Y %I:%M %p")
    )

    fila(
        "FECHA SALIDA:",
        hora_salida.strftime("%d/%m/%Y %I:%M %p")
    )

    # ==========================================
    # TIEMPO TRANSCURRIDO
    # ==========================================
    tiempo = hora_salida - hora_ingreso

    horas = int(
        tiempo.total_seconds() // 3600
    )

    minutos = int(
        (tiempo.total_seconds() % 3600) // 60
    )

    tiempo_formateado = f"{horas:02}:{minutos:02}"

    fila(
        "TIEMPO TRANSCURRIDO:",
        tiempo_formateado
    )

    # ==========================================
    # TOTAL PAGADO
    # ==========================================
    y -= 70

    c.setFillColorRGB(0, 0, 0)

    c.roundRect(
        15,
        y - 15,
        195,
        92,
        12,
        fill=1
    )

    c.setFillColorRGB(1, 1, 1)

    c.setFont(
        "Helvetica-Bold",
        16
    )

    c.drawCentredString(
        ancho / 2,
        y + 50,
        "TOTAL PAGADO"
    )

    c.setFont(
        "Helvetica-Bold",
        44
    )

    c.drawCentredString(
        ancho / 2,
        y + 5,
        f"${valor}"
    )

    # ==========================================
    # LINEA FINAL
    # ==========================================
    y -= 45

    c.setFillColorRGB(0, 0, 0)

    c.setDash(4, 3)

    c.line(
        15,
        y,
        210,
        y
    )

    c.setDash()

    # ==========================================
    # MENSAJE FINAL
    # ==========================================
    y -= 35

    c.setFont(
        "Helvetica-Bold",
        16
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "¡Gracias por su visita!"
    )

    y -= 24

    c.setFont(
        "Helvetica-Bold",
        11
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "ESPUMOSO MOTORBIKE WASH"
    )

    y -= 18

    c.setFont(
        "Helvetica",
        10
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "Vuelve pronto"
    )

    c.save()

    return ruta_pdf