// Add an event listener for when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the 'userName' value from localStorage
    let userName = localStorage.getItem('userName');

    // Check if 'userName' is not null or undefined
    if (userName) {
        // If 'userName' is available, update the content of the element with the ID 'thankYouMessage'
        document.getElementById('thankYouMessage').textContent = 'Thank You, ' + userName + ', for Your Purchase!';
    }
});
