$(document).ready(function () {

    /* How to hide flash message after few seconds? (no date) 
    Stack Overflow. Available at: 
    https://stackoverflow.com/questions/31176402/how-to-hide-flash-message-after-few-seconds 
    (Accessed: 27 October 2024). */
    // Delay and fade out the flash message
    $("#flash-message").delay(4000).slideUp(200, function() {
    $(this).remove();
    });

    // Get the CSRF token from the meta tag
    var csrf_token = $('meta[name=csrf-token]').attr('content');

    // Configure AJAX setup for CSRF token
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    // Handle click on increment button
    $("a.increment-btn").on("click", function () {
        var item_id = $(this).attr('id'); // Get the item ID
        updateQuantity(item_id, 'increment');
    });

    // Handle click on decrement button
    $("a.decrement-btn").on("click", function () {
        var item_id = $(this).attr('id'); // Get the item ID
        updateQuantity(item_id, 'decrement');
    });

    // Handle quantity change on saree details page
    $(document).on("click", "#increment-btn, #decrement-btn", function (e) {
        e.preventDefault();
        var quantityInput = $("#quantity"); // Input field for quantity
        var max = parseInt(quantityInput.attr("max")); // Maximum stock
        var quantity = parseInt(quantityInput.val()); // Current quantity
        if ($(this).attr("id") === "increment-btn" && quantity < max) {
            quantityInput.val(quantity + 1); // Increment quantity
        } else if ($(this).attr("id") === "decrement-btn" && quantity > 1) {
            quantityInput.val(quantity - 1); // Decrement quantity
        }
    });

    // Function to send the AJAX request
    function updateQuantity(item_id, action) {
        $.ajax({
            url: '/update-quantity', // Endpoint for updating quantity
            type: 'POST',
            data: JSON.stringify({ item_id: item_id, action: action }), // Send item ID and action
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (response) {
                if (response.status === 'OK') {
                    // Update the quantity and total dynamically in the shopping cart page
                    $("#quantity-" + item_id).text(response.new_quantity);
                    $("#cart-total").text("Total: £" + response.new_total);
                    $("#subtotal-" + item_id).text("£" + response.new_subtotal);

                    // Dynamically update the subtotal for the corresponding item in the cart modal
                    $("#modal-quantity-" + item_id).text(response.new_quantity);
                    // Update the total in the cart modal
                    $("#modal-cart-total").text("Total: £" + response.new_total);
                } else {
                    alert('Error updating quantity: ' + response.message);
                }
            },
            error: function (error) {
                console.log(error);
                alert('An error occurred while updating the cart.');
            }
        });
    }

    
});


// Cookie Consent Initialization
window.addEventListener("load", function () {
    window.cookieconsent.initialise({
        palette: {
            popup: {
                background: "#eaf7f7",
                text: "#5c7291",
            },
            button: {
                background: "#c7182f",
                text: "#ffffff",
            },
        },
        content: {
            message: "This website uses cookies to ensure you get the best experience on our website.",
            dismiss: "Got it!",
            link: "Learn more",
            href: "/privacy-policy", // Link to your privacy policy
        },
        cookie: {
            expiryDays: 365, // Number of days until the cookie expires
        },
    });
});
