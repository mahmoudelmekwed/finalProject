document.addEventListener('DOMContentLoaded', function() {
    let userName = localStorage.getItem('userName');
    if (userName) {
        document.getElementById('thankYouMessage').textContent = 'Thank You, ' + userName + ', for Your Purchase!';
    }
});