const togglePassword = document.getElementById('togglePassword');
const passwordInput = document.getElementById('password');
const registerForm = document.querySelector('.register-form');
const notification = document.getElementById('notification');

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

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(registerForm);

    // Simulação de validação e exibição de notificação
    const name = formData.get('name');
    const login = formData.get('login');
    const password = formData.get('password');
    const role = formData.get('role');

    if (name && login && password && role) {
        // Simulando sucesso
        showNotification('Usuário cadastrado com sucesso', 'success');
        registerForm.reset();
    } else {
        // Simulando erro
        showNotification('Preencha todos os campos', 'error');
    }
});

function showNotification(message, type) {
    notification.textContent = message;
    notification.className = 'notification ' + type;
    notification.style.display = 'block';

    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}
