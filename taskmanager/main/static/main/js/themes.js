// Функция для смены темы
function changeTheme(theme) {
  document.body.className = theme;
  localStorage.setItem('theme', theme);
}

var savedTheme = localStorage.getItem('theme');
if (savedTheme) {

  changeTheme(savedTheme);
}


