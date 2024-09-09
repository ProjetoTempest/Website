document.querySelector('.menu-icon').addEventListener('click', function() {
  document.querySelector('.menu ul').classList.toggle('active');
  document.querySelector('.menu-icon .fa-bars').classList.toggle('active');
  document.querySelector('.menu-icon .fa-times').classList.toggle('active');
});

// Carrossel principal
document.addEventListener("DOMContentLoaded", function () {
  const carrosselContainer = document.querySelector('.carrossel-container');
  const nextButton = document.getElementById('next');
  const prevButton = document.getElementById('prev');

  // Calcula a largura de um card incluindo margens
  const card = document.querySelector('.equipe-container');
  const cardMargin = parseInt(getComputedStyle(card).marginRight);
  const cardWidth = card.clientWidth + cardMargin;

  let currentIndex = 0; // Índice do primeiro card visível

  const updateVisibleCards = () => {
    // Verifica a largura da tela e ajusta os cards visíveis
    return window.innerWidth < 768 ? 1 : Math.floor(carrosselContainer.clientWidth / cardWidth);
  };

  const updateVisible2Cards = () => {
    // Se a largura da tela for menor que 860px, exibir 2 cartões
    return window.innerWidth < 860 ? 2 : Math.floor(carrosselContainer.clientWidth / cardWidth);
  };


  let visibleCards = updateVisibleCards(); // Atualiza com base na largura da tela
  let visible2Cards = updateVisible2Cards();

  const updateButtons = () => {
    // Determina o índice máximo do primeiro card que pode ser mostrado
    const maxIndex = Math.floor((carrosselContainer.scrollWidth - carrosselContainer.clientWidth) / cardWidth);

    // Atualiza o estado dos botões
    prevButton.disabled = currentIndex <= 0;
    nextButton.disabled = currentIndex >= maxIndex;
  };

  const moveCarrossel = (direction) => {
    if (window.innerWidth < 768) {
      visibleCards = updateVisibleCards(); // Atualiza os cards visíveis
      let step = visibleCards;

      if (window.innerWidth < 700) {
        step = (visibleCards + 0.03);
      }
      if (window.innerWidth < 600) {
        step = (visibleCards + 0.04);
      }
      if (window.innerWidth < 500) {
        step = (visibleCards + 0.055);
      }
      if (window.innerWidth < 400) {
        step = (visibleCards + 0.065);
      }
      if (direction === 'next' && currentIndex < Math.floor((carrosselContainer.scrollWidth - carrosselContainer.clientWidth) / cardWidth)) {
        currentIndex += step; // Pula pelo número de cards visíveis
      } else if (direction === 'prev' && currentIndex > 0) {
        currentIndex -= step; // Pula para trás pelo número de cards visíveis
      } 
    } else if (window.innerWidth < 860) {
      visible2Cards = updateVisible2Cards(); 
      let step = (visible2Cards + 0.1);
      if (direction === 'next' && currentIndex < Math.floor((carrosselContainer.scrollWidth - carrosselContainer.clientWidth) / cardWidth)) {
        currentIndex += step; // Pula pelo número de cards visíveis
      } else if (direction === 'prev' && currentIndex > 0) {
        currentIndex -= step; // Pula para trás pelo número de cards visíveis
      } 
    } else {
      visibleCards = updateVisibleCards(); // Atualiza os cards visíveis
      let step = visibleCards;
      if (direction === 'next' && currentIndex < Math.floor((carrosselContainer.scrollWidth - carrosselContainer.clientWidth) / cardWidth)) {
        currentIndex += step; // Pula pelo número de cards visíveis
      } else if (direction === 'prev' && currentIndex > 0) {
        currentIndex -= step; // Pula para trás pelo número de cards visíveis
      } 
    }

    // Move o carrossel para a posição correta
    carrosselContainer.scrollLeft = currentIndex * cardWidth;

    updateButtons(); // Atualiza o estado dos botões
  };

  // Adiciona eventos aos botões
  nextButton.addEventListener('click', () => moveCarrossel('next'));
  prevButton.addEventListener('click', () => moveCarrossel('prev'));

  updateButtons(); // Atualiza inicialmente os botões
});

// Carrossel alternativo para a segunda seção
document.addEventListener("DOMContentLoaded", function () {
  const carrosselContainer = document.querySelector('.carrossel-containerP');
  const nextButton = document.getElementById('nextP');
  const prevButton = document.getElementById('prevP');

  // Calcula a largura de um card incluindo margens
  const card = document.querySelector('.produto-container');
  const cardMargin = parseInt(getComputedStyle(card).marginRight);
  const cardWidth = card.clientWidth + cardMargin;

  let currentIndex = 0; // Índice do primeiro card visível

  const updateVisibleCards = () => {
    // Verifica a largura da tela e ajusta os cards visíveis
    return window.innerWidth < 768 ? 1 : Math.floor(carrosselContainer.clientWidth / cardWidth);
  };

  const updateVisible2Cards = () => {
    // Se a largura da tela for menor que 860px, exibir 2 cartões
    return window.innerWidth < 860 ? 2 : Math.floor(carrosselContainer.clientWidth / cardWidth);
  };

  let visibleCards = updateVisibleCards(); // Atualiza com base na largura da tela

  const updateButtons = () => {
    // Determina o índice máximo do primeiro card que pode ser mostrado
    const maxIndex = Math.floor((carrosselContainer.scrollWidth - carrosselContainer.clientWidth) / cardWidth);

    // Atualiza o estado dos botões
    prevButton.disabled = currentIndex <= 0;
    nextButton.disabled = currentIndex >= maxIndex;
  };

  const moveCarrossel = (direction) => {
    if (window.innerWidth < 768) {
      visibleCards = updateVisibleCards(); // Atualiza os cards visíveis
      let step = visibleCards;

      if (window.innerWidth < 700) {
        step = (visibleCards + 0.03);
      }
      if (window.innerWidth < 600) {
        step = (visibleCards + 0.04);
      }
      if (window.innerWidth < 500) {
        step = (visibleCards + 0.055);
      }
      if (window.innerWidth < 400) {
        step = (visibleCards + 0.065);
      }

      if (direction === 'nextP' && currentIndex < Math.floor((carrosselContainer.scrollWidth - carrosselContainer.clientWidth) / cardWidth)) {
        currentIndex += step; // Pula pelo número de cards visíveis
      } else if (direction === 'prevP' && currentIndex > 0) {
        currentIndex -= step; // Pula para trás pelo número de cards visíveis
      }
    }
    else if (window.innerWidth < 860) {
      visibleCards = updateVisible2Cards(); // Atualiza os cards visíveis
      let step = (visibleCards + 0.1);
      if (direction === 'nextP' && currentIndex < Math.floor((carrosselContainer.scrollWidth - carrosselContainer.clientWidth) / cardWidth)) {
        currentIndex += step; // Pula pelo número de cards visíveis
      } else if (direction === 'prevP' && currentIndex > 0) {
        currentIndex -= step; // Pula para trás pelo número de cards visíveis
      }
    } else {
      visibleCards = updateVisibleCards(); // Atualiza os cards visíveis
      let step = visibleCards;
      if (direction === 'nextP' && currentIndex < Math.floor((carrosselContainer.scrollWidth - carrosselContainer.clientWidth) / cardWidth)) {
        currentIndex += step; // Pula pelo número de cards visíveis
      } else if (direction === 'prevP' && currentIndex > 0) {
        currentIndex -= step; // Pula para trás pelo número de cards visíveis
      } 
    }

    // Move o carrossel para a posição correta
    carrosselContainer.scrollLeft = currentIndex * cardWidth;

    updateButtons(); // Atualiza o estado dos botões
  };

  // Adiciona eventos aos botões
  nextButton.addEventListener('click', () => moveCarrossel('nextP'));
  prevButton.addEventListener('click', () => moveCarrossel('prevP'));

  updateButtons(); // Atualiza inicialmente os botões
});





