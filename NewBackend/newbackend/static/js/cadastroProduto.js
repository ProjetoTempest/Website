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
        const formImg = new FormData();
        formImg.append('ident_img', title);

        for (let i = 0; i < imageFiles.length; i++) {
          formImg.append('imgs', imageFiles[i]);
        }

        try {
          const responImg = await fetch(`http://127.0.0.1:8000/save_img/`, {
            method: 'POST',
            body: formImg
          });

          console.log("Banana1")
          console.log(responImg.ok)
          
          if (!responImg.ok) {
            console.log("entrou no if")
            const result = await responImg.json();
            showNotification(result.message || 'Erro ao enviar imagens', 'error');
            return;
          }

          const resultImg = await responImg.json();
          console.log("ResultImg: ", resultImg);

          const images = resultImg.map(imageDict => ({ url: imageDict.url }));
          console.log("Images array: ", images);

          // const resultImg = await responImg.json();
          // const images = resultImg.map(imageDict => ({ url: imageDict.url }));

          // console.log(images)

          const productData = {
            "title": title,
            "description": description,
            "value": value, // Certifique-se de que o valor está no formato correto
            "images": images
          };

          console.log("Banana")
          const response = await fetch('http://127.0.0.1:8000/products/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData)
          });

          const result1 = await response.json();

          if (response.ok) {
            showNotification('Produto cadastrado com sucesso', 'success');
            registerForm.reset();
          } else {
            showNotification(result1.message || 'Erro ao cadastrar produto', 'error');
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

    // setTimeout(() => {
    //   notification.textContent = '';
    //   notification.classList.remove(type, 'show');
    // }, 5000);
  }
});
