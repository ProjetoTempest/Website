document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById('registerForm');
    const notification = document.getElementById('notification');
    const tbody = document.querySelector('tbody');

    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            if (confirm('Tem certeza de que deseja cadastrar este serviço?')) {
                const name = document.getElementById('nameservice').value;
                const description = document.getElementById('description').value;
                const price = document.getElementById('price').value;

                if (name && description && price) {
                    const formData = new FormData();
                    formData.append('title', name);
                    formData.append('description', description);
                    formData.append('value', price);

                    try {
                        const response = await fetch('http://127.0.0.1:8000/services/', {
                            method: 'POST',
                            body: formData
                        });

                        const result = await response.json();
                        if (response.ok) {
                            showNotification('Serviço cadastrado com sucesso', 'success');
                            registerForm.reset();
                        } else {
                            showNotification(result.message, 'error');
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

    // Função para adicionar um serviço à tabela
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

    // Carrega os serviços do banco de dados ao carregar a página
    async function loadServices() {
        tbody.innerHTML = ''; // Limpa a tabela

        try {
            const response = await fetch('http://127.0.0.1:8000/services'); // Ajuste a URL conforme necessário
            const services = await response.json();

            services.forEach(service => {
                addServiceToTable(service);
            });
        } catch (error) {
            showNotification('Erro ao carregar serviços', 'notification error show');
        }
    }

    if (tbody) {
        // Event listener para excluir serviços
        tbody.addEventListener('click', async (e) => {
            if (e.target.classList.contains('delete-btn')) {
                const row = e.target.parentElement.parentElement;
                const id = row.children[0].textContent; // Obtém o id do serviço, ajuste conforme necessário

                try {
                    const response = await fetch(`http://127.0.0.1:8000/services/${id}`, { // Ajuste a URL conforme necessário
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
                    showNotification('Erro ao excluir serviço', 'notification error show');
                }
            }
        });

        // Carrega os serviços ao carregar a página
        loadServices();
    } else {
        console.error('Elemento tbody não encontrado');
    }
});
