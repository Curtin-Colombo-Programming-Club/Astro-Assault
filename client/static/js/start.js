// DOM elements
const username = document.getElementById("username");

// functions
function sendData(_username = "UsErNaMe", _color = [255, 0, 0]) {
    const formData = new FormData();

    formData.append("username", _username);
    formData.append("color", JSON.stringify(_color));

    console.log(_color, username.value);

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