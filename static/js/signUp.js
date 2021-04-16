$(document).ready(function() {
    $("#submit").click(function(event) {
        if(!isEmailValid($("#email").val())) {
            event.preventDefault();
            console.log("Invalid email");
            //todo show email is not valid error
        }
        if(!isPasswordValid($("#password").val())) {
            event.preventDefault();
            console.log("Invalid password")
            //todo show password is not strong enough error
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
    //minimum 6, maximum 30; at least one uppercase, at least one lowercase, at least one digit, at least one special character
    var pwdRegex = new RegExp('^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[*.!@$%^&(){}[]:;<>,.?/~_+-=|\]).{6,30}$');
    if(pwdRegex.test(pwd))
        return true;
    return false;
}