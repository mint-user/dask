if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+ ...
    xhr = new XMLHttpRequest();
} else if (window.ActiveXObject) { // IE 6 and older
    xhr = new ActiveXObject("Microsoft.XMLHTTP");
}

if (!xhr) {
    alert('Giving up :( Cannot create an XMLHTTP instance');
}

err_block = document.getElementById("error");
success_block = document.getElementById("success");


function makeRequest(reqType, URL, funcOnLoad, data) {
    // console.log(reqType, URL, funcOnLoad, data);
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
    }
}

function Login(status, response){
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let reqData = JSON.stringify({"email": email, "password": password});
    err_block.innerHTML = "";
    success_block.innerHTML = "";
    makeRequest("POST", "/api/v1/accounts/session", handleLogin, reqData);
}

function Logout(){
    document.getElementById("nav_buttons").innerHTML = "<li><a href=# onclick='Register();'>Register</a></li>"
}

function showSignUpForm(){
    let formTitle = document.getElementById("formTitle");
    formTitle.innerText = "Sign Up";
    let submitBtn = document.getElementById("submit");
    submitBtn.value = "Register";
    submitBtn.onclick = function singUp(){
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;
        let reqData = JSON.stringify({"email": email, "password": password});
        err_block.innerHTML = "";
        success_block.innerHTML = "";
        makeRequest("POST", "/api/v1/accounts", handleSingUp, reqData);
    }
}

function handleSingUp(status, response){
    console.log(status, JSON.parse(response));
    if (status === 400) {
        JSON.parse(response).msg.forEach((err) => {
            console.log(err);
            err_block.innerText += err.msg;
            err_block.appendChild(document.createElement("br"));
        })
    } else if (status === 201) {
        console.log("SIGNED UP SUCCESSFUL!");
        // window.location.replace("/tasks");
        success_block.innerText += "SIGNED UP SUCCESSFUL! Now you may Log In";
        showLoginForm();
    }
}

function showLoginForm(){
    let formTitle = document.getElementById("formTitle");
    formTitle.innerText = "Login";
    let submitBtn = document.getElementById("submit");
    submitBtn.value = "Login";
    // let submitBtn = document.getElementById("submit");
    // submitBtn.onclick = Login();
    submitBtn.setAttribute("onclick", "Login();")
}