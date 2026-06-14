// ==========================================
// ABRIR TICKET
// ==========================================
function abrirTicket(html, ticketId){

    const ventana = window.open(
        "",
        "_blank",
        "width=250,height=700"
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
// TERMINOS
// ==========================================
function generarTerminos(){

    return `

        <div class="terminos">

            <p>
                <strong>
                    El ingreso del vehículo implica aceptación de los presentes términos y condiciones.
                </strong>
            </p>

            <p>
                <strong>
                    El vehículo será entregado únicamente al portador del comprobante de ingreso.
                </strong>
            </p>

            <p>
                <strong>
                    No se aceptan reclamaciones posteriores al retiro del vehículo.
                </strong>
            </p>

            <p>
                <strong>
                    El establecimiento no responde por objetos, dinero o documentos dejados dentro del vehículo.
                </strong>
            </p>

            <p>
                <strong>
                    El parqueadero no asume responsabilidad por hurto, incendio, daños causados por terceros o fuerza mayor.
                </strong>
            </p>

            <p>
                <strong>
                    En caso de pérdida del comprobante, la entrega del vehículo solo se realizará con la tarjeta de propiedad.
                </strong>
            </p>

        </div>

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

            <strong>PLACA:</strong>

            <strong>${data.placa}</strong>

        </div>

        <div class="dato">

            <strong>VEHÍCULO:</strong>

            <strong>${data.tipo}</strong>

        </div>

        <div class="dato">

            <strong>INGRESO:</strong>

            <Strong>${data.hora}</strong>

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