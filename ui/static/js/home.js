document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchForm').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission
        var searchTerm = document.getElementById('keyword').value.trim();
        if (searchTerm !== '') {
            // Fetch search results using AJAX
            fetchSearchResults(searchTerm);
        }
    });
});

function fetchSearchResults(keyword) {
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keyword: keyword }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Debugging: Check if data is received correctly
        // Update the right content with search results
        updateSearchResults(data);
    })
    .catch(error => console.error('Error:', error));
}

function updateSearchResults(data) {
    var searchResults = document.getElementById('rightContent');
    searchResults.innerHTML = ''; // Clear existing search results

    // Create and append list items for each search result
    if (data.length > 0) {
        var ul = document.createElement('ul');
        data.forEach(function (paper) {
            var li = document.createElement('li');
            li.textContent = paper.category + ' - ' + paper.title;
            ul.appendChild(li);
        });
        searchResults.appendChild(ul);

        // Show the right content
        searchResults.style.display = 'block';
    } else {
        // No results message
        searchResults.textContent = 'No results found.';
        searchResults.style.display = 'block';
    }
}
