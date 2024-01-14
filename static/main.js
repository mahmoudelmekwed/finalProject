
function updateTotalPrice(productId) {
    let pricePerUnit = document.getElementById('price-'+productId).getAttribute('data-price-per-unit');
    let quantity = document.getElementById('quantity-'+productId).value;
    localStorage.setItem('quantity-'+productId , quantity);
    let totalPrice = pricePerUnit * quantity;
    document.getElementById('price-'+productId).innerText = 'Total price: ' + totalPrice.toFixed(2);
}

function onChangeQuantity(productId){
    let quantity = document.getElementById('quantity-'+productId).value;
    localStorage.setItem('quantity-'+productId , quantity);
    updateTotalPrice(productId);
}

document.addEventListener('DOMContentLoaded', function() {
    var productIds = [1,2,3,4,5,6,7,8,9];
    productIds.forEach(function(productId) {
        var savedQuantity = localStorage.getItem('quantity-' + productId);
        if (savedQuantity) {
            var quantityElement = document.getElementById('quantity-' + productId);
            if (quantityElement) {
                quantityElement.value = savedQuantity;
            }
        }
    });
});
