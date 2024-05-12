function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("main").style.marginLeft = "0";
}

// Toggle the visibility of the search input field, cover, and submit button
function toggleSearchInput() {
    var searchInputContainer = document.getElementById("search-input-container");
    searchInputContainer.classList.toggle("hidden");
}
function ToView(itemContent) {
window.location.href = "/view?item=" + encodeURIComponent(itemContent);
}
function ToSearch() {
    window.location.href = "search";
}



// Perform logout action
function ToLogin() {
    window.location.href="login";
    // Your logout action here, such as redirecting to a logout page
    console.log('Logging out...');
    // For demonstration purposes, let's just alert the user
    alert('Are you sure you want to logout?');
}




