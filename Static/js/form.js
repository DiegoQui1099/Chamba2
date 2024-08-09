// Archivo: form.js
 
document.addEventListener('DOMContentLoaded', function() {
    const macroprocesoSelect = document.getElementById('mp');
    const procesoSelect = document.getElementById('p');
 
    // Mapa de procesos relacionados con cada macroproceso
    const procesosRelacionados = {
        'IDE': [
            { id: 'IDE', name: 'Identificación (Tarjeta de Identidad, Cedulación)' },
            { id: 'REG', name: 'Registro Civil' }
        ],
        'ELE': [
            { id: 'CEN', name: 'Censo' },
            { id: 'GEL', name: 'Gestión Electoral' }
        ],
        'Todos': [
            { id: 'XXX', name: 'Todos'}
        ]
    };
 
    macroprocesoSelect.addEventListener('change', function() {
        const selectedMacroproceso = macroprocesoSelect.value;
 
        // Limpiar las opciones anteriores del Proceso
        procesoSelect.innerHTML = '<option value="all">Todos</option>';
 
        // Verificar si el macroproceso seleccionado tiene procesos relacionados
        if (procesosRelacionados[selectedMacroproceso]) {
            procesosRelacionados[selectedMacroproceso].forEach(proceso => {
                const newOption = document.createElement('option');
                newOption.value = proceso.id;
                newOption.text = proceso.name;
                procesoSelect.appendChild(newOption);
            });
        }
    });
 
    // Validación del formulario
    document.getElementById('consultaForm').addEventListener('submit', function(event) {
        let valid = true;
 
        // Validar macroproceso
        if (macroprocesoSelect.value === 'all') {
            alert('Por favor seleccione un Macroproceso');
            valid = false;
        }
 
        // Validar el proceso si es necesario
        if (procesoSelect.value === 'all') {
            alert('Por favor seleccione un Proceso');
            valid = false;
        }
 
        if (!valid) {
            event.preventDefault();
        }
    });
});