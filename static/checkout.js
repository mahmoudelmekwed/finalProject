function storeName() {
    let name = document.getElementById('name').value;
    localStorage.setItem('userName', name); 
}


document.getElementById('confirm').addEventListener('click', function() {
    storeName()
    window.location.href = '/confirmation';
});