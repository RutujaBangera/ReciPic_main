function validateForm(){
    var fname = document.getElementById("fname").value;
    var lname = document.getElementById("lname").value;
    var password = document.getElementById("password").value;
    var email = document.getElementById("email").value;
    var mobile = document.getElementById("mobile").value;

    if (fname.length < 6 || !/^[a-zA-Z]+$/.test(fname)) {
        alert("First name should contain alphabets and should be at least 6 characters long.");
        return false;
    }   
    if (lname.trim() === "") {
        alert("Last name cannot be empty.");
        return false;
    }
    if (password.length < 6) {
        alert("Password should be at least 6 characters long.");
        return false;
    }
    var email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.test(email)) {
        alert("Invalid email format.");
        return false;
    }
    if (!/^\d{10}$/.test(mobile)) {
        alert("Mobile number should contain 10 digits only.");
        return false;
    }
        return true;
    }