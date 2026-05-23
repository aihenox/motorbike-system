def validar_placa(placa):

    placa = placa.strip().upper()

    return placa.isalnum()