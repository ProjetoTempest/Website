document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.querySelector("#membrosTable tbody");
  const excluirBtn = document.querySelector(".excluirBtn");

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
        }
      } else {
        alert("Por favor, selecione um membro para excluir.");
      }
    });
  } else {
    console.error("Elemento não encontrado.");
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
});







document.addEventListener("DOMContentLoaded", function () {
  const tbody = document.querySelector("#productTable tbody");
  const excluirBtn = document.querySelector(".excluirBtnP");

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
              }
          } else {
              alert("Por favor, selecione um produto para excluir.");
          }
      });
  } else {
      console.error("Elemento não encontrado.");
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
});
