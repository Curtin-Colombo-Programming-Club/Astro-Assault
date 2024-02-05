const joystickContainer = document.getElementById('joystick-container');
const joystickHandle = document.getElementById('joystick-handle');

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
            joystickHandle.style.transform = `translate(calc(-50% + ${joyx}px), calc(-50% + ${joyy}px))`;
        }
        else if (ack.status == 404 ) {
            console.log("Movement Error!");
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
}

function handleJoystickMove(event) {
    if (isJoystickPressed) {
        const containerRect = joystickContainer.getBoundingClientRect();
        let touch;
        try {
            touch = event.touches[0];
        } catch (error) {
            console.log(error)
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

        //console.log("moved", joyx, joyy, distance)

        /* socket.emit("movement", { dx: dx, dy: 0 }, (ack) => {
            console.log(ack);

            if (ack.status == 200) {
                joystickHandle.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
            }
        }); */


    }
}