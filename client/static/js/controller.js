const joystickContainer = document.getElementById('joystick-container');
const joystickHandle = document.getElementById('joystick-handle');

let isJoystickPressed = false;

joystickHandle.addEventListener('mousedown', handleJoystickPress);
joystickHandle.addEventListener('touchstart', handleJoystickPress);

document.addEventListener('mouseup', handleJoystickRelease);
document.addEventListener('touchend', handleJoystickRelease);

document.addEventListener('mousemove', handleJoystickMove);
document.addEventListener('touchmove', handleJoystickMove);

function handleJoystickPress(event) {
    event.preventDefault();
    isJoystickPressed = true;
}

function handleJoystickRelease() {
    isJoystickPressed = false;
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

        let x = (event.clientX || touch.clientX) - (containerRect.left + containerRect.width / 2);
        let y = (event.clientY || touch.clientY) - (containerRect.top + containerRect.height / 2);

        const distance = Math.sqrt((x) ** 2 + (y) ** 2);

        if (distance <= containerHL) {
            joystickHandle.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;

            console.log("moved", x, -y, distance)

            socket.emit("movement", {dx: x/containerHL, dy: -y/containerHL}, (ack) => {
                console.log(ack);
            });
        }

    }
}