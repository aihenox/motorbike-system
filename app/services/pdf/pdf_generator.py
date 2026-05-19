import os

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from app.services.pdf.barcode_service import (
    crear_codigo_barras
)


# ==========================================
# RECIBO INGRESO
# ==========================================
def generar_recibo_ingreso(
    ticket,
    placa,
    tipo,
    hora
):

    os.makedirs("recibos", exist_ok=True)

    ruta = f"recibos/recibo_{ticket}.pdf"

    ancho = 226
    alto = 600

    c = canvas.Canvas(
        ruta,
        pagesize=(ancho, alto)
    )

    y = 560

    # ==========================================
    # LOGO
    # ==========================================
    logo_path = "app/static/img/logo.png"

    if os.path.exists(logo_path):

        logo = ImageReader(logo_path)

        c.drawImage(
            logo,
            55,
            y - 80,
            width=120,
            height=120,
            preserveAspectRatio=True,
            mask='auto'
        )

    y -= 90

    # ==========================================
    # INFO NEGOCIO
    # ==========================================
    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "Cra 11 Calle 22 Esquina"
    )

    y -= 12

    c.drawCentredString(
        ancho / 2,
        y,
        "3207081059 - 3217433167"
    )

    y -= 12

    c.drawCentredString(
        ancho / 2,
        y,
        "NIT: PENDIENTE"
    )

    y -= 15

    c.line(10, y, 216, y)

    y -= 30

    # ==========================================
    # HEADER
    # ==========================================
    c.setFillColorRGB(0, 0, 0)

    c.rect(
        20,
        y,
        186,
        22,
        fill=1
    )

    c.setFillColorRGB(1, 1, 1)

    c.setFont(
        "Helvetica-Bold",
        11
    )

    c.drawCentredString(
        ancho / 2,
        y + 6,
        "RECIBO DE INGRESO"
    )

    c.setFillColorRGB(0, 0, 0)

    y -= 45

    # ==========================================
    # BARCODE
    # ==========================================
    barcode = crear_codigo_barras(ticket)

    barcode.drawOn(
        c,
        63,
        y
    )

    y -= 25

    # ==========================================
    # TICKET
    # ==========================================
    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawString(
        15,
        y,
        "RECIBO No:"
    )

    c.setFont(
        "Helvetica-Bold",
        18
    )

    c.drawRightString(
        205,
        y,
        f"{int(ticket):06d}"
    )

    y -= 30

    c.line(10, y, 216, y)

    y -= 30

    # ==========================================
    # DATOS
    # ==========================================
    c.setFont(
        "Helvetica",
        11
    )

    c.drawString(
        15,
        y,
        "Placa:"
    )

    c.setFont(
        "Helvetica-Bold",
        14
    )

    c.drawRightString(
        205,
        y,
        placa.upper()
    )

    y -= 28

    c.setFont(
        "Helvetica",
        11
    )

    c.drawString(
        15,
        y,
        "Tipo:"
    )

    c.setFont(
        "Helvetica-Bold",
        14
    )

    c.drawRightString(
        205,
        y,
        tipo.upper()
    )

    y -= 28

    c.setFont(
        "Helvetica",
        11
    )

    c.drawString(
        15,
        y,
        "Entrada:"
    )

    c.setFont(
        "Helvetica-Bold",
        9
    )

    c.drawRightString(
        205,
        y,
        hora.replace("T", " ")[:16]
    )

    y -= 25

    c.line(10, y, 216, y)

    y -= 35

    # ==========================================
    # REGLAMENTO
    # ==========================================
    c.setFillColorRGB(0, 0, 0)

    c.rect(
        40,
        y,
        140,
        18,
        fill=1
    )

    c.setFillColorRGB(1, 1, 1)

    c.setFont(
        "Helvetica-Bold",
        9
    )

    c.drawCentredString(
        ancho / 2,
        y + 5,
        "REGLAMENTO"
    )

    c.setFillColorRGB(0, 0, 0)

    y -= 30

    reglas = [

        "• El vehículo se entrega al portador.",
        "• No aceptamos órdenes telefónicas.",
        "• No aceptamos reclamos posteriores.",
        "• No respondemos por objetos.",
        "• No respondemos por hurto.",
        "• No respondemos por incendios.",
        "• Asegure bien su vehículo."
    ]

    c.setFont(
        "Helvetica",
        6.5
    )

    for regla in reglas:

        c.drawString(
            10,
            y,
            regla
        )

        y -= 14

    c.save()

    return ruta


# ==========================================
# RECIBO SALIDA POS COMPACTO
# ==========================================
def generar_recibo_salida(
    ticket,
    placa,
    tipo,
    hora_ingreso,
    hora_salida,
    tiempo,
    valor
):

    import os

    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader

    from app.services.pdf.barcode_service import (
        crear_codigo_barras
    )

    os.makedirs(
        "recibos",
        exist_ok=True
    )

    ruta = f"recibos/salida_{ticket}.pdf"

    # ==========================================
    # TAMAÑO PAPEL MÁS LARGO
    # ==========================================
    ancho = 226
    alto = 620

    c = canvas.Canvas(
        ruta,
        pagesize=(ancho, alto)
    )

    y = 565

    # ==========================================
    # LOGO
    # ==========================================
    logo_path = "app/static/img/logo.png"

    if os.path.exists(logo_path):

        logo = ImageReader(
            logo_path
        )

        c.drawImage(

            logo,

            38,

            y - 60,

            width=150,

            height=110,

            preserveAspectRatio=True,

            mask='auto'
        )

    y -= 85

    # ==========================================
    # HEADER NEGRO
    # ==========================================
    c.setFillColorRGB(0, 0, 0)

    c.roundRect(
        12,
        y,
        202,
        24,
        4,
        fill=1
    )

    c.setFillColorRGB(1, 1, 1)

    c.setFont(
        "Helvetica-Bold",
        11
    )

    c.drawCentredString(
        ancho / 2,
        y + 7,
        "RECIBO DE SALIDA"
    )

    c.setFillColorRGB(0, 0, 0)

    y -= 45

    # ==========================================
    # BARCODE
    # ==========================================
    barcode = crear_codigo_barras(
        ticket
    )

    barcode.drawOn(
        c,
        60,
        y
    )

    y -= 10

    # ==========================================
    # SEPARADOR
    # ==========================================
    c.setDash(3, 2)

    c.line(
        5,
        y,
        220,
        y
    )

    c.setDash()

    y -= 35

    # ==========================================
    # RECIBO
    # ==========================================
    c.setFont(
        "Helvetica-Bold",
        12
    )

    c.drawString(
        15,
        y,
        "RECIBO No:"
    )

    c.setFont(
        "Helvetica-Bold",
        22
    )

    c.drawRightString(
        205,
        y + 2,
        f"{int(ticket):05d}"
    )

    y -= 15

    # ==========================================
    # LINEA
    # ==========================================
    c.line(
        15,
        y,
        205,
        y
    )

    y -= 35

    # ==========================================
    # DATOS
    # ==========================================
    datos = [

        ("PLACA:", placa.upper()),

        ("TIPO:", tipo.upper()),

        ("FECHA INGRESO:", hora_ingreso),

        ("FECHA SALIDA:", hora_salida),

        ("TIEMPO TRANSCURRIDO:", tiempo)
    ]

    for titulo, dato in datos:

        c.setFont(
            "Helvetica-Bold",
            10
        )

        c.drawString(
            10,
            y,
            titulo
        )

        c.drawRightString(
            205,
            y,
            dato
        )

        y -= 18

        c.setDash(1, 2)

        c.line(
            10,
            y + 8,
            205,
            y + 8
        )

        c.setDash()

        y -= 12

    # ==========================================
    # BAJAR MÁS EL TOTAL
    # ==========================================
    y -= 80

    # ==========================================
    # TOTAL NEGRO
    # ==========================================
    c.setFillColorRGB(0, 0, 0)

    c.roundRect(
        12,
        y - 5,
        202,
        95,
        10,
        fill=1
    )

    c.setFillColorRGB(1, 1, 1)

    c.setFont(
        "Helvetica-Bold",
        14
    )

    c.drawCentredString(
        ancho / 2,
        y + 62,
        "TOTAL PAGADO"
    )

    c.setFont(
        "Helvetica-Bold",
        34
    )

    c.drawCentredString(
        ancho / 2,
        y + 22,
        f"${valor:,}"
    )

    c.setFillColorRGB(0, 0, 0)

    # ==========================================
    # ESPACIO DESPUÉS DEL TOTAL
    # ==========================================
    y -= 20

    # ==========================================
    # SEPARADOR FINAL
    # ==========================================
    c.setDash(3, 2)

    c.line(
        5,
        y,
        220,
        y
    )

    c.setDash()

    y -= 30

    # ==========================================
    # MENSAJE FINAL
    # ==========================================
    c.setFont(
        "Helvetica-Bold",
        15
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "¡Gracias por su visita!"
    )

    y -= 15

    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "ESPUMOSO MOTORBIKE WASH"
    )

    y -= 10

    c.setFont(
        "Helvetica",
        9
    )

    c.drawCentredString(
        ancho / 2,
        y,
        "Vuelve pronto"
    )

    # ==========================================
    # GUARDAR
    # ==========================================
    c.save()

    return ruta