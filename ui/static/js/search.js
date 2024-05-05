function redirectToResults() {
    // Submit the form (necessary for Flask to process the data)
    document.getElementById('search-form').submit();
  
    // Redirect to result.html after form submission
    window.location.href = '/result';
  
    // Prevent default form submission behavior (optional)
    return false;
  }