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

            ${data.placa}

        </div>

        <div class="dato">

            <strong>VEHÍCULO:</strong>

            ${data.tipo}

        </div>

        <div class="dato">

            <strong>INGRESO:</strong>

            ${data.hora}

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