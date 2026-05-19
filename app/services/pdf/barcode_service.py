from reportlab.graphics.barcode import code128


# ==========================================
# GENERAR CÓDIGO BARRAS
# ==========================================
def crear_codigo_barras(ticket):

    return code128.Code128(
        str(ticket),
        barHeight=40,
        barWidth=1.2
    )