
function updateTotalPrice(productId) {
    console.log("updateTotalPrice called for product ID:", productId);
    var pricePerUnit = document.getElementById('price-'+productId).innerText;
    var quantity = document.getElementById('quantity-'+productId).value;
    var totalPrice = pricePerUnit * quantity;
    document.getElementById('total_price-'+productId).innerText = totalPrice;
}
