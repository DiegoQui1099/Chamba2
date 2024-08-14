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

function updatePerPage() {
    const perPage = document.getElementById('per_page').value;
    const url = new URL(window.location.href);
    url.searchParams.set('per_page', perPage);
    window.location.href = url.toString();
};

function searchResults() {
    const input = document.getElementById('search');
    const filter = input.value.toLowerCase();
    const table = document.getElementById('consulta');
    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName('td');
        let found = false;

        for (let j = 0; j < cells.length; j++) {
            const cell = cells[j];
            if (cell.textContent.toLowerCase().indexOf(filter) > -1) {
                found = true;
                break;
            }
        }

        if (found) {
            rows[i].style.display = '';
        } else {
            rows[i].style.display = 'none';
        }
    }
}