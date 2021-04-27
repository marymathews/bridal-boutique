$(document).ready(function() {
    var isLoggedIn = false;
    $.get({
        url: '/checkSignedIn',
        dataType: 'JSON',
        success: function(response) {
            $.each(response, function(key, value) {
                if(value == 'Logged In') {
                    isLoggedIn = true;
                    $("#logout").show();
                    $("#profile").attr('href', '/showUserProfile');
                    $(".wishlist").attr('href', '#');
                    $("#show-wishlist").attr('href', '/showWishlist');
                }
                else {
                    isLoggedIn = false;
                    $("#logout").hide();
                    $("#profile").attr('href', '/showSignIn');
                    $(".wishlist").attr('href', '/showSignIn');
                    $("#show-wishlist").attr('href', '/showSignIn');
                }
            })
        }
    });
    
    var path = window.location.pathname

    if(path.includes(1)) {
        $("#page-1").addClass("active");
        $("#page-2").removeClass("active");
        $("#page-3").removeClass("active");
    };

    if(path.includes(2)) {
        $("#page-1").removeClass("active");
        $("#page-2").addClass("active");
        $("#page-3").removeClass("active");
    };

    if(path.includes(3)) {
        $("#page-1").removeClass("active");
        $("#page-2").removeClass("active");
        $("#page-3").addClass("active");
    };

    $(".wishlist").click(function() {
        if(isLoggedIn) {
            $.ajax({
                url: '/addToWishlist',
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
});