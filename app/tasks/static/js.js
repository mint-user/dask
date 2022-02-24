if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+ ...
    xhr = new XMLHttpRequest();
} else if (window.ActiveXObject) { // IE 6 and older
    xhr = new ActiveXObject("Microsoft.XMLHTTP");
}

if (!xhr) {
    alert('Giving up :( Cannot create an XMLHTTP instance');
}

function makeRequest(reqType, URL, funcOnLoad, data=null) {
    // console.log(reqType, URL, funcOnLoad, data);
    xhr.open(reqType, URL, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    xhr.onload = function() { funcOnLoad.call(this, xhr.status, xhr.response) }
    xhr.send(data);
}

function renderTasks(status, response){
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

            // fill table row
            for (var j = 0; j < col.length; j++) {
                var tabCell = tr.insertCell(-1);
                tabCell.innerHTML = data[i][col[j]];
            }

            // add delete button
            var cellDelete = tr.insertCell(-1);
            var btnDelete = document.createElement("a");
            btnDelete.href = "#";
            btnDelete.innerText = "x";
            btnDelete.setAttribute("onclick", `deleteTask(${data[i].id});`);
            cellDelete.appendChild(btnDelete);
        }

        // add for Actions
        trActions = table.insertRow(-1);
        let btnPlusCell = trActions.insertCell(-1);
        let btnPlusTag = document.createElement("a");
        btnPlusTag.href = "#";
        btnPlusTag.onclick = function f() { showFormForNewTask();};
        btnPlusTag.innerText = "+"
        btnPlusTag.id = "btnPlus"
        btnPlusCell.appendChild(btnPlusTag);
        let nameField = trActions.insertCell(-1);
        nameField.id = "nameField";
        let actionsCell = trActions.insertCell(-1);
        actionsCell.id = "actionsCell";

        // Now, add the newly created table with json data, to a container.
        var divShowData = document.getElementById('app');
        divShowData.innerHTML = "";
        divShowData.appendChild(table);
}

function showFormForNewTask(){
    // hide "+" button
    document.getElementById("btnPlus").style = "display: none";
    // add Name field
    let nameFieldCell = document.getElementById("nameField");
    let inputField = document.createElement("input");
    inputField.id = "inputField";
    nameFieldCell.appendChild(inputField);
    inputField.focus();

    // add Confirm button
    let actionsCell = document.getElementById("actionsCell");
    let btnConfirm = document.createElement("a");
    btnConfirm.innerHTML = `<a href="#" onclick="sendNewTask();">Add</a>`;
    btnConfirm.id = "btnConfirm";
    actionsCell.appendChild(btnConfirm);

    //add Cancel button
    let btnCancel = document.createElement("a");
    btnCancel.innerText = "Hide"
    btnCancel.href = "#"
    btnCancel.onclick = function candel(){
        nameFieldCell.innerHTML = "";
        actionsCell.innerHTML = "";
        document.getElementById("btnPlus").style = "";

    }
    actionsCell.appendChild(btnCancel);
}

function handleNewTaskResp(status, response) {
    if (status == 201) {
        loadTasks();
    } else {
        console.log(response);
        let actionsCell = document.getElementById("actionsCell");
        let errMess = document.createElement("span");
        errMess.innerText = JSON.parse(response).msg[0].msg;
        actionsCell.appendChild(errMess);
    }
}

function sendNewTask() {
        let name = document.getElementById("inputField").value;
        data = JSON.stringify({name: name});
        makeRequest("POST", "/api/v1/tasks", handleNewTaskResp, data);
}

function deleteTask(taskID){
    let data = JSON.stringify({id: taskID});
    makeRequest("DELETE", "/api/v1/tasks", loadTasks, data);
}

function loadTasks(){
    makeRequest("GET", "/api/v1/tasks", renderTasks);
}

loadTasks()