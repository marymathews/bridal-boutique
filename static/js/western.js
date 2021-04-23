$(document).ready(function() {
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
});