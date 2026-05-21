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