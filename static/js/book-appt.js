$(document).ready(function() {
    $("#logout").show();

    $(".quantity").hide();
    $(".delete").hide();

    if($(".wishlist-container li").length == 0) {
        $(".book-appointment").hide();
    }
    else {
        $(".book-appointment").show();
    }

    $(".size").click(function() {
        $(this).parent().siblings().show();
    });

    $(".delete").click(function() {
        $(this).siblings(".quantity").hide();
        $(this).hide();
    });
    
    var currentItem;
    $(".remove-wishlist").click(function() {
        currentItem = $(this);
        deleteItem($(this).attr('id'), currentItem)
    });
})

function deleteItem(id, currentItem) {
    $.ajax({
        url: '/deleteFromWishlist/' + id,
        type: 'DELETE',
        dataType: 'json',
        success: function(response) {
            $.each(response, function(key, value) {
                if(key == 'success' && value == 'Deleted') {
                    $(currentItem).parent().parent().remove();
                    if($(".wishlist-container li").length == 0) {
                        $(".book-appointment").hide();
                    }
                }
            });
        },
        error: function(error) {
            $.each(response, function(key, value) {
                if(key == 'error') {
                    Swal.fire("Something went wrong!", "", "error");
                }
            });
        }
    });
}