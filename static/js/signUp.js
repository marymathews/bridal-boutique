$(document).ready(function() {
    $("#submit").click(function(event) {
        if(!isEmailValid($("#email").val())) {
            event.preventDefault();
            $("#email-validation").css({
                'color': 'red'
            });
        }
        if(!isPasswordValid($("#password").val())) {
            event.preventDefault();
            $("#pwd-validation").css({
                'color': 'red'
            });
        }
    });

    $("#email").focus(function() {
        $("#email-validation").show();
    });

    $("#email").blur(function() {
        $("#email-validation").hide();
    });

    $("#password").focus(function() {
        $("#pwd-validation").show();
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

function isPasswordValid(pwd) {
    console.log(pwd)
    //minimum 6, maximum 30; at least one uppercase, at least one lowercase, at least one digit
    var pwdRegex = /(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{6,30}/;
    if(pwdRegex.test(pwd))
        return true;
    return false;
}