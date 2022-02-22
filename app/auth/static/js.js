if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+ ...
    xhr = new XMLHttpRequest();
} else if (window.ActiveXObject) { // IE 6 and older
    xhr = new ActiveXObject("Microsoft.XMLHTTP");
}

if (!xhr) {
    alert('Giving up :( Cannot create an XMLHTTP instance');
}

//  (function() {
//  var httpRequest;
//  document.getElementById("submit").addEventListener('click', makeRequest);
err_block = document.getElementById("error");


function makeRequest() {
    let email = document.getElementById("email").value
    let password = document.getElementById("password").value
    console.log('Fetching updated data.');
    xhr.open("POST", "/api/v1/accounts/session", true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    xhr.onload = function() {
        Login(xhr.status, xhr.response);
    }
    let body = JSON.stringify({"email": email, "password": password})
//    let body = {"email": email, "password": password}
    console.log(body)
    console.log(typeof(body))
    err_block.innerHTML = ""
    xhr.send(body);
}

function Login(status, response){
    console.log(status, JSON.parse(response));
    if (status === 400) {
//        alert(response);
        JSON.parse(response).msg.forEach((err) => {
            console.log(err);
            err_block.innerText += err.msg
            err_block.appendChild(document.createElement("br"))
        })
    } else if (status === 200) {
        console.log("LOGGED IN!")
    }
}