document.addEventListener('DOMContentLoaded', () => {
  fetchMembros();
  fetchProdutos();
  fetchServicos();

  const filtroSelect = document.getElementById("filtro");
  const membrosTableBody = document.querySelector("#membrosTable tbody");

  // Adiciona um evento de mudança ao seletor de filtro
  if (filtroSelect && membrosTableBody) {
    filtroSelect.addEventListener("change", function () {
      const filtroValue = filtroSelect.value.toLowerCase(); // Obtém o valor selecionado e converte para minúsculas

      if (filtroValue === 'cargo' || filtroValue === 'nome') {
        const linhas = Array.from(membrosTableBody.querySelectorAll("tr"));
        linhas.sort(function (a, b) {
          let valueA, valueB;
          if (filtroValue === 'cargo') {
            valueA = a.querySelector("td:nth-child(4)").textContent.toLowerCase();
            valueB = b.querySelector("td:nth-child(4)").textContent.toLowerCase();
          } else { // Se selecionado 'nome'
            valueA = a.querySelector("td:first-child").textContent.toLowerCase();
            valueB = b.querySelector("td:first-child").textContent.toLowerCase();
          }
          if (valueA < valueB) return -1;
          if (valueA > valueB) return 1;
          return 0;
        });

        linhas.forEach(function (linha) {
          membrosTableBody.appendChild(linha);
        });
      }
    });
  }

  // setupDeleteHandler("#membrosTable tbody", 'users');
  // setupDeleteHandler("#productTable tbody", 'products');
});

function fetchMembros() {
  fetch('http://127.0.0.1:8000/users/')
    .then(response => response.json())
    .then(data => {
      const membrosTableBody = document.getElementById('membrosTable').querySelector('tbody');
      membrosTableBody.innerHTML = '';
      console.log(data);
      data.forEach(membro => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${membro.name}</td>
          <td>${membro.email}</td>
          <td>${membro.password}</td>
          <td>${membro.role_id}</td>
        `;
        membrosTableBody.appendChild(row);
      });
      // Ordena as linhas após os dados serem inseridos
      ordenarPorNome();
    })
    .catch(error => console.error('Erro ao buscar membros:', error));
}

function fetchProdutos() {
  fetch('http://127.0.0.1:8000/products/')
    .then(response => response.json())
    .then(data => {
      const productTableBody = document.getElementById('productTable').querySelector('tbody');
      productTableBody.innerHTML = '';
      data.forEach(produto => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${produto.title}</td>
          <td>${produto.description}</td>
          <td>${produto.value}</td>
          <td>${produto.id}</td>
        `;
        productTableBody.appendChild(row);
      });
    })
    .catch(error => console.error('Erro ao buscar produtos:', error));
}


function fetchServicos() {
  fetch('http://127.0.0.1:8000/services/')
    .then(response => response.json())
    .then(data => {
      const servicosTableBody = document.getElementById('tabela-servico').querySelector('tbody');
      servicosTableBody.innerHTML = '';
      data.forEach(servico => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${servico.title}</td>
          <td>${servico.description}</td>
          <td>${servico.value}</td>
          <td>${servico.id}</td>
        `;
        servicosTableBody.appendChild(row);
      });
    })
    .catch(error => console.error('Erro ao buscar serviços:', error));
}



// Função para ordenar as linhas da tabela com base no nome do membro
function ordenarPorNome() {
  const tabelaBody = document.querySelector("#membrosTable tbody");
  const linhas = Array.from(tabelaBody.querySelectorAll("tr"));
  linhas.sort(function (a, b) {
    const nomeA = a.querySelector("td:first-child").textContent.toLowerCase();
    const nomeB = b.querySelector("td:first-child").textContent.toLowerCase();
    if (nomeA < nomeB) return -1;
    if (nomeA > nomeB) return 1;
    return 0;
  });
  linhas.forEach(function (linha) {
    tabelaBody.appendChild(linha);
  });
}



function showNotification(message, type, notificationElement) {
  notificationElement.textContent = message;
  notificationElement.className = 'notification ' + type + ' show';

  setTimeout(() => {
    notificationElement.className = 'notification';
  }, 5000);
}




document.addEventListener("DOMContentLoaded", function () {
  const tbodyMembros = document.querySelector("#membrosTable tbody");
  const excluirBtnMembros = document.querySelector(".excluirBtn");
  const deleteNotification = document.getElementById('deleteNotification');
  const cancelNotification = document.getElementById('cancelNotification');

  const tbodyProdutos = document.querySelector("#productTable tbody");
  const excluirBtnProdutos = document.querySelector(".excluirBtnP");
  const deleteNotificationP = document.getElementById('deleteNotificationP');
  const cancelNotificationP = document.getElementById('cancelNotificationP');

  const tbodyServicos = document.querySelector("#serviceTable tbody");
  const excluirBtnServicos = document.querySelector(".excluirBtnS");
  const deleteNotificationS = document.getElementById('deleteNotificationS');
  const cancelNotificationS = document.getElementById('cancelNotificationS');

  if (excluirBtnMembros && tbodyMembros) {
    tbodyMembros.addEventListener("click", function (event) {
      const target = event.target;
      if (target.tagName === "TD") {
        const row = target.closest("tr");
        const rows = tbodyMembros.querySelectorAll("tr");
        rows.forEach((row) => row.classList.remove("selected"));
        row.classList.add("selected");
      }
    });

    excluirBtnMembros.addEventListener("click", async function () {
      const selectedRow = tbodyMembros.querySelector("tr.selected");
      if (selectedRow) {
        if (confirm("Tem certeza de que deseja excluir este membro?")) {
          const login = selectedRow.querySelector("td:nth-child(2)").textContent;
          const senha = selectedRow.querySelector("td:nth-child(3)").textContent;

          try {
            const response = await fetch(`http://127.0.0.1:8000/users/delete/${login}/${senha}`, {
              method: 'DELETE'
            });

            if (response.ok) {
              selectedRow.remove();
              showNotification('Membro excluído com sucesso!', 'success', deleteNotification);
            } else {
              const result = await response.json();
              showNotification(result.message, 'error', deleteNotification);
            }
          } catch (error) {
            showNotification('Erro ao excluir membro', 'error', deleteNotification);
          }
        } else {
          showNotification('Ação de exclusão cancelada!', 'error', cancelNotification);
        }
      } else {
        alert("Por favor, selecione um Membro para excluir.");
      }
    });
  } else {
    console.error("Elemento não encontrado.");
  }

  if (excluirBtnProdutos && tbodyProdutos) {
    tbodyProdutos.addEventListener("click", function (event) {
      const target = event.target;
      if (target.tagName === "TD") {
        const row = target.closest("tr");
        const rows = tbodyProdutos.querySelectorAll("tr");
        rows.forEach((row) => row.classList.remove("selected"));
        row.classList.add("selected");
      }
    });

    excluirBtnProdutos.addEventListener("click", async function () {
      const selectedRow = tbodyProdutos.querySelector("tr.selected");
      if (selectedRow) {
        if (confirm("Tem certeza de que deseja excluir este produto?")) {
          const idProduto = selectedRow.querySelector("td:nth-child(4)").textContent;

          try {
            const response = await fetch(`http://127.0.0.1:8000/products/delete/${idProduto}`, {
              method: 'DELETE'
            });

            if (response.ok) {
              selectedRow.remove();
              showNotification('Produto excluído com sucesso!', 'success', deleteNotificationP);
            } else {
              const result = await response.json();
              showNotification(result.message, 'error', deleteNotificationP);
            }
          } catch (error) {
            showNotification('Erro ao excluir produto', 'error', deleteNotificationP);
          }
        } else {
          showNotification('Ação de exclusão cancelada!', 'error', cancelNotificationP);
        }
      } else {
        alert("Por favor, selecione um Produto para excluir.");
      }
    });
  } else {
    console.error("Elemento não encontrado.");
  }

  if (excluirBtnServicos && tbodyServicos) {
    tbodyServicos.addEventListener("click", function (event) {
      const target = event.target;
      if (target.tagName === "TD") {
        const row = target.closest("tr");
        const rows = tbodyServicos.querySelectorAll("tr");
        rows.forEach((row) => row.classList.remove("selected"));
        row.classList.add("selected");
      }
    });

    excluirBtnServicos.addEventListener("click", async function () {
      const selectedRow = tbodyServicos.querySelector("tr.selected");
      if (selectedRow) {
        if (confirm("Tem certeza de que deseja excluir este serviço?")) {
          const idServico = selectedRow.querySelector("td:nth-child(4)").textContent;

          try {
            const response = await fetch(`http://127.0.0.1:8000/services/delete/${idServico}`, {
              method: 'DELETE'
            });

            if (response.ok) {
              selectedRow.remove();
              showNotification('Serviço excluído com sucesso!', 'success', deleteNotificationS);
            } else {
              const result = await response.json();
              showNotification(result.message, 'error', deleteNotificationS);
            }
          } catch (error) {
            showNotification('Erro ao excluir serviço', 'error', deleteNotificationS);
          }
        } else {
          showNotification('Ação de exclusão cancelada!', 'error', cancelNotificationS);
        }
      } else {
        alert("Por favor, selecione um Serviço para excluir.");
      }
    });
  } else {
    console.error("Elemento não encontrado.");
  }

  function showNotification(message, type, notificationElement) {
    notificationElement.textContent = message;
    notificationElement.className = 'notification ' + type + ' show';

    setTimeout(() => {
      notificationElement.className = 'notification';
    }, 5000);
  }
});



