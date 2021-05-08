$(document).ready(function() {
    $(".flexslider").flexslider();

    $.get({
        url: '/checkSignedIn',
        dataType: 'JSON',
        success: function(response) {
            $.each(response, function(key, value) {
                if(value == 'Logged In') {
                    $("#logout").show();
                    $("#profile").attr('href', '/userProfile');
                    $("#show-wishlist").attr('href', '/showWishlist');
                }
                else {
                    $("#logout").hide();
                    $("#profile").attr('href', '/signInPage');
                    $("#show-wishlist").attr('href', '/signInPage');
                }
            })
        }
    });
})