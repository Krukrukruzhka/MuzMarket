const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");
signupBtn.onclick = () => {
  loginForm.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
};
loginBtn.onclick = () => {
  loginForm.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
};
signupLink.onclick = () => {
  signupBtn.click();
  return false;
};


// Get the modal
var modal = document.getElementById('id01');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

btn_login.onclick = function() {
//    const xhr = new XMLHttpRequest();
//    xhr.open("POST", "http://127.0.0.1:8000/auth/login");
//    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded"; "charset=UTF-8");
//    const body = JSON.stringify({
//        "grant_type": null,
//        "username": email_login.value,
//        "password": password_login.value,
//        "scope": null,
//        "client_id": null,
//        "client_secret": null
//    });
//    xhr.onload = () => {
//      if (xhr.readyState == 4 && xhr.status == 201) {
//        console.log(JSON.parse(xhr.responseText));
//      } else {
//        console.log(`Error: ${xhr.status}`);
//      }
//    };
//    xhr.send(body);
    var xhr = new XMLHttpRequest();
    var body = 'grant_type=&username=' + encodeURIComponent(email_login.value) +
        '&password=' + encodeURIComponent(password_login.value) +
        '&scope=&client_id=&client_secret=';

    xhr.open("POST", 'http://127.0.0.1:8000/auth/login', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

//    xhr.onreadystatechange = ...;

    xhr.send(body);
};

btn_signup.onclick = function() {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8000/auth/register");
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    const body = JSON.stringify({
        "email": email_signup.value,
        "password": password_signup.value,
        "is_active": true,
        "is_superuser": false,
        "is_verified": false,
        "firstname": "Имя",
        "role_id": 1,
        "region_id": 20
    });
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 201) {
        console.log(JSON.parse(xhr.responseText));
      } else {
        console.log(`Error: ${xhr.status}`);
      }
    };
    xhr.send(body);
};