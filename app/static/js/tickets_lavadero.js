// ==========================================
// ABRIR TICKET LAVADERO
// ==========================================
function abrirTicketLavadero(html){

    alert("Abriendo ticket");

    const ventana = window.open(
        "",
        "_blank"
    );

    console.log(
        "VENTANA:",
        ventana
    );

    if(!ventana){

        alert(
            "Popup bloqueado"
        );

        return;
    }

    ventana.document.open();

    ventana.document.write(
        html
    );

    ventana.document.close();

    setTimeout(() => {

        ventana.print();

    }, 500);
}


// ==========================================
// TICKET LAVADERO
// ==========================================
function generarTicketLavadero(data){

    return `

    <html>

    <head>

        <title>
            Recibo Lavado
        </title>

        <style>

            *{

                margin:0;

                padding:0;

                box-sizing:border-box;
            }

            body{

                font-family:'Courier New', monospace;

                width:300px;

                margin:auto;

                padding:14px;

                background:white;

                color:#000;

                font-size:12px;
            }

            .center{

                text-align:center;
            }

            .logo{

                width:85px;

                margin-bottom:8px;
            }

            .empresa{

                font-size:17px;

                font-weight:bold;

                margin-bottom:2px;
            }

            .subtitulo{

                font-size:11px;

                margin-bottom:4px;
            }

            .direccion{

                font-size:11px;

                margin-bottom:2px;
            }

            .telefonos{

                font-size:11px;

                margin-bottom:10px;
            }

            .linea{

                border-top:1px dashed #000;

                margin:10px 0;
            }

            .titulo{

                text-align:center;

                font-size:15px;

                font-weight:bold;

                margin-bottom:12px;
            }

            .dato{

                display:flex;

                justify-content:space-between;

                margin:8px 0;
            }

            .total{

                text-align:center;

                font-size:28px;

                font-weight:bold;

                margin:15px 0;
            }

            .footer{

                margin-top:15px;

                text-align:center;

                font-weight:bold;
            }

        </style>

    </head>

    <body>

        <div class="center">

            <img
                src="/static/img/logo.png"
                class="logo"
            >

            <div class="empresa">

                ESPUMOSO MOTORBIKE

            </div>

            <div class="subtitulo">

                PARQUEADERO Y LAVADERO

            </div>

            <div class="direccion">

                Cra 11 Calle 22 Esquina

            </div>

            <div class="telefonos">

                Tel: 3207081059

                <br>

                WhatsApp: 3217343167

            </div>

        </div>

        <div class="linea"></div>

        <div class="titulo">

            RECIBO DE LAVADO

        </div>

        <div class="linea"></div>

        <div class="dato">

            <span>
                PLACA:
            </span>

            <strong>
                ${data.placa}
            </strong>

        </div>

        <div class="dato">

            <span>
                VEHÍCULO:
            </span>

            <strong>
                ${data.vehiculo}
            </strong>

        </div>

        <div class="dato">

            <span>
                SERVICIO:
            </span>

            <strong>
                ${data.tipo_lavado}
            </strong>

        </div>

        <div class="dato">

            <span>
                RESPONSABLE:
            </span>

            <strong>
                ${data.responsable}
            </strong>

        </div>

        <div class="dato">

            <span>
                FECHA:
            </span>

            <strong>
                ${data.fecha}
            </strong>

        </div>

        <div class="linea"></div>

        <div class="total">

            $ ${data.valor}

        </div>

        <div class="linea"></div>

        <div class="footer">

            ¡Gracias por preferirnos!

        </div>
    
    </body>

    </html>

    `;
}