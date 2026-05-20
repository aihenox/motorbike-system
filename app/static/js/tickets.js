// ==========================================
// ABRIR TICKET
// ==========================================
function abrirTicket(html, ticketId){

    const ventana = window.open(
        "",
        "_blank",
        "width=400,height=900"
    );

    ventana.document.write(html);

    ventana.document.close();

    // ==========================================
    // CUANDO CARGA
    // ==========================================
    ventana.onload = function(){

        const script = ventana.document.createElement(
            "script"
        );

        script.src =
            "https://cdn.jsdelivr.net/npm/jsbarcode@3.11.6/dist/JsBarcode.all.min.js";

        script.onload = function(){

            ventana.JsBarcode(

                ventana.document.getElementById(
                    "barcode"
                ),

                String(ticketId).padStart(
                    6,
                    "0"
                ),

                {

                    format: "CODE128",

                    width: 2,

                    height: 50,

                    displayValue: true,

                    fontSize: 16,

                    margin: 10
                }
            );

            ventana.print();
        };

        ventana.document.head.appendChild(
            script
        );
    };
}


// ==========================================
// HEADER EMPRESA
// ==========================================
function generarHeaderTicket(){

    return `

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

    `;
}


// ==========================================
// TERMINOS
// ==========================================
function generarTerminos(){

    return `

        <div class="terminos">

            <p>
                El ingreso del vehículo implica aceptación de los presentes términos y condiciones.
            </p>

            <p>
                El vehículo será entregado únicamente al portador del comprobante de ingreso.
            </p>

            <p>
                No se aceptan reclamaciones posteriores al retiro del vehículo.
            </p>

            <p>
                El establecimiento no responde por objetos, dinero o documentos dejados dentro del vehículo.
            </p>

            <p>
                El parqueadero no asume responsabilidad por hurto, incendio, daños causados por terceros o fuerza mayor.
            </p>

            <p>
                En caso de pérdida del comprobante, la entrega del vehículo solo se realizará con la tarjeta de propiedad.
            </p>

        </div>

    `;
}


// ==========================================
// ESTILOS BASE
// ==========================================
function generarEstilosTicket(){

    return `

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

                font-size:15px;

                font-weight:bold;

                margin-bottom:12px;

                text-align:center;
            }

            .ticket{

                font-size:36px;

                font-weight:bold;

                text-align:center;

                margin:16px 0;
            }

            .dato{

                display:flex;

                justify-content:space-between;

                gap:10px;

                margin:8px 0;

                font-size:12px;
            }

            .dato strong{

                text-align:right;
            }

            .barcode{

                text-align:center;

                margin-top:18px;
            }

            .mensaje{

                text-align:center;

                margin-top:15px;

                font-size:12px;

                font-weight:bold;
            }

            .terminos{

                margin-top:18px;

                font-size:10px;

                line-height:15px;

                text-align:justify;
            }

            .terminos p{

                margin-bottom:8px;
            }

            .footer{

                margin-top:15px;

                text-align:center;

                font-size:11px;

                font-weight:bold;
            }

            .total{

                text-align:center;

                font-size:34px;

                font-weight:bold;

                margin:18px 0;
            }

            .pagado{

                text-align:center;

                font-size:16px;

                font-weight:bold;

                margin-top:10px;
            }

        </style>

    `;
}


// ==========================================
// TICKET INGRESO
// ==========================================
function generarTicketIngreso(data){

    return `

    <html>

    <head>

        <title>
            Ticket Ingreso
        </title>

        ${generarEstilosTicket()}

    </head>

    <body>

        ${generarHeaderTicket()}

        <div class="linea"></div>

        <div class="titulo">

            RECIBO DE INGRESO

        </div>

        <div class="ticket">

            #${String(data.ticket).padStart(6, "0")}

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
                ${data.tipo}
            </strong>

        </div>

        <div class="dato">

            <span>
                INGRESO:
            </span>

            <strong>
                ${data.hora}
            </strong>

        </div>

        <div class="linea"></div>

        <div class="barcode">

            <svg id="barcode"></svg>

        </div>

        <div class="mensaje">

            CONSERVE SU TICKET

        </div>

        ${generarTerminos()}

        <div class="linea"></div>

        <div class="footer">

            ¡Gracias por preferirnos!

        </div>

    </body>

    </html>

    `;
}


// ==========================================
// TICKET SALIDA
// ==========================================
function generarTicketSalida(data){

    return `

    <html>

    <head>

        <title>
            Ticket Salida
        </title>

        ${generarEstilosTicket()}

    </head>

    <body>

        ${generarHeaderTicket()}

        <div class="linea"></div>

        <!-- TITULO -->
        <div class="titulo">

            RECIBO DE SALIDA

        </div>

        <!-- TICKET -->
        <div class="ticket">

            #${String(data.ticket).padStart(6, "0")}

        </div>

        <div class="linea"></div>

        <!-- DATOS -->
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
                ${data.tipo}
            </strong>

        </div>

        <div class="dato">

            <span>
                INGRESO:
            </span>

            <strong>
                ${data.hora_ingreso}
            </strong>

        </div>

        <div class="dato">

            <span>
                SALIDA:
            </span>

            <strong>
                ${data.hora_salida}
            </strong>

        </div>

        <div class="dato">

            <span>
                TIEMPO:
            </span>

            <strong>
                ${data.tiempo}
            </strong>

        </div>

        <div class="linea"></div>

        <!-- TOTAL -->
        <div class="total">

            $ ${data.valor}

        </div>

        <!-- PAGADO -->
        <div class="pagado">

            ✓ PAGO REALIZADO

        </div>

        <div class="linea"></div>

        <!-- FOOTER -->
        <div class="footer">

            ¡Gracias por su visita!

        </div>

    </body>

    </html>

    `;
}