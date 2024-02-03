const socket = io('http://localhost:5000/', {
    query: {
        token: localStorage.token  // Pass your authentication token here
    }
});

socket.on('auth', (data) => {
    console.log(data)
    console.log('Authentication Status:', data.status);
    localStorage.token = data.token
});