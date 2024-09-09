/*document.addEventListener("DOMContentLoaded", function () {
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('password');
  const registerForm = document.getElementById('registerForm');
  const notification = document.getElementById('notification');
  const tbody = document.querySelector("#memberTable tbody");

  togglePassword.addEventListener('click', () => {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;

    if (type === 'password') {
      togglePassword.classList.add('fa-eye-slash');
      togglePassword.classList.remove('fa-eye');
    } else {
      togglePassword.classList.remove('fa-eye-slash');
      togglePassword.classList.add('fa-eye');
    }
  });

  registerForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    if (name && login && password && role) {
      // Salva os dados no localStorage
      const member = { name, login, password, role };
      let members = JSON.parse(localStorage.getItem('members')) || [];
      members.push(member);
      localStorage.setItem('members', JSON.stringify(members));

      // Adiciona na tabela de membros
      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td>${name}</td>
        <td>${login}</td>
        <td>${password}</td>
        <td>${role}</td>
      `;
      tbody.appendChild(newRow);

      showNotification('Membro cadastrado com sucesso!', 'notification success show');
      registerForm.reset();
    } else {
      showNotification('Preencha todos os campos', 'error');
    }
  });

  function showNotification(message, type) {
    notification.textContent = message;
    notification.className = 'notification ' + type;
    notification.style.display = 'block';

    setTimeout(() => {
      notification.style.display = 'none';
    }, 5000);
  }

  // Carrega os membros do localStorage ao carregar a página
  loadMembers();

  function loadMembers() {
    tbody.innerHTML = ''; // Limpa a tabela

    const members = JSON.parse(localStorage.getItem('members')) || [];

    members.forEach(member => {
      const { name, login, password, role } = member;

      const newRow = document.createElement('tr');
      newRow.innerHTML = `
        <td>${name}</td>
        <td>${login}</td>
        <td>${password}</td>
        <td>${role}</td>
      `;
      tbody.appendChild(newRow);
    });
  }

  // Event listener para excluir membros
  tbody.addEventListener('click', (e) => {
    if (e.target.classList.contains('delete-btn')) {
      const row = e.target.parentElement.parentElement;
      const login = row.children[1].textContent; // Obtém o login do membro

      // Remove do localStorage
      let members = JSON.parse(localStorage.getItem('members')) || [];
      members = members.filter(member => member.login !== login);
      localStorage.setItem('members', JSON.stringify(members));

      // Remove da tabela
      row.remove();

      showNotification('Membro excluído com sucesso!', 'notification success show');
    }
  });
});*/

document.addEventListener("DOMContentLoaded", function () {
  const togglePassword = document.getElementById('togglePassword');
  const passwordInput = document.getElementById('password');
  const registerForm = document.getElementById('registerForm');
  const notification = document.getElementById('notification');
  const tbody = document.querySelector("#memberTable tbody");

  togglePassword.addEventListener('click', () => {
    const type = passwordInput.type === 'password' ? 'text' : 'password';
    passwordInput.type = type;

    if (type === 'password') {
      togglePassword.classList.add('fa-eye-slash');
      togglePassword.classList.remove('fa-eye');
    } else {
      togglePassword.classList.remove('fa-eye-slash');
      togglePassword.classList.add('fa-eye');
    }
  });

  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value;
    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;
    const role = document.getElementById('role').value;

    if (name && login && password && role) {
      const data = { name, login, password, role };

      try {
        const response = await fetch('https://api.seuservidor.com/register', { 
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.ok) {
        
          addMemberToTable(data);

          showNotification('Membro cadastrado com sucesso!', 'notification success show');
          registerForm.reset();
        } else {
          showNotification(result.message, 'notification error show');
        }
      } catch (error) {
        showNotification('Erro ao registrar usuário', 'notification error show');
      }
    } else {
      showNotification('Preencha todos os campos', 'notification error show');
    }
  });

  function showNotification(message, type) {
    notification.textContent = message;
    notification.className = 'notification ' + type;
    notification.style.display = 'block';

    setTimeout(() => {
      notification.style.display = 'none';
    }, 5000);
  }

  // Função para adicionar um membro à tabela
  function addMemberToTable(member) {
    const { name, login, password, role } = member;
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
      <td>${name}</td>
      <td>${login}</td>
      <td>${password}</td>
      <td>${role}</td>
    `;
    tbody.appendChild(newRow);
  }

  // Carrega os membros do banco de dados ao carregar a página
  loadMembers();

  async function loadMembers() {
    tbody.innerHTML = ''; // Limpa a tabela

    try {
      const response = await fetch('https://api.seuservidor.com/members'); // Ajuste a URL conforme necessário
      const members = await response.json();

      members.forEach(member => {
        addMemberToTable(member);
      });
    } catch (error) {
      showNotification('Erro ao carregar membros', 'notification error show');
    }
  }

  // Event listener para excluir membros
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
          showNotification('Membro excluído com sucesso!', 'notification success show');
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
