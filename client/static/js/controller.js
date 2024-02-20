// vars
var joyx = 0, joyy = 0, joydx = 0, joydy = 0, movementInterval;
var isJoystickPressed = false, joystickTouch = null;

// DOM elements
const main = document.getElementById("main");

const kills = document.getElementById("rectangle-button-1");
const deaths = document.getElementById("rectangle-button-2");

const joystickWrapper = document.getElementById("joy-stick-wrapper");
const joystickContainer = document.getElementById('joy-stick-container');
const joystickHandle = document.getElementById('joy-stick-thumb');

const settings_btn = document.getElementById("middle-button-1");
const respawn_btn = document.getElementById("middle-button-2");
const fullscreen_btn = document.getElementById("middle-button-3");

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

joystickHandle.addEventListener('mousedown', handleJoystickPress);
main.addEventListener('touchstart', (event) => {
    event.preventDefault();
    let touches = event.touches;
    console.log("touch start", touches);
    for (const touch of touches) {
        if (touch.target.id === "joy-stick-thumb" && !isJoystickPressed) {
            isJoystickPressed = true;
            movementInterval = setInterval(sendMovement, 10);
        }
        else if (touch.target.id === "button-1") {
            sendTrigger(1);
        }
        else if (touch.target.id === "button-2") {
            sendTrigger(2);
        }
        else if (touch.target.id === "button-3") {
            sendTrigger(3);
        }
        else if (touch.target.id === "middle-button-2") {
            respawn();
        }
        else if (touch.target.id === "middle-button-3") {
            toggleFullScreen();
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
function checkOrientation() {
    if (window.innerWidth > window.innerHeight) {
        console.log("Landscape orientation");
        document.querySelector(".overlay-container").classList.add('x');
        // Your code for landscape orientation
        main.classList.remove("portrait")
    } else {
        console.log("Portrait orientation");
        document.querySelector(".overlay-container").classList.remove('x');
        // Your code for portrait orientation
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
    socket.volatile.emit("respawn", { auth_token: localStorage.token });
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