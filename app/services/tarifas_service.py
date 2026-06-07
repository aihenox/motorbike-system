from app.repositories.tarifas_repository import (
    obtener_tarifas_db,
    actualizar_tarifas_db,
    obtener_tarifa_activa_db
)

# ==========================================
# OBTENER TARIFAS
# ==========================================
def obtener_tarifas():

    return obtener_tarifas_db()


# ==========================================
# ACTUALIZAR TARIFAS
# ==========================================
def actualizar_tarifas(

    hora_moto,
    hora_carro,

    dia_moto,
    dia_carro,

    noche_moto,
    noche_carro,

    mensualidad_moto,
    mensualidad_carro,

    minutos_gracia
):

    actualizar_tarifas_db(

        hora_moto,
        hora_carro,

        dia_moto,
        dia_carro,

        noche_moto,
        noche_carro,

        mensualidad_moto,
        mensualidad_carro,

        minutos_gracia
    )

# ==========================================
# TARIFA ACTIVA
# ==========================================
def obtener_tarifa_activa():

    tarifa = obtener_tarifa_activa_db()

    if tarifa:

        return dict(tarifa)

    return None