function abrirEditar(boton) {

    const id = boton.dataset.id;

    console.log("Editar usuario:", id);

    // Aquí posteriormente abriremos el modal de edición
}


function abrirMovimientos(boton) {

    const id = boton.dataset.id;
    const nombre = boton.dataset.nombre;
    const puntos = boton.dataset.puntos;

    console.log("Usuario:", nombre);
    console.log("ID:", id);
    console.log("Puntos:", puntos);

    // Aquí posteriormente abriremos el modal de movimientos
}


function cerrarEditar() {

    console.log("Cerrar edición");
}


function cerrarMovimientos() {

    console.log("Cerrar movimientos");
}