function updateTotalPrice(productId) {
    let pricePerUnit = parseFloat(document.getElementById('price-'+productId).getAttribute('data-price-per-unit'));
    let quantity = parseInt(document.getElementById('quantity-'+productId).value);
    let totalPrice = pricePerUnit * quantity;
    document.getElementById('price-'+productId).innerText = totalPrice.toFixed(2);
    localStorage.setItem('quantity-'+productId , quantity);
}


function checkForUpdates() {
    let productIds = [1,2,3,4,5,6,7,8,9]; 
    productIds.forEach(function(productId) {
        let savedQuantity = localStorage.getItem('quantity-' + productId);
        let quantityElement = document.getElementById('quantity-' + productId);
        if (savedQuantity && quantityElement && quantityElement.value !== savedQuantity) {
            quantityElement.value = savedQuantity;
            updateTotalPrice(productId);
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    checkForUpdates();
    setInterval(checkForUpdates, 1000); 
});
