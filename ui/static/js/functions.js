function validatePassword() {
    var password = document.getElementById("psw").value;
    var confirm_password = document.getElementById("confirm").value;

    if (password != confirm_password) {
        alert("Passwords do not match");
        return false;
    }
    return true;
}