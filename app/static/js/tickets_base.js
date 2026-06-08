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

            @page{

                size:58mm auto;

                margin:0;
            }

            html,
            body{

                width:48mm;

                margin:0;

                padding:1mm;

                font-family:'Courier New', monospace;

                overflow:hidden;
            }

            .center{

                text-align:center;
            }

            .logo{

                width:55px;

                margin-bottom:8px;
            }

            .empresa{

                font-size:13px;

                font-weight:bold;

                margin-bottom:2px;
            }

            .subtitulo{

                font-size:9px;

                margin-bottom:4px;
            }

            .direccion{

                font-size:11px;

                margin-bottom:2px;
            }

            .telefonos{

                font-size:9px;

                margin-bottom:10px;
            }

            .linea{

                border-top:1px dashed #000;

                margin:10px 0;
            }

            .titulo{

                font-size:13px;

                font-weight:bold;

                margin-bottom:12px;

                text-align:center;
            }

            .ticket{

                font-size:20px;

                font-weight:bold;

                text-align:center;

                margin:16px 0;
            }

            .dato{

                margin:4px 0;

                font-size:10px;

                word-wrap:break-word;
            }

            .dato span{

                font-weight:bold;
            }

            .dato strong{

                display:block;

                margin-top:1px;
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

                margin-top:5px;

                text-align:center;

                font-size:11px;

                font-weight:bold;
            }

            .total{

                text-align:center;

                font-size:20px;

                font-weight:bold;

                margin:18px 0;
            }

            .pagado{

                text-align:center;

                font-size:16px;

                font-weight:bold;

                margin-top:10px;
            }

            @media print {

                @page {

                    size: 58mm auto;

                    margin: 0;
                }

                html,
                body {

                    width: 58mm !important;

                    min-height: auto !important;

                    height: auto !important;

                    margin: 0 !important;

                    padding: 2mm !important;

                    overflow: hidden !important;
                }

                .linea:last-of-type {

                    margin-bottom: 0 !important;
                }

                .footer {

                    margin-bottom: 0 !important;

                    padding-bottom: 0 !important;
                }
            }

        </style>

    `;
}