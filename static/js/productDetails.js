$(document).ready(function() {
    $(".flexslider").flexslider();

    var isLoggedIn = false;
    $.get({
        url: '/checkSignedIn',
        dataType: 'JSON',
        success: function(response) {
            $.each(response, function(key, value) {
                if(value == 'Logged In') {
                    isLoggedIn = true;
                    $("#logout").show();
                    $("#profile").attr('href', '/userProfile');
                    $("#wishlist").attr('href', '#');
                    $("#show-wishlist").attr('href', '/wishlist')
                }
                else {
                    isLoggedIn = false;
                    $("#logout").hide();
                    $("#profile").attr('href', '/signInPage');
                    $("#wishlist").attr('href', '/signInPage');
                    $("#show-wishlist").attr('href', '/signInPage')
                }
            })
        }
    });

    $("#wishlist").click(function() {
        if(isLoggedIn) {
            $.ajax({
                url: '/wishlist',
                type: 'PUT',
                dataType: 'json',
                data: {item_id: $(this).parent().attr('id')},
                success: function(response) {
                    $.each(response, function(key, value) {
                        if(key == 'error' && value == 'Item not added') {
                            Swal.fire("Something went wrong!", "", "error");                
                        }
                        else {
                            Swal.fire("Item Added to Wishlist!", "", "success");
                        }
                    });
                },
                error: function(error) {
                    Swal.fire("This item is already in your wishlist!", "", "error");                
                }
            });
        }
    });
})