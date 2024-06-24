// Variables to store keystroke and mouse dynamics data
var keystrokeData = [];
var mouseData = [];
var mouseClickData = [];
console.log("script.js loaded");



// Capture mouse movements
document.addEventListener('mousemove', function(event) {
    mouseData.push({
        eventType: 'mousemove',
        x: event.clientX,
        y: event.clientY,
        button: "MOVE",
        timeStamp: new Date().getTime()
    });
});
['mousedown', 'mouseup'].forEach(function(type) {
    document.addEventListener(type, function(event) {
        mouseData.push({
            eventType: type,
            x: event.clientX,
            y: event.clientY,
            button: event.button,
            timeStamp: new Date().getTime()
        });
    });
});
// Variables to store keystroke and mouse dynamics data
var keystrokeData = [];
var mouseMoveData = [];
var mouseClickData = [];
console.log("script.js loaded");

// Capture keystroke dynamics
document.addEventListener('keydown', function(event) {
    keystrokeData.push({
        key: event.key,
        action: "keydown",
        timeStamp: new Date().getTime()
    });
    console.log("Key down:", event.key, "at time", event.timeStamp);
});
document.addEventListener('keyup', function(event) {
    keystrokeData.push({
        key: event.key,
        action: "keyup",
        timeStamp: new Date().getTime()
    });
    console.log("Key up:", event.key, "at time", event.timeStamp);
});


// Capture mouse clicks (uncommented and adjusted)
// document.addEventListener('click', function(event) {
//     mouseClickData.push({
//         eventType: 'click',
//         x: event.clientX,
//         y: event.clientY,
//         button: event.button,
//         timeStamp: event.timeStamp
//     });
//     console.log("Mouse click at:", event.clientX, event.clientY, "button", event.button, "at time", event.timeStamp);
// });

// Capture mouse down
document.addEventListener('mousedown', function(event) {
    mouseClickData.push({
        eventType: 'mousedown',
        x: event.clientX,
        y: event.clientY,
        button: event.button,
        timeStamp: new Date().getTime()
    });
    console.log("Mouse down at:", event.clientX, event.clientY, "button", event.button, "at time", event.timeStamp);
});


// // Capture mouse clicks
// document.addEventListener('click', function(event) {
//     mouseClickData.push({
//         x: event.clientX,
//         y: event.clientY,
//         button: event.button,
//         timeStamp: event.timeStamp
//     });
// });

// Capture mouse down
document.addEventListener('mousedown', function(event) {
    mouseClickData.push({ // You might want to use a separate array for clarity
        eventType: 'mousedown',
        x: event.clientX,
        y: event.clientY,
        button: event.button,
        timeStamp: new Date().getTime()
    });
});



// Updates the message displayed on the page to indicate success or failure
function updateMessage(msg, isSuccess) {
    var messageElement = document.getElementById('message');
    messageElement.textContent = msg;
    messageElement.style.color = isSuccess ? 'green' : 'red';
    messageElement.style.fontSize = '1.2em';
}

// Clears login form fields after submission
function clearLoginForm() {
    document.getElementById('loginEmail').value = '';
    document.getElementById('robotCheck').value = '';
}

// Clears signup form fields after submission
function clearSignupForm() {
    document.getElementById('fullName').value = '';
    document.getElementById('signupEmail').value = '';
}
// Clears signup form fields after submission
function clearSignupForm() {
    document.getElementById('fullName').value = '';
    document.getElementById('signupEmail').value = '';
    document.getElementById('signupPassword').value = '';
    document.getElementById('confirmPassword').value = '';
}

// Handles form submission for both login and signup actions
function handleFormSubmit(event) {
    event.preventDefault();
    // If value is not equal to I am not a robot, then alert the user and reload the page
    if (document.getElementById('robotCheck').value !== "I am not a robot") {
        alert("Please confirm you are not a robot.");
        setTimeout(function() { window.location.reload(); }, 500);
    }else{
    const mouseCSVData = convertArrayToCSV(mouseData, ["eventType", "x", "y", "button", "timeStamp"]);
    downloadCSV(mouseCSVData, "mouseDynamicsData.csv");

    const keystrokeCSVData = convertArrayToCSV(keystrokeData, ["action", "key", "action","timeStamp"]);
    downloadCSV(keystrokeCSVData, "keystrokeDynamicsData.csv");

    resetDynamicsData();
    setTimeout(function() { window.location.reload(); }, 500);
}
}
// Clears all data arrays after sending
function resetDynamicsData() {
    keystrokeData = [];
    mouseMoveData = [];
    mouseClickData = [];
}

// Handles user login, including data collection and sending to the server
function login() {
    var email = document.getElementById('loginEmail').value;
    var robotCheck = document.getElementById('robotCheck').value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/login", true); // Assume '/login' is your backend endpoint for login
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            clearFormFields(); // Clear fields after submission
            if (xhr.status === 200) {
                updateMessage('Login successful!', true);
            } else {
                updateMessage('Login failed. ' + xhr.responseText, false);
            }
        }
    };

    var data = JSON.stringify({
        email: email,
        robotCheck: robotCheck,
        keystrokeData: keystrokeData,
        mouseMoveData: mouseMoveData,
        mouseClickData: mouseClickData
    });

    xhr.send(data);
}

function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}


// Handles new user registration, including data collection and sending to the server
function signup() {
    var fullName = document.getElementById('fullName').value;
    var email = document.getElementById('signupEmail').value;
    var password = document.getElementById('signupPassword').value;
    var fingerprintData = collectFingerprintData(); // Collects browser and device fingerprint data

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/signup", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            clearSignupForm(); // Clears form fields after server response
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
        mouseClickData: mouseClickData,
        fingerprintData: fingerprintData
    });

    xhr.send(data);

    // Reset data arrays after sending
    keystrokeData = [];
    mouseMoveData = [];
    mouseClickData = [];
}

// Attach event listeners to the form submit events
document.getElementById('loginForm').addEventListener('submit', handleFormSubmit);
document.getElementById('signupForm').addEventListener('submit', handleFormSubmit);
// Function to convert mouse data to CSV format
// Convert dynamics data to CSV format
function convertArrayToCSV(data, headers) {
    const csvRows = [];
    csvRows.push(headers.join(',')); // Add headers
    data.forEach(item => {
        const values = headers.map(header => item[header]);
        csvRows.push(values.join(','));
    });
    return csvRows.join("\n");
}

// Function to trigger CSV download
// Function to trigger CSV download
function downloadCSV(csvData, fileName) {
    const blob = new Blob([csvData], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', fileName);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

function detectFonts() {
    const baseFonts = ['monospace', 'sans-serif', 'serif'];
    const testString = "mmmmmmmmmmlli";
    const testSize = '72px';
    const h = document.getElementsByTagName("body")[0];
    const testSpan = document.createElement("span");
    testSpan.style.fontSize = testSize;
    testSpan.innerHTML = testString;
    const defaultWidths = {};
    const detectedFonts = [];

    for (const baseFont of baseFonts) {
        testSpan.style.fontFamily = baseFont;
        h.appendChild(testSpan);
        defaultWidths[baseFont] = testSpan.offsetWidth;
        h.removeChild(testSpan);
    }

    const testFonts = ['Arial', 'Verdana', 'Helvetica', 'Times New Roman', 'Courier New']; // Add more fonts as needed
    for (const font of testFonts) {
        for (const baseFont of baseFonts) {
            testSpan.style.fontFamily = font + ',' + baseFont;
            h.appendChild(testSpan);
            const matched = testSpan.offsetWidth !== defaultWidths[baseFont];
            h.removeChild(testSpan);
            if (matched) {
                detectedFonts.push(font);
                break; // No need to check other base fonts
            }
        }
    }

    return detectedFonts;
}


// Collects browser and device information for fingerprinting, including canvas fingerprint
function collectFingerprintData() {
    var canvasFingerprint = getCanvasFingerprint(); // Existing canvas fingerprinting
    var fonts = detectFonts(); // Detect available fonts
    var clientHints = getClientHints(); // Collect client hints (simplified version)

    var fingerprint = {
        userAgent: navigator.userAgent,
        screenResolution: screen.width + 'x' + screen.height,
        language: navigator.language,
        platform: navigator.platform,
        canvasFingerprint: canvasFingerprint,
        fonts: fonts, // Include detected fonts
        clientHints: clientHints, // Include client hints
    };
    return fingerprint;
}

function getClientHints() {
    return {
        deviceMemory: navigator.deviceMemory || 'unknown', // Returns the amount of device memory in GiB, if available.
        hardwareConcurrency: navigator.hardwareConcurrency, // Returns the number of logical processors.
        userAgent: navigator.userAgent, // The user agent string (considered a legacy approach).
        viewportWidth: window.innerWidth, // The width of the viewport.
    };
}
// Generates a unique identifier using the HTML5 Canvas API
function getCanvasFingerprint() {
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    ctx.textBaseline = "top";
    ctx.font = "14px Arial";
    ctx.fillText("canvas fingerprint", 10, 10);
    return canvas.toDataURL();
}

// Ensures default tab is opened and canvas fingerprinting is ready after DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    document.getElementsByClassName("tablinks")[0].click();
});
