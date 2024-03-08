function showMenu(toggleId, navId){
    var toggle = document.getElementById(toggleId),
          nav = document.getElementById(navId)
 
    toggle.addEventListener('click', () =>{
        nav.classList.toggle('show-menu')
        toggle.classList.toggle('show-icon')
    })
 }

 var event = window.matchMedia("(max-width:768px)");

 function clonarETrocarPosicoes() {
    // Selecionar os elementos originais
    var elemento1 = document.getElementById('logo');
    var elemento2 = document.getElementById('menuNavbar');

    // Clonar os elementos
    var cloneElemento1 = elemento1.cloneNode(true);
    var cloneElemento2 = elemento2.cloneNode(true);

    // Trocar as posições
    elemento1.parentNode.replaceChild(cloneElemento2, elemento1);
    elemento2.parentNode.replaceChild(cloneElemento1, elemento2);
  }

 function MediaQueryChange(event) {
    if (event.matches) {
      clonarETrocarPosicoes();
    } else {
      clonarETrocarPosicoes();
    }
  }

  function InitialMediaQueryChange(event) {
    if (event.matches) {
      clonarETrocarPosicoes();
    }
  }

window.addEventListener('load',InitialMediaQueryChange(event));
event.addListener(MediaQueryChange);

showMenu('navbarButton','menu');