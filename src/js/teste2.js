document.addEventListener('DOMContentLoaded', () => {
  fetchMembros();
  fetchProdutos();
});

function fetchMembros() {
  fetch('/api/membros')
    .then(response => response.json())
    .then(data => {
      const membrosTableBody = document.getElementById('membrosTable').querySelector('tbody');
      membrosTableBody.innerHTML = ''; 
      data.forEach(membro => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${membro.nome}</td>
          <td>${membro.login}</td>
          <td>${membro.senha}</td>
          <td>${membro.cargo}</td>
        `;
        membrosTableBody.appendChild(row);
      });
    })
    .catch(error => console.error('Erro ao buscar membros:', error));
}

function fetchProdutos() {
  fetch('/api/produtos')
    .then(response => response.json())
    .then(data => {
      const productTableBody = document.getElementById('productTable').querySelector('tbody');
      productTableBody.innerHTML = ''; 
      data.forEach(produto => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${produto.nome}</td>
          <td>${produto.descricao}</td>
          <td>${produto.valor}</td>
          <td>${produto.imagem}</td>
        `;
        productTableBody.appendChild(row);
      });
    })
    .catch(error => console.error('Erro ao buscar produtos:', error));
}


function fetchServicos() {
  fetch('/api/servicos')
    .then(response => response.json())
    .then(data => {
      const servicosTableBody = document.getElementById('servicosTable').querySelector('tbody');
      servicosTableBody.innerHTML = '';
      data.forEach(servico => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${servico.nome}</td>
          <td>${servico.descricao}</td>
          <td>${servico.valor}</td>
        `;
        servicosTableBody.appendChild(row);
      });
    })
    .catch(error => console.error('Erro ao buscar serviços:', error));
}