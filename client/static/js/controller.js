// vars
var joyx = 0, joyy = 0, joydx = 0, joydy = 0, movementInterval;
var isJoystickPressed = false, joystickTouch = null;
var settingsOverlay = false;

// DOM elements
const main = document.getElementById("main");

const kills = document.getElementById("rectangle-button-1");
const deaths = document.getElementById("rectangle-button-2");

const joystickWrapper = document.getElementById("joy-stick-wrapper");
const joystickContainer = document.getElementById('joy-stick-container');
const joystickHandle = document.getElementById('joy-stick-thumb');

// settings
const settings_btn = document.getElementById("settings");
const settings_back = document.getElementById("settings-back");

const respawn_btn = document.getElementById("respawn");
const fullscreen_btn = document.getElementById("fullscreen");

const button1 = document.getElementById("button-1");
const button2 = document.getElementById("button-2");
const button3 = document.getElementById("button-3");

// initial func calls
checkOrientation();

// SOCK listners
socket.on('kills', (data) => {
    console.log(data)
    kills.children[0].innerText = data.kills
});

socket.on('deaths', (data) => {
    console.log(data)
    deaths.children[0].innerText = data.deaths
});

socket.on("kds", (data) => {
    kills.children[0].innerText = data.kills
    deaths.children[0].innerText = data.deaths
});

// DOM listners
window.addEventListener('resize', checkOrientation);

settings_btn.addEventListener("click", ()=>{console.log("settings")})

joystickHandle.addEventListener('mousedown', handleJoystickPress);
document.body.addEventListener('touchstart', (event) => {
    event.preventDefault();
    let touches = event.touches;
    console.log("touch start", touches);

    for (const touch of touches) {
        switch (touch.target.id) {
            case "joy-stick-thumb":
                if (!isJoystickPressed) {
                    isJoystickPressed = true;
                    movementInterval = setInterval(sendMovement, 10);
                }
                break;

            case "button-1":
                sendTrigger(1);
                break;

            case "button-2":
                sendTrigger(2);
                break;

            case "button-3":
                sendTrigger(3);
                break;

            case "settings":
                toggleSettings();
                break;

            case "settings-back":
                toggleSettings();
                break;

            case "respawn":
                respawn()
                break;

            case "fullscreen":
                toggleFullScreen();
                break;
        
            default:
                break;
        }
    }
});

document.addEventListener('mouseup', handleJoystickRelease);
document.addEventListener('touchend', (event) => {
    let _js = false, _btn1 = false, _btn2 = false, _btn3 = false;
    event.preventDefault();
    let touches = event.touches;
    console.log("touch end", touches);
    for (const touch of touches) {
        if (touch.target.id === "joy-stick-thumb") {
            _js = true;
        }
    }

    if (!_js) {
        isJoystickPressed = false;
        clearInterval(movementInterval);
        socket.volatile.emit("movement", { dx: 0, dy: 0, auth_token: localStorage.token })
        joystickHandle.style.transform = `translate(calc(-50%), calc(-50%))`;
        joyx = joyy = joydx = joydy = 0;
        if (joystickWrapper.classList.contains("bad")) {
            joystickWrapper.classList.remove("bad");
        }
        if (joystickWrapper.classList.contains("good")) {
            joystickWrapper.classList.remove("good");
        }
    }
});

document.addEventListener('mousemove', handleJoystickMove);
document.addEventListener('touchmove', handleJoystickMove);

// functions
function toggleSettings() {
    settingsOverlay = !settingsOverlay;
    console.log(settingsOverlay);
    if (settingsOverlay) {
        console.log("Showing settings...");
        document.querySelector(".overlay-container").classList.remove('x');
        document.getElementById("settings-overlay").classList.add('a');
    } else {
        console.log("Closing settings...");
        document.querySelector(".overlay-container").classList.add('x');
        document.getElementById("settings-overlay").classList.remove('a');
    }
}

function checkOrientation() {
    if (window.innerWidth > window.innerHeight) {
        if (!settingsOverlay) {
            document.querySelector(".overlay-container").classList.add('x');
            document.getElementById("orientation-overlay").classList.remove('a');
        }
        console.log("Landscape orientation");
        // Your code for landscape orientation
        main.classList.remove("portrait")
    } else {
        console.log("Portrait orientation");
        
        if (!settingsOverlay) {
            document.querySelector(".overlay-container").classList.remove('x');
            document.getElementById("orientation-overlay").classList.add('a');
            // Your code for portrait orientation
        }
        main.classList.add("portrait");
        //main.style.left = `${(window.innerWidth - window.innerHeight) / 2}px`
    }
}

function sendMovement() {
    console.log(joydy);
    socket.volatile.emit("movement", { dx: joydx, dy: joydy, auth_token: localStorage.auth_token }, (ack) => {
        if (ack.status == 200) {
            if (!joystickWrapper.classList.contains("good")) {
                joystickWrapper.classList.add("good");
            }
            if (joystickWrapper.classList.contains("bad")) {
                joystickWrapper.classList.remove("bad");
            }
        }
        else if (ack.status == 404) {
            if (!joystickWrapper.classList.contains("bad")) {
                joystickWrapper.classList.add("bad");
            }
            if (joystickWrapper.classList.contains("good")) {
                joystickWrapper.classList.remove("good");
            }
        }
    });
}

function sendTrigger(_n) {
    socket.volatile.emit("trigger", { n: _n, auth_token: localStorage.auth_token }, (ack) => {
        if (ack.status == 200) {
            //
        }
        else if (ack.status == 404) {
            console.log("Movement Error!");
        }
    });
}

function respawn() {
    socket.volatile.emit("respawn", { auth_token: localStorage.auth_token });
}

function handleJoystickPress(event) {
    event.preventDefault();
    isJoystickPressed = true;
    movementInterval = setInterval(sendMovement, 10);
}

function handleJoystickRelease() {
    isJoystickPressed = false;
    clearInterval(movementInterval);
    joystickHandle.style.transform = `translate(calc(-50%), calc(-50%))`;
    joyx = joyy = joydx = joydy = 0;
    if (joystickWrapper.classList.contains("bad")) {
        joystickWrapper.classList.remove("bad");
    }
    if (joystickWrapper.classList.contains("good")) {
        joystickWrapper.classList.remove("good");
    }
}

function handleJoystickMove(event) {
    if (isJoystickPressed) {
        const containerRect = joystickContainer.getBoundingClientRect();

        let containerHL = containerRect.width / 2

        for (const touch of event.touches) {
            if (touch.target.id === "joy-stick-thumb") {
                joystickTouch = touch;
            }
        }

        joyx = (event.clientX || joystickTouch.clientX) - (containerRect.left + containerRect.width / 2);
        joyy = (event.clientY || joystickTouch.clientY) - (containerRect.top + containerRect.height / 2);

        joydx = joyx / containerHL;
        joydy = joyy / containerHL;

        const distance = Math.sqrt((joyx) ** 2 + (joyy) ** 2);

        if (distance > containerHL) {
            let theta = Math.atan2(joydy, joydx);
            joydx = Math.cos(theta);
            joydy = Math.sin(theta);

            joyx = joydx * containerHL;
            joyy = joydy * containerHL;
        }

        joystickHandle.style.transform = `translate(calc(-50% + ${joyx}px), calc(-50% + ${joyy}px))`;
        //sendMovement();
    }
}