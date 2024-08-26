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
          <td>${membro.id}</td>
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




// Edição menbro

document.addEventListener("DOMContentLoaded", function () {
  const tabelaBody = document.querySelector("#membrosTable tbody");
  const editarBtn = document.querySelector(".editarBtn");
  const confirmarBtn = document.querySelector(".confirmarBtn");
  const notification = document.getElementById('notification');
  let editing = false; // Flag para indicar se a edição está habilitada
  let clickCount = 0; // Contador de cliques

  // Função para desmarcar a linha selecionada
  function deselecionarLinha() {
    tabelaBody.querySelectorAll("tr.selected").forEach(row => row.classList.remove("selected"));
  }

  // Adiciona evento de clique para o botão de "Editar Membro"
  editarBtn.addEventListener("click", function () {
    const selectedRow = document.querySelector("tr.selected"); // Obtém a linha selecionada

    if (selectedRow) {
      if (!editing) {
        const cells = selectedRow.querySelectorAll("td");
        cells.forEach(function (cell) {
          cell.contentEditable = true; // Torna as células editáveis
          cell.style.border = "1px solid #000"; // Adiciona uma borda para indicar edição
        });

        editing = true; // Define a flag como true
        // Exibe o botão de "Confirmar Edição" e oculta o botão de "Editar Membro"
        confirmarBtn.style.display = "inline-block";
        editarBtn.style.display = "none";
      }
    } else {
      alert("Por favor, selecione um Membro para editar.");
    }
  });

  // Adiciona evento de clique para o botão de "Confirmar Edição"
  confirmarBtn.addEventListener("click", async function () {
    const selectedRow = document.querySelector("tr.selected"); // Obtém a linha selecionada

    if (selectedRow) {
      const cells = selectedRow.querySelectorAll("td");
      const memberData = {
        name: cells[0].textContent,
        login: cells[1].textContent,
        password: cells[2].textContent,
        id: cells[3].textContent
      };

      try {
        const response = await fetch(`http://127.0.0.1:8000/users/update_user/${memberData.id}`, { 
          method: 'PUT', // ou 'PATCH' dependendo da implementação da API
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(memberData)
        });

        const result = await response.json();
        if (response.ok) {
          showNotification('Membro atualizado com sucesso!', 'success');
          cells.forEach(function (cell) {
            cell.contentEditable = false; // Torna as células não editáveis
            cell.style.border = "none"; // Remove a borda
          });
          editing = false; // Define a flag como false
          // Oculta o botão de "Confirmar Edição" e exibe o botão de "Editar Membro"
          confirmarBtn.style.display = "none";
          editarBtn.style.display = "inline-block";
        } else {
          showNotification(result.message, 'error');
        }
      } catch (error) {
        showNotification('Erro ao atualizar membro', 'error');
      }
    } else {
      alert("Por favor, selecione um Membro para editar.");
    }
  });

  // Adiciona evento de clique para as linhas da tabela
  tabelaBody.addEventListener("click", function (event) {
    const targetRow = event.target.closest("tr"); // Obtém a linha clicada

    if (targetRow) {
      clickCount++; // Incrementa o contador de cliques
      // Se o contador de cliques atingir 3, desmarca a linha selecionada e reinicia o contador
      if (clickCount === 3) {
        deselecionarLinha();
        clickCount = 0;
      } else {
        // Remove a classe de seleção de todas as linhas
        deselecionarLinha();
        // Adiciona a classe de seleção à linha clicada
        targetRow.classList.add("selected");
      }
    }
  });

  function showNotification(message, type) {
    notification.textContent = message;
    notification.className = 'notification ' + type + ' show';

    setTimeout(() => {
      notification.className = 'notification';
    }, 5000);
  }
});


// Edição produto

document.addEventListener("DOMContentLoaded", function () {
  const tabelaBody = document.querySelector("#productTable tbody");
  const editarBtn = document.querySelector(".editarBtnP");
  const confirmarBtn = document.querySelector(".confirmarBtnP");
  let editing = false; // Flag para indicar se a edição está habilitada
  let clickCount = 0; // Contador de cliques

  // Função para desmarcar a linha selecionada
  function deselecionarLinha() {
      tabelaBody.querySelectorAll("tr.selected").forEach(row => row.classList.remove("selected"));
  }

  // Adiciona evento de clique para o botão de "Editar Produto"
  editarBtn.addEventListener("click", function () {
      const selectedRow = document.querySelector("tr.selected"); // Obtém a linha selecionada

      if (selectedRow) {
          if (!editing) {
              const cells = selectedRow.querySelectorAll("td");
              cells.forEach(function (cell) {
                  cell.contentEditable = true; // Torna as células editáveis
                  cell.style.border = "1px solid #000"; // Adiciona uma borda para indicar edição
              });

              editing = true; // Define a flag como true
              // Exibe o botão de "Confirmar Edição" e oculta o botão de "Editar Produto"
              confirmarBtn.style.display = "inline-block";
              editarBtn.style.display = "none";
          }
      }
  });

  // Adiciona evento de clique para o botão de "Confirmar Edição"
  confirmarBtn.addEventListener("click", async function () {
      const selectedRow = document.querySelector("tr.selected"); // Obtém a linha selecionada

      if (selectedRow) {
          const cells = selectedRow.querySelectorAll("td");
          const updatedProduct = {
              title: cells[0].textContent,
              description: cells[1].textContent,
              value: cells[2].textContent,
              id: cells[3].textContent
          };

          try {
              const response = await fetch(`http://127.0.0.1:8000/products/update/${updatedProduct.id}`, { // Ajuste a URL conforme necessário
                  method: 'PUT',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: JSON.stringify(updatedProduct)
              });

              if (response.ok) {
                  cells.forEach(function (cell) {
                      cell.contentEditable = false; // Torna as células não editáveis
                      cell.style.border = "none"; // Remove a borda
                  });

                  editing = false; // Define a flag como false
                  // Oculta o botão de "Confirmar Edição" e exibe o botão de "Editar Produto"
                  confirmarBtn.style.display = "none";
                  editarBtn.style.display = "inline-block";
                  showNotification('Produto editado com sucesso!', 'success');
              } else {
                  const result = await response.json();
                  showNotification(result.message, 'error');
              }
          } catch (error) {
              showNotification('Erro ao editar produto', 'error');
          }
      }
  });

  // Adiciona evento de clique para as linhas da tabela
  tabelaBody.addEventListener("click", function (event) {
      const targetRow = event.target.closest("tr"); // Obtém a linha clicada

      if (targetRow) {
          clickCount++; // Incrementa o contador de cliques
          // Se o contador de cliques atingir 3, desmarca a linha selecionada e reinicia o contador
          if (clickCount === 3) {
              deselecionarLinha();
              clickCount = 0;
          } else {
              // Remove a classe de seleção de todas as linhas
              deselecionarLinha();
              // Adiciona a classe de seleção à linha clicada
              targetRow.classList.add("selected");
          }
      }
  });

  function showNotification(message, type) {
      const notificationElement = document.getElementById('notification');
      notificationElement.textContent = message;
      notificationElement.className = 'notification ' + type + ' show';

      setTimeout(() => {
          notificationElement.className = 'notification';
      }, 5000);
  }
});


// Edição serviço

document.addEventListener("DOMContentLoaded", function () {
  const tabelaBody = document.querySelector("#serviceTable tbody");
  const editarBtn = document.querySelector(".editarBtnS");
  const confirmarBtn = document.querySelector(".confirmarBtnS");
  let editing = false;
  let clickCount = 0;

  function deselecionarLinha() {
    tabelaBody.querySelectorAll("tr.selected").forEach(row => row.classList.remove("selected"));
  }

  editarBtn.addEventListener("click", function () {
    const selectedRow = document.querySelector("tr.selected");

    if (selectedRow) {
      if (!editing) {
        const cells = selectedRow.querySelectorAll("td");
        cells.forEach(function (cell) {
          cell.contentEditable = true;
          cell.style.border = "1px solid #000";
        });

        editing = true;
        confirmarBtn.style.display = "inline-block";
        editarBtn.style.display = "none";
      }
    }
  });

  confirmarBtn.addEventListener("click", async function () {
    const selectedRow = document.querySelector("tr.selected");

    if (selectedRow) {
      const cells = selectedRow.querySelectorAll("td");
      const updatedService = {
        title: cells[0].textContent,
        description: cells[1].textContent,
        value: cells[2].textContent,
        id: cells[3].textContent
      };

      try {
        const response = await fetch(`http://127.0.0.1:8000/services/update/${updatedService.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(updatedService)
        });

        if (response.ok) {
          cells.forEach(function (cell) {
            cell.contentEditable = false;
            cell.style.border = "none";
          });

          editing = false;
          confirmarBtn.style.display = "none";
          editarBtn.style.display = "inline-block";
          showNotification('Serviço editado com sucesso!', 'success');
        } else {
          const result = await response.json();
          showNotification(result.message, 'error');
        }
      } catch (error) {
        showNotification('Erro ao editar serviço', 'error');
      }
    }
  });

  tabelaBody.addEventListener("click", function (event) {
    const targetRow = event.target.closest("tr");

    if (targetRow) {
      clickCount++;
      if (clickCount === 3) {
        deselecionarLinha();
        clickCount = 0;
      } else {
        deselecionarLinha();
        targetRow.classList.add("selected");
      }
    }
  });

  function showNotification(message, type) {
    const notificationElement = document.getElementById('notification');
    notificationElement.textContent = message;
    notificationElement.className = 'notification ' + type + ' show';

    setTimeout(() => {
      notificationElement.className = 'notification';
    }, 5000);
  }
});