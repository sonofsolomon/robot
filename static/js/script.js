// Variables to store keystroke and mouse dynamics data
var keystrokeData = [];
var mouseMoveData = [];
var mouseClickData = [];

// Function to update message on the page
function updateMessage(msg, isSuccess) {
    var messageElement = document.getElementById('message');
    messageElement.textContent = msg;
    messageElement.style.color = isSuccess ? 'green' : 'red';
    messageElement.style.fontSize = '1.2em';
}

// Function to clear login form fields
function clearLoginForm() {
    document.getElementById('loginEmail').value = '';
    document.getElementById('loginPassword').value = '';
    document.getElementById('robotCheck').value = '';
}

// Function to clear signup form fields
function clearSignupForm() {
    document.getElementById('fullName').value = '';
    document.getElementById('signupEmail').value = '';
    document.getElementById('signupPassword').value = '';
    document.getElementById('confirmPassword').value = '';
}

// Function to handle form submission
function handleFormSubmit(event) {
    event.preventDefault(); // Prevent the default form submission

    var formId = event.target.id;
    if (formId === 'loginForm') {
        login();
    } else if (formId === 'signupForm') {
        signup();
    }
}

// Function to handle login
function login() {
    var email = document.getElementById('loginEmail').value;
    var password = document.getElementById('loginPassword').value;
    var robotCheck = document.getElementById('robotCheck').value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/login", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            clearLoginForm(); // Clear the form immediately after server response
            if (xhr.status === 200) {
                updateMessage('Login successful!', true);
            } else {
                updateMessage('Login failed. ' + xhr.responseText, false);
            }
        }
    };

    var data = JSON.stringify({
        email: email,
        password: password,
        robotCheck: robotCheck,
        keystrokeData: keystrokeData,
        mouseMoveData: mouseMoveData,
        mouseClickData: mouseClickData
    });

    xhr.send(data);

    // Clear the arrays after sending data
    keystrokeData = [];
    mouseMoveData = [];
    mouseClickData = [];
}

// Function to handle signup
function signup() {
    var fullName = document.getElementById('fullName').value;
    var email = document.getElementById('signupEmail').value;
    var password = document.getElementById('signupPassword').value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/signup", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            clearSignupForm(); // Clear the form immediately after server response
            if (xhr.status === 200) {
                updateMessage('Signup successful!', true);
            } else {
                updateMessage('Signup failed. ' + xhr.responseText, false);
            }
        }
    };

    var data = JSON.stringify({
        fullName: fullName,
        email: email,
        password: password,
        keystrokeData: keystrokeData,
        mouseMoveData: mouseMoveData,
        mouseClickData: mouseClickData
    });

    xhr.send(data);

    // Clear the arrays after sending data
    keystrokeData = [];
    mouseMoveData = [];
    mouseClickData = [];
}

// Attach the event listener to the form's submit event
document.getElementById('loginForm').addEventListener('submit', handleFormSubmit);
document.getElementById('signupForm').addEventListener('submit', handleFormSubmit);

// Function to handle tab switching
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Function to capture keystroke dynamics
document.getElementById('robotCheck').addEventListener('keyup', function(event) {
    var keystroke = {
        key: event.key,
        timeStamp: event.timeStamp
    };
    keystrokeData.push(keystroke);
});

// Function to capture mouse movements
document.addEventListener('mousemove', function(event) {
    var mouseMove = {
        x: event.clientX,
        y: event.clientY,
        timeStamp: event.timeStamp
    };
    mouseMoveData.push(mouseMove);
});

// Function to capture mouse clicks
document.addEventListener('click', function(event) {
    var mouseClick = {
        x: event.clientX,
        y: event.clientY,
        timeStamp: event.timeStamp
    };
    mouseClickData.push(mouseClick);
});

// Set the default open tab
document.getElementsByClassName("tablinks")[0].click();
