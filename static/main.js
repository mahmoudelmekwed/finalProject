function updateTotalPrice(productId) {
    let pricePerUnit = parseFloat(document.getElementById('price-'+productId).getAttribute('data-price-per-unit'));
    let quantity = parseInt(document.getElementById('quantity-'+productId).value);
    let totalPrice = pricePerUnit * quantity;
    document.getElementById('price-'+productId).innerText = totalPrice.toFixed(2);
    localStorage.setItem('quantity-'+productId , quantity);
}


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
    checkForUpdates();
    setInterval(checkForUpdates, 1000); 
});

/////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////

document.addEventListener('DOMContentLoaded', () => {
    let dropdownMenu = document.getElementById('dropdown-menu');
    let toggleMenu = document.getElementById('toggle-menu');

    dropdownMenu.addEventListener('click', ()=> toggleMenu.classList.toggle('opened'));
});

//  //////////////////////////////////////////////////////////////////////////////

// $(document).ready(() => {
//     // Initially disable the submit button
//     $('#registerForm button[type="submit"]').prop('disabled', true);

//     // Event listener for email input
//     $('#emailField').on('input', function() {
//         let email = $(this).val();
//         $.ajax({
//             url: '/check-email',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({email: email}),
//             success: function(response) {
//                 if(response.exists) {
//                     $('#emailError').text('Email already in use.');
//                     $('#registerForm button[type="submit"]').prop('disabled', true);
//                 } else {
//                     $('#emailError').text('');
//                     $('#registerForm button[type="submit"]').prop('disabled', false);
//                 }
//             }
//         });
//     });

    // Form submission event listener
    // document.getElementById('registerForm').addEventListener('submit', (event) => {
    //     let password = document.getElementById('password').value;
    //     let errors = [];

    //     // Password validation
    //     if (password.length < 8) {
    //         errors.push("Password must be at least 8 characters long.");
    //     }
    //     if (!password.match(/[A-Z]/)) {
    //         errors.push("Password must contain at least one uppercase letter.");
    //     }
    //     if (!password.match(/[a-z]/)) {
    //         errors.push("Password must contain at least one lowercase letter.");
    //     }
    //     if (!password.match(/[0-9]/)) {
    //         errors.push("Password must contain at least one digit.");
    //     }
    //     if (!password.match(/[^a-zA-Z0-9]/)) {
    //         errors.push("Password must contain at least one special character.");
    //     }

    //     // Display errors
    //     if (errors.length > 0) {
    //         document.getElementById('passwordError').innerHTML = errors.join("<br>");
    //         event.preventDefault();
    //     }
    //     // If no errors, the form will submit normally
    // });



/////////////////////////////////////////////////////////////////////////////////////////////////////////////

// document.getElementById('registerForm').addEventListener('submit', (event) => {
//     let password = document.getElementById('password').value;
//     let errors = [];

//     if (password.length < 8) {
//         errors.push("Password must be at least 8 characters long.");
//     }
//     if (!password.match(/[A-Z]/)) {
//         errors.push("Password must contain at least one uppercase letter.");
//     }
//     if (!password.match(/[a-z]/)) {
//         errors.push("Password must contain at least one lowercase letter.");
//     }
//     if (!password.match(/[0-9]/)) {
//         errors.push("Password must contain at least one digit.");
//     }
//     if (!password.match(/[^a-zA-Z0-9]/)) {
//         errors.push("Password must contain at least one special character.");
//     }
//     // if (!isEmailValid) {
//     //     errors.push("The entered email is already in use. Please use a different email.");
//     // }

//     if (errors.length > 0) {
//         document.getElementById('passwordError').innerHTML = errors.join("<br>");
//         event.preventDefault();
//     }
// });

// $(document).ready(() => {
//     $('#emailField').on('input', function() {
//         let email = $(this).val();
//         $.ajax({
//             url: '/check-email',
//             type: 'POST',
//             contentType: 'application/json',
//             data: JSON.stringify({email: email}),
//             success: function(response) {
//                 if(response.exists) {
//                     $('#emailError').text('Email already in use.');
//                 } else {
//                     $('#emailError').text('');
//                 }
//             }
//         });
//     });
// });

/////////////////////////////////////////////////////////////////////////////



// dropdown_menu.onClick = function(){
//     toggle_menu.classList.toggle('opened')
// }

// let dropdown_menu = document.getElementById('dropdown-menu');
// let toggle_menu = document.getElementById('toggle-menu');

// dropdown_menu.addEventListener('click', ()=>{
//     toggle_menu.classList.toggle("opened");
// })



/////////////////////////////////////////////////////////////




