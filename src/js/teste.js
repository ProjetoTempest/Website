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
  if (registerForm) {
      registerForm.addEventListener('submit', async (e) => {
          e.preventDefault();

          console.log("Passou aqui b")
  
          const name = document.getElementById('name').value;
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;
          const role_id = document.getElementById('role_id').value;
          console.log("String aqui3")
  
          if (name && email && password && role_id) {
              const data = { name, email, password, role_id };
  
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

  tbody.addEventListener('click', async (e) => {
    if (e.target.classList.contains('delete-btn')) {
      const row = e.target.parentElement.parentElement;
      const login = row.children[1].textContent; // Obtém o login do membro

      try {
        const response = await fetch(`https://api.seuservidor.com/members/${login}`, { // Ajuste a URL conforme necessário
          method: 'DELETE'
        });

        if (response.ok) {
          // Remove da tabela
          row.remove();
          showNotification('Membro excluído com sucesso!', 'notification success show');
        } else {
          const result = await response.json();
          showNotification(result.message, 'notification error show');
        }
      } catch (error) {
        showNotification('Erro ao excluir membro', 'notification error show');
      }
    }
  });
});