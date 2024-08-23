document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById('registerForm');
    const notification = document.getElementById('notification');
    const tbody = document.querySelector('tbody');

    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            if (confirm('Tem certeza de que deseja cadastrar este serviço?')) {
                const title = document.getElementById('nameservice').value; // Alterado para 'title'
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

                        if (!responImg.ok) {
                            const result = await responImg.json();
                            showNotification(result.message || 'Erro ao enviar imagens', 'error');
                            return;
                        }

                        const resultImg = await responImg.json();
                        const images = resultImg.map(imageDict => ({ url: imageDict.url }));

                        const serviceData = {
                            "title": title,
                            "description": description,
                            "value": value,
                            "images": images
                        };

                        const response = await fetch('http://127.0.0.1:8000/services/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(serviceData)
                        });

                        const result = await response.json();

                        if (response.ok) {
                            showNotification('Serviço cadastrado com sucesso', 'success');
                            registerForm.reset();
                        } else {
                            showNotification(result.message || 'Erro ao cadastrar serviço', 'error');
                        }
                    } catch (error) {
                        showNotification('Erro ao cadastrar serviço', 'error');
                    }
                } else {
                    showNotification('Preencha todos os campos', 'error');
                }
            } else {
                showNotification('Cadastro cancelado.', 'error');
            }
        });
    } else {
        console.error('Elemento registerForm não encontrado');
    }

    function showNotification(message, type) {
        if (notification) {
            notification.textContent = message;
            notification.classList.add(type, 'show');

            setTimeout(() => {
                notification.textContent = '';
                notification.classList.remove(type, 'show');
            }, 5000);
        } else {
            console.error('Elemento notification não encontrado');
        }
    }

    function addServiceToTable(service) {
        const { title, description, value } = service;
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${title}</td>
            <td>${description}</td>
            <td>${value}</td>
        `;
        tbody.appendChild(newRow);
    }

    async function loadServices() {
        tbody.innerHTML = ''; // Limpa a tabela

        try {
            const response = await fetch('http://127.0.0.1:8000/services'); // Ajuste a URL conforme necessário
            const services = await response.json();

            services.forEach(service => {
                addServiceToTable(service);
            });
        } catch (error) {
            showNotification('Erro ao carregar serviços', 'error');
        }
    }

    if (tbody) {
        tbody.addEventListener('click', async (e) => {
            if (e.target.classList.contains('delete-btn')) {
                const row = e.target.parentElement.parentElement;
                const id = row.children[0].textContent; // Obtém o id do serviço, ajuste conforme necessário

                try {
                    const response = await fetch(`http://127.0.0.1:8000/services/${id}`, {
                        method: 'DELETE'
                    });

                    if (response.ok) {
                        row.remove();
                        showNotification('Serviço excluído com sucesso!', 'success');
                    } else {
                        const result = await response.json();
                        showNotification(result.message || 'Erro ao excluir serviço', 'error');
                    }
                } catch (error) {
                    showNotification('Erro ao excluir serviço', 'error');
                }
            }
        });

        loadServices();
    } else {
        console.error('Elemento tbody não encontrado');
    }
});
