document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('https://your-backend-url/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    
    if (result.success) {
        alert(`Welcome ${result.user.name}`);
        window.location.href = 'dashboard.html';
    } else {
        alert(result.message);
    }
});
