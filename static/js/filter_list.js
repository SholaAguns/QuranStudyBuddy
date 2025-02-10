document.getElementById('searchBox').addEventListener('input', function () {
    const searchQuery = this.value.toLowerCase(); // Get the search query
    const searchItems = document.querySelectorAll('.search-item'); // Get all phrase items

    searchItems.forEach(function (item) {
        const searchText = item.querySelector('a').textContent.toLowerCase(); // Get the phrase text
        if (searchText.includes(searchQuery)) {
            item.style.display = ''; // Show the item if it matches the query
        } else {
            item.style.display = 'none'; // Hide the item if it doesn't match
        }
    });
});
