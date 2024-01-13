
function updateTotalPrice(productId) {
    console.log("updateTotalPrice called for product ID:", productId);
    let pricePerUnit = document.getElementById('price-'+productId).innerText;
    let quantity = document.getElementById('quantity-'+productId).value;
    let totalPrice = pricePerUnit * quantity;
    document.getElementById('total_price-'+productId).innerText = totalPrice;
}
