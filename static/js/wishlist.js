$(document).ready(function() {
    $("#logout").show();
    
    if($(".wishlist-container li").length == 0)
        $("h3").show();
    else
        $("h3").hide();

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
                    if($(".wishlist-container li").length == 0)
                        $("h3").show();
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