const main = document.getElementById("main");

const joystickWrapper = document.getElementById("joy-stick-wrapper");
const joystickContainer = document.getElementById('joy-stick-container');
const joystickHandle = document.getElementById('joy-stick-thumb');

const button1 = document.getElementById("button-1");
const button2 = document.getElementById("button-2");
const button3 = document.getElementById("button-3");

var joyx = 0, joyy = 0, joydx = 0, joydy = 0, movementInterval;
var isJoystickPressed = false, joystickTouch = null;

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

/* button1.addEventListener("click", () => { sendTrigger(1) });
button2.addEventListener("click", () => { sendTrigger(2) });
button3.addEventListener("click", () => { sendTrigger(3) }); */

function sendMovement() {
    socket.emit("movement", { dx: joydx, dy: joydy, auth_token: localStorage.token }, (ack) => {
        //console.log(ack);
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
    socket.emit("trigger", { n: _n, auth_token: localStorage.token }, (ack) => {
        //console.log(ack);

        if (ack.status == 200) {
            //
        }
        else if (ack.status == 404) {
            console.log("Movement Error!");
        }
    });
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