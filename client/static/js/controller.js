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

        let dx = x / containerHL;
        let dy = y / containerHL;

        const distance = Math.sqrt((x) ** 2 + (y) ** 2);

        if (distance > containerHL) {
            let theta = Math.atan2(dy, dx);
            dx = Math.cos(theta);
            dy = Math.sin(theta);

            x = dx * containerHL;
            y = dy * containerHL;
        }

        console.log("moved", x, y, distance)

        socket.emit("movement", { dx: dx, dy: dy }, (ack) => {
            console.log(ack);

            if (ack.status == 200) {
                joystickHandle.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
            }
        });


    }
}