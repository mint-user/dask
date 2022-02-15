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

function makeRequest() {
    let email = document.getElementById("username").value
    console.log('Fetching updated data.');
    xhr.open("POST", "/api/v1/accounts/session", true);
    xhr.onload = function() {
        updateDisplay(xhr.status, xhr.response);
    }
    xhr.send({"email": email});
}

function updateDisplay(status, response){
    console.log(status, JSON.parse(response));
    if (status === 400) {
        alert(response);
    }
}