if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+ ...
    xhr = new XMLHttpRequest();
} else if (window.ActiveXObject) { // IE 6 and older
    xhr = new ActiveXObject("Microsoft.XMLHTTP");
}

if (!xhr) {
    alert('Giving up :( Cannot create an XMLHTTP instance');
}

function makeRequest(reqType, URL, funcOnLoad, data=null) {
    console.log(reqType, URL, funcOnLoad, data);
    xhr.open(reqType, URL, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    xhr.onload = function() { funcOnLoad.call(this, xhr.status, xhr.response) }
    xhr.send(data);
}

function renderTasks(status, response){
    console.log(response);
    data = JSON.parse(response).tasks;
        var col = [];
        for (var i = 0; i < data.length; i++) {
            for (var key in data[i]) {
                if (col.indexOf(key) === -1) {
                    col.push(key);
                }
            }
        }

        // Create a table.
        var table = document.createElement("table");

        // Create table header row using the extracted headers above.
        var tr = table.insertRow(-1);                   // table row.

        for (var i = 0; i < col.length; i++) {
            var th = document.createElement("th");      // table header.
            th.innerHTML = col[i];
            tr.appendChild(th);
        }

        // add json data to the table as rows.
        for (var i = 0; i < data.length; i++) {

            tr = table.insertRow(-1);

            for (var j = 0; j < col.length; j++) {
                var tabCell = tr.insertCell(-1);
                tabCell.innerHTML = data[i][col[j]];
            }
        }

        // Now, add the newly created table with json data, to a container.
        var divShowData = document.getElementById('app');
        divShowData.innerHTML = "";
        divShowData.appendChild(table);
}

function loadTasks(){
    makeRequest("GET", "/api/v1/tasks", renderTasks);
}

loadTasks()