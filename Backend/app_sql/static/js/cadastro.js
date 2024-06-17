document.addEventListener("DOMContentLoaded", function () {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const registerForm = document.getElementById('registerForm');
    const notification = document.getElementById('notification');
    console.log("Passou aqui")
    console.log(document.getElementById('registerForm'))
    if (togglePassword && passwordInput) {
        console.log("Passou aqui a")
        
        togglePassword.addEventListener('click', () => {
            const type = passwordInput.type === 'password' ? 'text' : 'password';
            passwordInput.type = type;
    
            if (type === 'password') {
                togglePassword.classList.add('fa-eye-slash');
                togglePassword.classList.remove('fa-eye');
            } else {
                togglePassword.classList.remove('fa-eye-slash');
                togglePassword.classList.add('fa-eye');
            }
        });
    }
  
    console.log(registerForm)
    if (registerForm) { // erro
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            console.log("Paasou be")
    
            const name = document.getElementById('name').value;
            const login = document.getElementById('login').value;
            const password = document.getElementById('password').value;
            const role = document.getElementById('role').value;
            console.log("String aqui3")
    
            if (name && login && password && role) {
                const data = { name, login, password, role };
    
                console.log("String aqui2")
                try {
                    console.log("String aqui")
                    const response = await fetch('http://127.0.0.1:8000/users/', {
                        method: 'POST',
                        headers: {
                            'accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });
    
                    if (response.ok) {
                        // const result = await response.json();
                        // showNotification(result.message, 'notification success show');
                        showNotification('Membro cadastrado com sucesso!', 'notification success show');
                        console.log("Ok")
                        registerForm.reset();
                    } else {
                        const errorResult = await response.json();
                        showNotification(errorResult.detail, 'notification error show');
                    }
                } catch (error) {
                    console.error('Erro na requisição:', error);
                    showNotification('Erro ao registrar usuário', 'notification error show');
                }
            } else {
                showNotification('Preencha todos os campos', 'notification error show');
            }
        });
    }
  
    function showNotification(message, type) {
        notification.textContent = message;
        notification.className = 'notification ' + type;
        notification.style.display = 'block';
    
        setTimeout(() => {
            notification.style.display = 'none';
        }, 5000);
    }
});
