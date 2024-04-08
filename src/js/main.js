document.querySelector('.menu-icon').addEventListener('click', function() {
  document.querySelector('.menu ul').classList.toggle('active');
  document.querySelector('.menu-icon .fa-bars').classList.toggle('active');
  document.querySelector('.menu-icon .fa-times').classList.toggle('active');
});
