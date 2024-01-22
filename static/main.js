// Function to update the total price of a product based on its quantity and unit price.
function updateTotalPrice(productId) {
    let pricePerUnit = parseFloat(document.getElementById('price-'+productId).getAttribute('data-price-per-unit'));
    let quantity = parseInt(document.getElementById('quantity-'+productId).value);
    let totalPrice = pricePerUnit * quantity;
    document.getElementById('price-'+productId).innerText = totalPrice.toFixed(2);
    localStorage.setItem('quantity-'+productId , quantity);
}

// Function to check for updates in the quantities of products and update the total price accordingly.
function checkForUpdates() {
    let productIds = [1,2,3,4,5,6,7,8,9,10,11,12]; 
    productIds.forEach(function(productId) {
        let savedQuantity = localStorage.getItem('quantity-' + productId);
        let quantityElement = document.getElementById('quantity-' + productId);
        if (savedQuantity && quantityElement && quantityElement.value !== savedQuantity) {
            quantityElement.value = savedQuantity;
            updateTotalPrice(productId);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
     // Check for updates in product quantities and prices when the page loads.
    checkForUpdates();
    setInterval(checkForUpdates, 1000); 
});

// Event listener for when the DOM content is fully loaded.
document.addEventListener('DOMContentLoaded', () => {
    let dropdownMenu = document.getElementById('dropdown-menu');
    let toggleMenu = document.getElementById('toggle-menu');

    dropdownMenu.addEventListener('click', ()=> toggleMenu.classList.toggle('opened'));
});





