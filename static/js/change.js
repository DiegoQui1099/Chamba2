// Manejar el cambio en el número de resultados por página
function updatePerPage() {
    const perPage = document.getElementById('per_page').value;
    const url = new URL(window.location.href);
    url.searchParams.set('per_page', perPage);

    // Actualizar la URL sin recargar la página
    fetch(url.toString())
        .then(response => response.text())
        .then(html => {
            // Crear un nuevo elemento DOM para contener la respuesta
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // Obtener solo el contenido de resultados del documento cargado
            const newResults = doc.querySelector('#contenedor-resultados').innerHTML;

            // Actualizar el contenedor de resultados con la nueva información
            document.querySelector('#contenedor-resultados').innerHTML = newResults;
        })
        .catch(error => console.error('Error:', error));
}
