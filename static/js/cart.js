var productElement = document.getElementById('product-info');
console.log(productElement);
var productId = productElement.dataset.productId

// JavaScript code to add products to the cart using AJAX
function addToCart(productId) {
    fetch(`/add-to-cart/?product_id=${productId}`)
        .then(response => {
            if (response.ok) {
                console.log('Product added to cart successfully');
                // You can update the cart UI here if needed
            } else {
                console.error('Failed to add product to cart');
            }
        })
        .catch(error => {
            console.error('Error adding product to cart:', error);
        });
        document.activeElement.blur();
}

// Add event listener to the document and use event delegation to handle "Shop now" button clicks
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('add-btn')) {
        const productId = event.target.dataset.productId;
        if (productId) {
            fetch(`/add-to-cart/${productId}/`)
                .then(response => {
                    if (response.ok) {
                        // Handle successful response
                    } else {
                        // Handle error response
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            console.error('Product ID is undefined');
        }
    }
    document.activeElement.blur();
});

function updateCart(itemId, newQuantity) {
    fetch(`/update-cart/?item_id=${itemId}&quantity=${newQuantity}`)
        .then(response => {
            if (response.ok) {
                console.log('Cart updated successfully');
                // You can update the cart UI here if needed
            } else {
                console.error('Failed to update cart');
            }
        })
        .catch(error => {
            console.error('Error updating cart:', error);
        });
}