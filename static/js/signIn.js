$(document).ready(function() {
    $("#submit").click(function(event) {
        if(!isEmailValid($("#email").val())) {
            event.preventDefault();
            $("#email-validation").show().css({
                'color': 'red'
            });
        }
        else {
            if(isPasswordEmpty($("#password").val())) {
                event.preventDefault();
                $("#pwd-validation").show().css({
                    'color': 'red'
                });
            }
        }
    });

    $("#email").blur(function() {
        $("#email-validation").hide();
    });

    $("#password").blur(function() {
        $("#pwd-validation").hide();
    });
})

function isEmailValid(email) {
    var emailRegex = new RegExp('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$');
    if(emailRegex.test(email))
        return true;
    return false;
}

function isPasswordEmpty(pwd) {
    if(pwd == "") 
        return true;
    return false;
}