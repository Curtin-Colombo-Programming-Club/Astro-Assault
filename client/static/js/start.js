// DOM elements
const username = document.getElementById("username");
const hueThumb = document.querySelector(".hue-thumb");
const hueSlider = document.querySelector(".hue-slider");

// Flag to track if the thumb is being dragged
let isDragging = false;

// Function to handle mouse down event on the thumb
function handleMouseDown(event) {
    isDragging = true;
}

// Function to handle mouse move event while dragging the thumb
function handleMouseMove(event) {
    if (isDragging) {
        const newPosition = event.clientX - hueSlider.getBoundingClientRect().left;
        const maxPosition = hueSlider.offsetWidth;
        const newPositionPercent = Math.max(0, Math.min(newPosition, maxPosition)) / maxPosition * 100;
        hueThumb.style.left = `${newPositionPercent}%`;
    }
}

// Function to handle mouse up event to stop dragging the thumb
function handleMouseUp(event) {
    if (isDragging) {
        isDragging = false;
        sendData(username.value, getColorFromPosition());
    }
}

// Add mouse event listeners for mouse interactions
hueThumb.addEventListener("mousedown", handleMouseDown);
document.addEventListener("mousemove", handleMouseMove);
document.addEventListener("mouseup", handleMouseUp);

// Function to handle touch start event on the thumb
function handleTouchStart(event) {
    isDragging = true;
    event.preventDefault();
}

// Function to handle touch move event while dragging the thumb
function handleTouchMove(event) {
    if (isDragging) {
        const touch = event.touches[0];
        const newPosition = touch.clientX - hueSlider.getBoundingClientRect().left;
        const maxPosition = hueSlider.offsetWidth;
        const newPositionPercent = Math.max(0, Math.min(newPosition, maxPosition)) / maxPosition * 100;
        hueThumb.style.left = `${newPositionPercent}%`;
    }
}

// Function to handle touch end event to stop dragging the thumb
function handleTouchEnd(event) {
    if (isDragging) {
        isDragging = false;
        sendData(username.value, getColorFromPosition());
    }
}

// Add touch event listeners for touch interactions
hueThumb.addEventListener("touchstart", handleTouchStart);
document.addEventListener("touchmove", handleTouchMove);
document.addEventListener("touchend", handleTouchEnd);

// Function to calculate color based on the position of the hue thumb
function getColorFromPosition() {
    const positionPercent = parseFloat(hueThumb.style.left);
    const hue = positionPercent * 2.55; // Convert percentage to hue value (0-255)
    return [hue, 255, 255]; // Return HSL color
}

// Function to send data
function sendData(_username, _color) {
    const formData = new FormData();

    formData.append("username", _username);
    formData.append("color", JSON.stringify(_color));

    console.log(_color, _username);

    // Make a POST request using fetch
    fetch('/', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Log the response data
            localStorage.auth_token = data.auth_token;
            localStorage.username = data.username;
            //window.location.href = "/";
        })
        .catch(error => {
            console.error('Error:', error);
        });
}