$(document).ready(function() {
    let data = [];

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

    $("#continue-booking").click(function() {
        getItems(data);
        if(data.length == 0)
            Swal.fire("Please select sizes for all items in your wishlist!", "", "error");
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

function getItems(data) {
    data.length = 0;
    $(".wishlist-container").children().each(function() {
        let item_id = $(this).find(".remove-wishlist").attr("id");
        let item_price = parseFloat($(this).find(".wishlist-cost").text().split(" ")[1]);
        $(this).find("table").find("tr").each(function() {
            let item_size = $(this).find(".size").text();
            let item_qty = 0;
            let max_item_qty = -1;
            if($(this).find("input").length && $(this).find("input").is(':visible')) {
                item_qty = parseInt($(this).find("input").val());
                max_item_qty = parseInt($(this).find("input").attr('max'));
            }
            if(item_qty <= max_item_qty && item_qty > 0) {
                let obj = {"item_id": item_id, "item_price": item_price, "item_size": item_size, "item_qty": item_qty};
                data.push(obj);
            }
        });
    });
}