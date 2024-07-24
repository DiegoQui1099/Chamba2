$(document).ready(function() {
    $('#tipo_busqueda').on('change', function() {
        var tipoBusqueda = $(this).val();

        // Habilitar todos los campos primero y quitar estilos de deshabilitado
        $('.bloque-formulario input, .bloque-formulario select').prop('disabled', false);
        $('.bloque-formulario').removeClass('deshabilitado');

        // Limpiar los valores de los campos relevantes según el tipo de búsqueda seleccionado
        if (tipoBusqueda === 'apellidos_nombres') {
            $('#serial_registro_civil').val('');
            $('#numero_identificacion').val('');
        } else if (tipoBusqueda === 'numero_identificacion') {
            $('#primer_apellido').val('');
            $('#segundo_apellido').val('');
            $('#primer_nombre').val('');
            $('#segundo_nombre').val('');
            $('#sexo').val('');
            $('#fecha_nacimiento').val('');
        } else if (tipoBusqueda === 'serial') {
            $('#numero_identificacion').val('');
            $('#primer_apellido').val('');
            $('#segundo_apellido').val('');
            $('#primer_nombre').val('');
            $('#segundo_nombre').val('');
            $('#sexo').val('');
            $('#fecha_nacimiento').val('');
        } else if (tipoBusqueda === 'todos_criterios') {
            $('#serial_registro_civil').val('');
        }

        // Deshabilitar los campos relevantes según el tipo de búsqueda seleccionado
        if (tipoBusqueda === 'apellidos_nombres') {
            $('#serial_registro_civil').closest('.bloque-formulario').addClass('deshabilitado');
            $('#serial_registro_civil').prop('disabled', true);
            $('#numero_identificacion').closest('.bloque-formulario').addClass('deshabilitado');
            $('#numero_identificacion').prop('disabled', true);
        } else if (tipoBusqueda === 'numero_identificacion') {
            $('#serial_registro_civil').closest('.bloque-formulario').addClass('deshabilitado');
            $('#serial_registro_civil').prop('disabled', true);
            $('#primer_apellido').closest('.bloque-formulario').addClass('deshabilitado');
            $('#primer_apellido').prop('disabled', true);
            $('#segundo_apellido').closest('.bloque-formulario').addClass('deshabilitado');
            $('#segundo_apellido').prop('disabled', true);
            $('#primer_nombre').closest('.bloque-formulario').addClass('deshabilitado');
            $('#primer_nombre').prop('disabled', true);
            $('#segundo_nombre').closest('.bloque-formulario').addClass('deshabilitado');
            $('#segundo_nombre').prop('disabled', true);
            $('#sexo').closest('.bloque-formulario').addClass('deshabilitado');
            $('#sexo').prop('disabled', true);
            $('#fecha_nacimiento').closest('.bloque-formulario').addClass('deshabilitado');
            $('#fecha_nacimiento').prop('disabled', true);
        } else if (tipoBusqueda === 'serial') {
            $('#numero_identificacion').closest('.bloque-formulario').addClass('deshabilitado');
            $('#numero_identificacion').prop('disabled', true);
            $('#primer_apellido').closest('.bloque-formulario').addClass('deshabilitado');
            $('#primer_apellido').prop('disabled', true);
            $('#segundo_apellido').closest('.bloque-formulario').addClass('deshabilitado');
            $('#segundo_apellido').prop('disabled', true);
            $('#primer_nombre').closest('.bloque-formulario').addClass('deshabilitado');
            $('#primer_nombre').prop('disabled', true);
            $('#segundo_nombre').closest('.bloque-formulario').addClass('deshabilitado');
            $('#segundo_nombre').prop('disabled', true);
            $('#sexo').closest('.bloque-formulario').addClass('deshabilitado');
            $('#sexo').prop('disabled', true);
            $('#fecha_nacimiento').closest('.bloque-formulario').addClass('deshabilitado');
            $('#fecha_nacimiento').prop('disabled', true);
        } else if (tipoBusqueda === 'todos_criterios') {
            $('#serial_registro_civil').closest('.bloque-formulario').addClass('deshabilitado');
            $('#serial_registro_civil').prop('disabled', true);
        }
    });

    // Al cargar la página, simular el cambio para aplicar la lógica inicialmente
    $('#tipo_busqueda').change();
});


//Funcion para la fecha 
$(document).ready(function() {
    // Función para obtener el rango de años desde 1800 hasta el año actual
    function obtenerRangoAnios() {
        var fechaActual = new Date();
        var anioActual = fechaActual.getFullYear();
        var anioMinimo = 1800; // Año mínimo permitido

        var rangoAnios = [];
        for (var i = anioActual; i >= anioMinimo; i--) {
            rangoAnios.push(i);
        }
        return rangoAnios;
    }

    // Configuración del Datepicker
    $('#fecha_nacimiento').datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true,
        showButtonPanel: true,
        yearRange: '1800:' + new Date().getFullYear(), // Establecer el rango de años
        onSelect: function(dateText, inst) {
            // Al seleccionar una fecha, actualizar el valor del input
            $(this).val(dateText);
        }
    });

    // Mostrar el calendario al hacer clic en el input de fecha
    $('#fecha_nacimiento').on('click', function() {
        $('#fecha_nacimiento').datepicker('show');
    });
});

$(document).ready(function() {
    // Evento al hacer clic en el botón de enviar
    $('#btnEnviar').on('click', function() {
        var tipoBusqueda = $('#tipo_busqueda').val();
        var camposValidos = true;
        var mensajeError = '';

        // Validar campos según el tipo de búsqueda seleccionado
        if (tipoBusqueda === 'apellidos_nombres') {
            // Validar que los campos de apellidos y nombres estén llenos
            if ($('#primer_apellido').val() === '' || $('#primer_nombre').val() === '') {
                camposValidos = false;
                mensajeError = 'Debe ingresar el primer apellido y el primer nombre.';
            }
        } else if (tipoBusqueda === 'numero_identificacion') {
            // Validar que el número de identificación esté lleno
            if ($('#numero_identificacion').val() === '') {
                camposValidos = false;
                mensajeError = 'Debe ingresar el número de identificación.';
            }
        } else if (tipoBusqueda === 'serial') {
            // Validar que el serial esté lleno
            if ($('#serial_registro_civil').val() === '') {
                camposValidos = false;
                mensajeError = 'Debe ingresar el serial.';
            }
        } else if (tipoBusqueda === 'todos_criterios') {
            // Validar que todos los campos relevantes estén llenos
            if ($('#primer_apellido').val() === '' || $('#primer_nombre').val() === ''
                || $('#numero_identificacion').val() === '' || $('#fecha_nacimiento').val() === '') {
                camposValidos = false;
                mensajeError = 'Debe llenar todos los campos obligatorios.';
            }
        }

        // Mostrar mensaje de error si los campos no son válidos
        if (!camposValidos) {
            // Aquí puedes redirigir a una página de error.html o mostrar un mensaje en pantalla
            alert(mensajeError);
            // Opcional: redirigir a una página de error.html
            // window.location.href = 'error.html';
        } else {
            // Aquí puedes enviar el formulario o hacer cualquier otra acción si todos los campos son válidos
            // Por ejemplo, enviar el formulario usando AJAX
            alert('Formulario válido. Enviar datos.');
        }
    });
});
