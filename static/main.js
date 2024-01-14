
function updateTotalPrice(productId) {
    let pricePerUnit = document.getElementById('price-'+productId).getAttribute('data-price-per-unit');
    let quantity = document.getElementById('quantity-'+productId).value;
    let totalPrice = pricePerUnit * quantity;
    document.getElementById('price-'+productId).innerText = 'Total price: ' + totalPrice.toFixed(2);
}
