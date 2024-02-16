//vars
var TOKEN = localStorage.auth_token;

// Construct the full URL
const sockUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? `:${window.location.port}` : ''}`;

const socket = io(sockUrl, {
    query: {
        token: TOKEN  // sending auth token
    }
});

socket.on('auth', (data) => {
    console.log(data)
    console.log('Authentication Status:', data.status);
    localStorage.token = data.token
});

// Listen for the 'cookie_set' event to handle setting the cookie on the client side
socket.on('cookie_set', (data) => {
    const expiryDate = new Date(data.expiry_time * 1000); // Convert timestamp to milliseconds
    document.cookie = `${data.cookie_name}=${data.cookie_value}; expires=${expiryDate.toUTCString()}`;
    console.log(`Cookie set: ${document.cookie}`);
});
