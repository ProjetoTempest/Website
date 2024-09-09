/*document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById('registerForm');
  const notification = document.getElementById('notification');

  registerForm.addEventListener('submit', function (event) {
    event.preventDefault();

    if (confirm('Tem certeza de que deseja cadastrar este produto?')) {
      const name = document.getElementById('nameprod').value;
      const description = document.getElementById('description').value;
      const price = document.getElementById('price').value;
      const image = document.getElementById('image').files[0].name;

      console.log("Nome:", name);
      console.log("Descrição:", description);
      console.log("Preço:", price);
      console.log("Imagem:", image);

      if (name && description && price && image) {
        // Criar o produto
        const product = {
          name: name,
          description: description,
          price: price,
          image: image
        };

        // Recuperar produtos do localStorage
        let products = JSON.parse(localStorage.getItem('products')) || [];

        // Adicionar o novo produto
        products.push(product);

        // Salvar no localStorage
        localStorage.setItem('products', JSON.stringify(products));

        // Simulando sucesso
        showNotification('Produto cadastrado com sucesso', 'success');
        registerForm.reset();
      } else {
        // Simulando erro
        showNotification('Preencha todos os campos', 'error');
      }
    } else {
      showNotification('Cadastro cancelado.', 'error');
    }
  });
});

function showNotification(message, type) {
  const notification = document.getElementById('notification');
  notification.textContent = message;
  notification.classList.add(type, 'show');

  setTimeout(() => {
    notification.textContent = '';
    notification.classList.remove(type, 'show');
  }, 5000);
}*/

document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById('registerForm');
  const notification = document.getElementById('notification');

  registerForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    if (confirm('Tem certeza de que deseja cadastrar este produto?')) {
      const name = document.getElementById('nameprod').value;
      const description = document.getElementById('description').value;
      const price = document.getElementById('price').value;
      const imageFile = document.getElementById('image').files[0];

      if (name && description && price && imageFile) {
        const formData = new FormData();
        formData.append('name', name);
        formData.append('description', description);
        formData.append('price', price);
        formData.append('image', imageFile);

        try {
          const response = await fetch('https://api.seuservidor.com/products', {
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

   // Função para adicionar um membro à tabela
   function addProductToTable(product) {
    const { name, description, value, image } = product;
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
  loadProducts();

  async function loadProducts() {
    tbody.innerHTML = ''; // Limpa a tabela

    try {
      const response = await fetch('https://api.seuservidor.com/members'); // Ajuste a URL conforme necessário
      const products = await response.json();

      products.forEach(product => {
        addProductToTable(product);
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
          showNotification('Produto excluído com sucesso!', 'notification success show');
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

