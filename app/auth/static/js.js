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


function makeRequest(reqType, URL, funcOnLoad, data) {
    console.log(reqType, URL, funcOnLoad, data);
    xhr.open(reqType, URL, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    xhr.onload = function() { funcOnLoad.call(this, xhr.status, xhr.response) }
    xhr.send(data);
}

function handleLogin(status, response){
    console.log(status, JSON.parse(response));
    if (status === 400) {
        JSON.parse(response).msg.forEach((err) => {
            console.log(err);
            err_block.innerText += err.msg
            err_block.appendChild(document.createElement("br"))
        })
    } else if (status === 200) {
        console.log("LOGGED IN!")
        window.location.replace("/tasks");
//        document.getElementById("nav_buttons").innerHTML = `<li><a href=# onclick='Profile();'>${JSON.parse(response).email}</a></li>
//        <li><a href="/api/v1/accounts/logout">Logout</a></li>`
//        document.getElementById("content").innerHTML = ""
    }
}

function Login(status, response){
    let email = document.getElementById("email").value
    let password = document.getElementById("password").value
    let reqData = JSON.stringify({"email": email, "password": password})
    err_block.innerHTML = ""
    makeRequest("POST", "/api/v1/accounts/session", handleLogin, reqData)
}

function Logout(){
    document.getElementById("nav_buttons").innerHTML = "<li><a href=# onclick='Register();'>Register</a></li>"
}