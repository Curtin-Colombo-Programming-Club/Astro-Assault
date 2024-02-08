const joystickWrapper = document.getElementById("joy-stick-wrapper");
const joystickContainer = document.getElementById('joy-stick-container');
const joystickHandle = document.getElementById('joy-stick-thumb');

var joyx = 0, joyy = 0, joydx = 0, joydy = 0, movementInterval;


let isJoystickPressed = false;

joystickHandle.addEventListener('mousedown', handleJoystickPress);
joystickHandle.addEventListener('touchstart', handleJoystickPress);

document.addEventListener('mouseup', handleJoystickRelease);
document.addEventListener('touchend', handleJoystickRelease);

document.addEventListener('mousemove', handleJoystickMove);
document.addEventListener('touchmove', handleJoystickMove);

function sendMovement() {
    socket.emit("movement", { dx: joydx, dy: joydy }, (ack) => {
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

function handleJoystickPress(event) {
    event.preventDefault();
    isJoystickPressed = true;
    movementInterval = setInterval(sendMovement, 100);
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
        let touch;
        try {
            touch = event.touches[0];
        } catch (error) {
            //console.log(error)
        }

        let containerHL = containerRect.width / 2

        joyx = (event.clientX || touch.clientX) - (containerRect.left + containerRect.width / 2);
        joyy = (event.clientY || touch.clientY) - (containerRect.top + containerRect.height / 2);

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
    }
}