$(document).ready(function() {
    $("#logout").show();
    
    if($(".wishlist-container li").length == 0) {
        $("h3").show();
        $(".book-appointment").hide();
    }
    else {
        $("h3").hide();
        $(".book-appointment").show();
    }

    var currentItem;
    $(".remove-wishlist").click(function() {
        currentItem = $(this);
        deleteItem($(this).attr('id'), currentItem)
    });
})

function deleteItem(id, currentItem) {
    $.ajax({
        url: '/wishlist/' + id,
        type: 'DELETE',
        dataType: 'json',
        success: function(response) {
            $.each(response, function(key, value) {
                if(key == 'success' && value == 'Deleted') {
                    $(currentItem).parent().parent().remove();
                    if($(".wishlist-container li").length == 0) {
                        $("h3").show();
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