document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById('registerForm');
  const notification = document.getElementById('notification');

  registerForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    if (confirm('Tem certeza de que deseja cadastrar este serviço?')) {
      const name = document.getElementById('nameservice').value;
      const description = document.getElementById('description').value;
      const price = document.getElementById('price').value;
      const imageFile = document.getElementById('image').files;
      
      const formData = new FormData();
      const imageFilesArray = Array.from(imageFile);

      imageFilesArray.forEach((file) => {
          formData.append('images', file);
      });

      const responseImg = await fetch('http://127.0.0.1:8000/images/upload-images', {
          method: 'POST',
          headers: {
              'Accept': 'application/json',
          },
          body: formData
      });

      const dataImg = await responseImg.json();
      const imgsUrl = [];

      dataImg.images.forEach((img) => {
          imgsUrl.push(img.url);
      });

      if (name && description && price && imageFile) {
        // formData.append('name', name);
        // formData.append('description', description);
        // formData.append('price', price);
        // formData.append('image', imageFile);

        const createService = {
          'title': name,
          'description': description,
          'value': parseFloat(price),
          'images': imgsUrl,
          }

        try {
          const response = await fetch('http://127.0.0.1:8000/services/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(createService)
          });

          const result = await response.json();
          if (response.ok) {
            showNotification('Serviço cadastrado com sucesso', 'success');
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

    // Função para adicionar um membro à tabela
    function addServiceToTable(service) {
      const { name, description, value, image } = service;
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td>${name}</td>
        <td>${description}</td>
        <td>${value}</td>
        <td>${image}</td>
      `;
      tbody.appendChild(newRow);
    }
  
    // Carrega os produtos do banco de dados ao carregar a página
    loadServices();
  
    async function loadServices() {
      tbody.innerHTML = ''; // Limpa a tabela
  
      try {
        const response = await fetch('https://api.seuservidor.com/members'); // Ajuste a URL conforme necessário
        const services = await response.json();
  
        services.forEach(service => {
          addServiceToTable(service);
        });
      } catch (error) {
        showNotification('Erro ao carregar produtos', 'notification error show');
      }
    }
  
    // Event listener para excluir produtos
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
            showNotification('Serviço excluído com sucesso!', 'notification success show');
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

