function buttonClicked(buttonNumber) {
    console.log('Button ' + buttonNumber + ' clicked!');
    // You can add your button click logic here

    navigator.vibrate(200); // vibrate for 200ms
    navigator.vibrate([80, 20, 80, 20, 80, 20, 80, 20, 80, 20]); // Vibrate 'SOS' in Morse.
}


let isButtonHeld = false;

function shoot1() {
    if (isButtonHeld) {
        navigator.vibrate([60, 15]); // Vibrate 'SOS' in Morse.
        console.log("shooting");
    }
}

let b = document.getElementById("button")
let buttonHoldInterval;

b.addEventListener('touchstart', () => {
    event.preventDefault();
    isButtonHeld = true;
    // Call the handleButtonHold function immediately
    shoot1();

    // Set an interval to call the handleButtonHold function repeatedly
    buttonHoldInterval = setInterval(shoot1, 90); // Adjust the interval as needed
});

// Event listener for mouse up (button release)
button.addEventListener('touchend', () => {
    isButtonHeld = false;
    // Clear the interval when the button is released
    clearInterval(buttonHoldInterval);
});