let timeoutId;
function filterVerseSelections() {
    clearTimeout(timeoutId);  // Clear the previous timeout
    timeoutId = setTimeout(() => {
        const searchQuery = document.getElementById('searchBox').value;
        const url = `?q=${encodeURIComponent(searchQuery)}`;
        fetch(url)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                document.getElementById('vs_list').innerHTML = doc.getElementById('vs_list').innerHTML;
                document.getElementById('pagination').innerHTML = doc.getElementById('pagination').innerHTML;
            })
            .catch(error => console.error('Error fetching filtered results:', error));
    }, 300);  // Delay of 300ms
}
