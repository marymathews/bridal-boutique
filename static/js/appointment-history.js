$(document).ready(function() {
    $("#logout").show();
    
    if($(".wishlist-container li").length == 0) {
        $("h3").show();
    }
    else {
        $("h3").hide();
    }
})