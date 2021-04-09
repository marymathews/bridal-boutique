$(document).ready(function() {
    $("#submit").click(function(event) {
        if(!isEmailValid($("#email").val())) {
            event.preventDefault();
            //todo show email is not valid error
        }
        if(!isPasswordValid($("#password").val())) {
            event.preventDefault();
            //todo show password is not strong enough error
        }
    });
})

function isEmailValid(email) {
    var emailRegex = new RegExp('^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$i');
    if(emailRegex.test(email))
        return true;
    return false;
}

function isPasswordValid(pwd) {
    //minimum 6, maximum 30; at least one uppercase, at least one lowercase, at least one digit, at least one special character
    var pwdRegex = new RegExp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,30}$');
    if(pwdRegex.test(pwd))
        return true;
    return false;
}