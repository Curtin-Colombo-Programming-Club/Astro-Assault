// DOM elements
const username = document.getElementById("username");
const hueThumb = document.querySelector(".hue-thumb");
const hueSlider = document.querySelector(".hue-slider");
const start = document.getElementById("start");

// vars
var rgb = [255, 0, 0];

// Flag to track if the thumb is being dragged
let isDragging = false;

// Add touch event listeners for touch interactions
hueThumb.addEventListener("touchstart", handleTouchStart);
document.addEventListener("touchmove", handleTouchMove);
document.addEventListener("touchend", handleTouchEnd);
// Add mouse event listeners for mouse interactions
hueThumb.addEventListener("mousedown", handleMouseDown);
document.addEventListener("mousemove", handleMouseMove);
document.addEventListener("mouseup", handleMouseUp);
//
start.addEventListener("click", sendData);

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


// Function to handle touch start event on the thumb
function handleTouchStart(event) {
    isDragging = true;
    event.preventDefault();
}

// Function to handle touch move event while dragging the thumb
function handleTouchMove(event) {
    if (isDragging) {
        event.preventDefault();
        const touch = event.touches[0];
        const newPosition = touch.clientX - hueSlider.getBoundingClientRect().left;
        const maxPosition = hueSlider.offsetWidth;
        const newPositionPercent = Math.max(0, Math.min(newPosition, maxPosition)) / maxPosition * 100;
        hueThumb.style.left = `${newPositionPercent}%`;

        rgb = [255, 0, 0];
        let rgb_e = [255, 255, 255]

        console.log(newPositionPercent);
        if (newPositionPercent >= 0 && newPositionPercent <=100/6) {
            _c = 255 * newPositionPercent* 6/100
            rgb = [255, _c, 0];
            rgb_e = [255, _c, 200];
        }
        else if (newPositionPercent > 100 / 6 && newPositionPercent <= 100/3) {
            _c = 255 - 255 * ((newPositionPercent - 100 / 6) * 6/100 )
            rgb = [_c, 255, 0];
            rgb_e = [_c, 255, 200];
        }
        else if (newPositionPercent > 100 / 3 && newPositionPercent <= 100 / 2) {
            _c = 255 * ((newPositionPercent - 100 / 3) * 6/100 )
            rgb = [0, 255, _c];
            rgb_e = [200, 255, _c];
        }
        else if (newPositionPercent > 100 / 2 && newPositionPercent <= 200 / 3) {
            _c = 255 - 255 * ((newPositionPercent - 100 / 2) * 6/100 )
            rgb = [0, _c, 255];
            rgb_e = [200, _c, 255];
        }
        else if (newPositionPercent > 200 / 3 && newPositionPercent <= 500 / 6) {
            _c = 255 * ((newPositionPercent - 200 / 3) * 6/100 )
            rgb = [_c, 0, 255];
            rgb_e = [_c, 200, 255];
        }
        else if (newPositionPercent > 500 / 6 && newPositionPercent <= 100) {
            _c = 255 - 255 * ((newPositionPercent - 500 / 6) * 6/100 )
            if (_c < 0) {
                _c = 0;
            }
            rgb = [255, 0, _c];
            rgb_e = [255, 200, _c];
            
        }

        //console.log(rgb)
        hueThumb.style.background = `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
        hueThumb.style.borderColor = `rgb(${rgb[0]*.33}, ${rgb[1]*.33}, ${rgb[2]*.33})`;
        document.documentElement.style.setProperty('--startP-start', `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`);
        document.documentElement.style.setProperty('--startP-end', `rgb(${rgb_e[0]}, ${rgb_e[1]}, ${rgb_e[2]})`);

    }
}

// Function to handle touch end event to stop dragging the thumb
function handleTouchEnd(event) {
    if (isDragging) {
        isDragging = false;
        //sendData(username.value, getColorFromPosition());
    }
}

// Function to calculate color based on the position of the hue thumb
function getColorFromPosition() {
    const positionPercent = parseFloat(hueThumb.style.left);
    const hue = positionPercent * 2.55; // Convert percentage to hue value (0-255)
    return [hue, 255, 255]; // Return HSL color
}

// Function to send data
function sendData(_username, _color) {
    const formData = new FormData();

    _color = rgb;
    _username = username.value || "nOuSeRnAmE";

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
            window.location.href = "/";
        })
        .catch(error => {
            console.error('Error:', error);
        });
}