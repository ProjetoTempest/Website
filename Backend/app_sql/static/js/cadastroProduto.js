document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById('registerForm');
    const notification = document.getElementById('notification');
  
    registerForm.addEventListener('submit', async function (event) {
      event.preventDefault();
  
      if (confirm('Tem certeza de que deseja cadastrar este produto?')) {
        const title = document.getElementById('nameprod').value; // Alterado para 'title'
        const description = document.getElementById('description').value;
        const value = document.getElementById('price').value; // Alterado para 'value'
        const imageFiles = document.getElementById('image').files;
  
        if (title && description && value && imageFiles.length > 0) {
          const formData = new FormData();
          formData.append('title', title);
          formData.append('description', description);
          formData.append('value', value);
          
          for (let i = 0; i < imageFiles.length; i++) {
            formData.append('images', imageFiles[i]);
          }
  
          try {
            const response = await fetch('http://127.0.0.1:8000/products/', {
              method: 'POST',
              body: formData
            });
  
            const result = await response.json();
            if (response.ok) {
              showNotification('Produto cadastrado com sucesso', 'success');
              registerForm.reset();
            } else {
              showNotification(result.message, 'error');
            }
          } catch (error) {
            showNotification('Erro ao cadastrar produto', 'error');
          }
        } else {
          showNotification('Preencha todos os campos', 'error');
        }
      } else {
        showNotification('Cadastro cancelado.', 'error');
      }
    });
  
    function showNotification(message, type) {
      notification.textContent = message;
      notification.classList.add(type, 'show');
  
      setTimeout(() => {
        notification.textContent = '';
        notification.classList.remove(type, 'show');
      }, 5000);
    }
  });
