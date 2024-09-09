/*document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.querySelector("#membrosTable tbody");
  const excluirBtn = document.querySelector(".excluirBtn");
  const deleteNotification = document.getElementById('deleteNotification');
  const cancelNotification = document.getElementById('cancelNotification');

  if (excluirBtn && tbody) {
    tbody.addEventListener("click", function (event) {
      const target = event.target;
      if (target.tagName === "TD") {
        const row = target.closest("tr");
        const rows = tbody.querySelectorAll("tr");
        rows.forEach((row) => row.classList.remove("selected"));
        row.classList.add("selected");
      }
    });

    excluirBtn.addEventListener("click", function () {
      const selectedRow = tbody.querySelector("tr.selected");
      if (selectedRow) {
        if (confirm("Tem certeza de que deseja excluir este membro?")) {
          selectedRow.remove();
          deleteNotification.textContent = 'Membro excluído com sucesso!';
          deleteNotification.className = 'notification success show';
          setTimeout(() => {
            deleteNotification.className = 'notification';
          }, 5000);
        } else {
          cancelNotification.textContent = 'Ação de exclusão cancelada!';
          cancelNotification.className = 'notification error show';
          setTimeout(() => {
            cancelNotification.className = 'notification';
          }, 5000);
        }
      } else {
        alert("Por favor, selecione um Membro para excluir.");
      }
    });
  } else {
    console.error("Elemento não encontrado.");
  }
});*/

document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.querySelector("#membrosTable tbody");
  const excluirBtn = document.querySelector(".excluirBtn");
  const deleteNotification = document.getElementById('deleteNotification');
  const cancelNotification = document.getElementById('cancelNotification');

  if (excluirBtn && tbody) {
    tbody.addEventListener("click", function (event) {
      const target = event.target;
      if (target.tagName === "TD") {
        const row = target.closest("tr");
        const rows = tbody.querySelectorAll("tr");
        rows.forEach((row) => row.classList.remove("selected"));
        row.classList.add("selected");
      }
    });

    excluirBtn.addEventListener("click", async function () {
      const selectedRow = tbody.querySelector("tr.selected");
      if (selectedRow) {
        if (confirm("Tem certeza de que deseja excluir este membro?")) {
          const login = selectedRow.querySelector("td:nth-child(2)").textContent;

          try {
            const response = await fetch(`https://api.seuservidor.com/members/${login}`, {
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

  function showNotification(message, type, notificationElement) {
    notificationElement.textContent = message;
    notificationElement.className = 'notification ' + type + ' show';

    setTimeout(() => {
      notificationElement.className = 'notification';
    }, 5000);
  }
});


document.addEventListener("DOMContentLoaded", function () {
  const filtroSelect = document.getElementById("filtro");
  const tabelaBody = document.querySelector("#membrosTable tbody");

  // Função para ordenar as linhas da tabela com base no nome do membro
  function ordenarPorNome() {
    const linhas = Array.from(tabelaBody.querySelectorAll("tr"));
    linhas.sort(function (a, b) {
      const nomeA = a.querySelector("td:first-child").textContent.toLowerCase();
      const nomeB = b.querySelector("td:first-child").textContent.toLowerCase();
      if (nomeA < nomeB) return -1;
      if (nomeA > nomeB) return 1;
      return 0;
    });
    linhas.forEach(function (linha) {
      tabelaBody.removeChild(linha);
    });
    linhas.forEach(function (linha) {
      tabelaBody.appendChild(linha);
    });
  }

  // Ordena inicialmente as linhas da tabela pelo nome do membro
  ordenarPorNome();

  // Adiciona um evento de mudança ao seletor de filtro
  filtroSelect.addEventListener("change", function () {
    const filtroValue = filtroSelect.value.toLowerCase(); // Obtém o valor selecionado e converte para minúsculas

    if (filtroValue === 'cargo' || filtroValue === 'nome') {
      const linhas = Array.from(tabelaBody.querySelectorAll("tr"));
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
        tabelaBody.removeChild(linha);
      });

      linhas.forEach(function (linha) {
        tabelaBody.appendChild(linha);
      });
    }
  });
});

/*
document.addEventListener("DOMContentLoaded", function () {
  const tabelaBody = document.querySelector("#membrosTable tbody");
  const editarBtn = document.querySelector(".editarBtn");
  const confirmarBtn = document.querySelector(".confirmarBtn");
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
      }
  });

  // Adiciona evento de clique para o botão de "Confirmar Edição"
  confirmarBtn.addEventListener("click", function () {
      const selectedRow = document.querySelector("tr.selected"); // Obtém a linha selecionada

      if (selectedRow) {
          const cells = selectedRow.querySelectorAll("td");
          cells.forEach(function (cell) {
              cell.contentEditable = false; // Torna as células não editáveis
              cell.style.border = "none"; // Remove a borda
          });

          editing = false; // Define a flag como false
          // Oculta o botão de "Confirmar Edição" e exibe o botão de "Editar Membro"
          confirmarBtn.style.display = "none";
          editarBtn.style.display = "inline-block";
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
});*/

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
        role: cells[3].textContent
      };

      try {
        const response = await fetch(`https://api.seuservidor.com/members/${memberData.login}`, { 
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


/*document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.querySelector("#productTable tbody");
  const excluirBtn = document.querySelector(".excluirBtnP");
  const deleteNotification = document.getElementById('deleteNotification');
  const cancelNotification = document.getElementById('cancelNotification');

  if (excluirBtn && tbody) {
    tbody.addEventListener("click", function (event) {
      const target = event.target;
      if (target.tagName === "TD") {
        const row = target.closest("tr");
        const rows = tbody.querySelectorAll("tr");
        rows.forEach((row) => row.classList.remove("selected"));
        row.classList.add("selected");
      }
    });

    excluirBtn.addEventListener("click", function () {
      const selectedRow = tbody.querySelector("tr.selected");
      if (selectedRow) {
        if (confirm("Tem certeza de que deseja excluir este produto?")) {
          selectedRow.remove();
          deleteNotification.textContent = 'Produto excluído com sucesso!';
          deleteNotification.className = 'notification success show';
          setTimeout(() => {
            deleteNotification.className = 'notification';
          }, 5000);
        } else {
          cancelNotification.textContent = 'Ação de exclusão cancelada!';
          cancelNotification.className = 'notification error show';
          setTimeout(() => {
            cancelNotification.className = 'notification';
          }, 5000);
        }
      } else {
        alert("Por favor, selecione um produto para excluir.");
      }
    });
  } else {
    console.error("Elemento não encontrado.");
  }
});
*/

document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.querySelector("#productTable tbody");
  const excluirBtn = document.querySelector(".excluirBtnP");
  const deleteNotification = document.getElementById('deleteNotification');
  const cancelNotification = document.getElementById('cancelNotification');

  if (excluirBtn && tbody) {
    tbody.addEventListener("click", function (event) {
      const target = event.target;
      if (target.tagName === "TD") {
        const row = target.closest("tr");
        const rows = tbody.querySelectorAll("tr");
        rows.forEach((row) => row.classList.remove("selected"));
        row.classList.add("selected");
      }
    });

    excluirBtn.addEventListener("click", async function () {
      const selectedRow = tbody.querySelector("tr.selected");
      if (selectedRow) {
        if (confirm("Tem certeza de que deseja excluir este produto?")) {
          const productName = selectedRow.querySelector("td:nth-child(1)").textContent; // Supondo que a primeira coluna seja o nome do produto

          try {
            const response = await fetch(`https://api.seuservidor.com/products/${productName}`, { // Ajuste a URL conforme necessário
              method: 'DELETE'
            });

            if (response.ok) {
              selectedRow.remove();
              showNotification('Produto excluído com sucesso!', 'success', deleteNotification);
            } else {
              const result = await response.json();
              showNotification(result.message, 'error', deleteNotification);
            }
          } catch (error) {
            showNotification('Erro ao excluir produto', 'error', deleteNotification);
          }
        } else {
          showNotification('Ação de exclusão cancelada!', 'error', cancelNotification);
        }
      } else {
        alert("Por favor, selecione um produto para excluir.");
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



document.addEventListener("DOMContentLoaded", function () {
  const filtroSelect = document.getElementById("filtro");
  const tabelaBody = document.querySelector("#productTable tbody");

  // Função para ordenar as linhas da tabela com base no nome do produto
  function ordenarPorNome() {
      const linhas = Array.from(tabelaBody.querySelectorAll("tr"));
      linhas.sort(function (a, b) {
          const nomeA = a.querySelector("td:first-child").textContent.toLowerCase();
          const nomeB = b.querySelector("td:first-child").textContent.toLowerCase();
          if (nomeA < nomeB) return -1;
          if (nomeA > nomeB) return 1;
          return 0;
      });
      linhas.forEach(function (linha) {
          tabelaBody.removeChild(linha);
      });
      linhas.forEach(function (linha) {
          tabelaBody.appendChild(linha);
      });
  }

  // Ordena inicialmente as linhas da tabela pelo nome do produto
  ordenarPorNome();
  
});

/*document.addEventListener("DOMContentLoaded", function () {
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
  confirmarBtn.addEventListener("click", function () {
      const selectedRow = document.querySelector("tr.selected"); // Obtém a linha selecionada

      if (selectedRow) {
          const cells = selectedRow.querySelectorAll("td");
          cells.forEach(function (cell) {
              cell.contentEditable = false; // Torna as células não editáveis
              cell.style.border = "none"; // Remove a borda
          });

          editing = false; // Define a flag como false
          // Oculta o botão de "Confirmar Edição" e exibe o botão de "Editar Produto"
          confirmarBtn.style.display = "none";
          editarBtn.style.display = "inline-block";
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
});*/

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
              name: cells[0].textContent,
              description: cells[1].textContent,
              price: cells[2].textContent,
              image: cells[3].textContent
          };

          try {
              const response = await fetch(`https://api.seuservidor.com/products/${updatedProduct.name}`, { // Ajuste a URL conforme necessário
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


/*document.addEventListener("DOMContentLoaded", function () {
  const productTable = document.getElementById('productTable').querySelector('tbody');

  // Recuperar produtos do localStorage
  const products = JSON.parse(localStorage.getItem('products')) || [];

  // Adicionar cada produto à tabela
  products.forEach(product => {
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
      <td>${product.name}</td>
      <td>${product.description}</td>
      <td>${product.price}</td>
      <td><img src="../../path/to/images/${product.image}" alt="${product.name}" style="width:50px;height:50px;"></td>
    `;
    productTable.appendChild(newRow);
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.querySelector("#membrosTable tbody");

  // Recuperar membros do localStorage
  const members = JSON.parse(localStorage.getItem('members')) || [];

  // Adicionar cada membro à tabela
  members.forEach(member => {
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
      <td>${member.name}</td>
      <td>${member.login}</td>
      <td>${member.password}</td>
      <td>${member.role}</td>
    `;
    tbody.appendChild(newRow);
  });
});
*/

document.addEventListener("DOMContentLoaded", async function () {
  const productTable = document.getElementById('productTable').querySelector('tbody');

  try {
    const response = await fetch('https://api.seuservidor.com/products'); 
    const products = await response.json();

    // Adicionar cada produto à tabela
    products.forEach(product => {
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td>${product.name}</td>
        <td>${product.description}</td>
        <td>${product.price}</td>
        <td><img src="https://api.seuservidor.com/images/${product.image}" alt="${product.name}" style="width:50px;height:50px;"></td>
      `;
      productTable.appendChild(newRow);
    });
  } catch (error) {
    console.error('Erro ao carregar produtos:', error);
  }
});

document.addEventListener("DOMContentLoaded", async function () {
  const tbody = document.querySelector("#membrosTable tbody");

  try {
    const response = await fetch('https://api.seuservidor.com/members');
    const members = await response.json();

    // Adicionar cada membro à tabela
    members.forEach(member => {
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td>${member.name}</td>
        <td>${member.login}</td>
        <td>${member.password}</td>
        <td>${member.role}</td>
      `;
      tbody.appendChild(newRow);
    });
  } catch (error) {
    console.error('Erro ao carregar membros:', error);
  }
});







