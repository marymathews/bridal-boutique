$(document).ready(function() {
    let data = [];
    var apptInfo = new Map();
    var selectedDate;
    var selectedTime;

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
        $('.modal-body p').remove();
        $('.modal-body form').empty();
        selectedDate = null;
        selectedTime = null;

        let result = getItems(data); 
        if(result.flag == 0) {
            if(data.length == 0)
                Swal.fire("No items selected!", "", "error");
            else {
                apptInfo.clear();
                $('.modal-body').append("<p>Total Price of Selected Items: &#36; " + result.totalPrice.toFixed(2) + "</p>"); 
                $.ajax({
                    url: '/getDates',
                    type: 'GET',
                    dataType: 'json',
                    success: function(response) {
                        $.each(response, function(key, value) {
                            if(key == 'error' && value == 'No appointments available') {
                                $('.modal-body #date-container form').append('<p>No appointments are available currently! Please try again later.</p>');
                            }
                            else {
                                apptInfo.set(key, value);
                                key = key.split("-").reverse().join("/");
                                $('.modal-body #date-container form').append('\
                                <div class="form-check my-1">\
                                    <input class="form-check-input dates" type="radio" name="flexRadioDefault id="' + key + '">\
                                    <label class="form-check-label for="' + key + '">\
                                    ' + key + '\
                                    </label>\
                                </div>');
                            }
                        });
                        $('.modal-body #date-container form').append('<hr>');
                        $('#date-modal').modal('show');
                    },
                    error: function(response) {
                        Swal.fire("Something Went Wrong!", "Please try again later.");
                    }
                }); 
            }
        }
        else {
            Swal.fire("Invalid item quantity entered!", "", "error");
        }
    });

    $(".modal-body #date-container form").on('click', '.dates', function() {
        $(".times").remove();
        date = $(this).siblings().text().trim();
        date = date.split("/").reverse().join("-");
        times = apptInfo.get(date);
        selectedDate = date;
        selectedTime = null;
        $.each(times, function(key, value) {
            if(value == 10) {
                $('.modal-body #time-container form').append('\
                    <div class="form-check my-1 times">\
                        <input class="form-check-input" type="radio" name="flexRadioDefault id="' + value + '">\
                        <label class="form-check-label for="' + value + '">\
                        ' + value + ' AM\
                        </label>\
                    </div>'
                );
            }
            else {
                $('.modal-body #time-container form').append('\
                    <div class="form-check my-1 times">\
                        <input class="form-check-input" type="radio" name="flexRadioDefault id="' + value + '">\
                        <label class="form-check-label for="' + value + '">\
                        ' + value + ' PM\
                        </label>\
                    </div>'
                );
            }
            if(key == times.length - 1)
                $('.modal-body #time-container form').append('<hr class="times">');
        });
    });

    $(".modal-body #time-container form").on('click', '.times input', function() {
        selectedTime = $(this).siblings().text().trim().split(" ")[0];
    });

    $("#confirm-selections").click(function() {
        if(selectedDate == null || selectedTime == null)
            Swal.fire("Please select a date and time!");
        else {
            let obj = {"date": selectedDate, "time": selectedTime};
            data.push(obj);
            $('#date-modal').modal('hide');
            $.post({
                url: '/bookAppointment',
                dataType: 'json',
                data: JSON.stringify(data),
                success: function(response) {
                    $.each(response, function(key, _) {
                        if(key == 'error')
                            Swal.fire("Something Went Wrong!", "Please try again later.");
                        else {
                            Swal.fire("Your appointment has been booked!", "", "success");
                        }
                    });
                },
                error: function(error) {
                    Swal.fire("Something Went Wrong!", "Please try again later.");
                }
            });
        }
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
    let totalPrice = 0.0;
    let flag = 0;
    data.length = 0;
    $(".wishlist-container").children().each(function() {
        let item_id = $(this).find(".remove-wishlist").attr("id");
        let item_price = parseFloat($(this).find(".wishlist-cost").text().split(" ")[1]);
        $(this).find("table").find("tr").each(function() {
            let item_size = $(this).find(".size").text();
            let item_qty = -1;
            let max_item_qty = -1;
            if($(this).find("input").length && $(this).find("input").is(':visible')) {
                item_qty = parseInt($(this).find("input").val());
                max_item_qty = parseInt($(this).find("input").attr('max'));
            }
            if(item_qty <= max_item_qty && item_qty > 0) {
                let obj = {"item_id": item_id, "item_price": item_price, "item_size": item_size, "item_qty": item_qty};
                totalPrice += item_qty * item_price;
                data.push(obj);
            }
            else if(item_qty != -1 && max_item_qty != -1) {
                flag = 1;
            }
        });
    });
    return {totalPrice, flag};
}