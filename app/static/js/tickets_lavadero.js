// ==========================================
// ABRIR TICKET LAVADERO
// ==========================================
function abrirTicketLavadero(html){

    const ventana = window.open(

        "",

        "ticket_lavado",

        "width=420,height=700"
    );

    if(!ventana){

        alert(
            "Permita ventanas emergentes para imprimir."
        );

        return;
    }

    ventana.document.open();

    ventana.document.write(
        html
    );

    ventana.document.close();

    setTimeout(() => {

        ventana.focus();

        ventana.print();

    }, 500);
}


// ==========================================
// GENERAR TICKET LAVADERO
// ==========================================
function generarTicketLavadero(data){

    return `

<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>

Recibo Lavadero

</title>

<style>

body{

    font-family:Arial,sans-serif;

    width:300px;

    margin:auto;

    padding:15px;

    text-align:center;
}

h2{

    margin-bottom:5px;
}

.linea{

    border-top:1px dashed #000;

    margin:10px 0;
}

.dato{

    text-align:left;

    margin:6px 0;
}

.total{

    font-size:26px;

    font-weight:bold;

    margin-top:15px;
}

</style>

</head>

<body>

<h2>

ESPUMOSO MOTORBIKE

</h2>

<p>

PARQUEADERO Y LAVADERO

</p>

<div class="linea"></div>

<h3>

RECIBO DE LAVADO

</h3>

<div class="linea"></div>

<div class="dato">

<strong>Placa:</strong>

${data.placa}

</div>

<div class="dato">

<strong>Vehículo:</strong>

${data.vehiculo}

</div>

<div class="dato">

<strong>Servicio:</strong>

${data.tipo_lavado}

</div>

<div class="dato">

<strong>Responsable:</strong>

${data.responsable}

</div>

<div class="dato">

<strong>Fecha:</strong>

${data.fecha}

</div>

<div class="linea"></div>

<div class="total">

$ ${data.valor}

</div>

<div class="linea"></div>

<p>

¡Gracias por preferirnos!

</p>

</body>

</html>

`;
}