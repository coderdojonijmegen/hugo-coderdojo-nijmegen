let mainNav = document.getElementById("js-menu");
let navBarToggle = document.getElementById("js-menu-toggle");

navBarToggle.addEventListener("click", function() {
  mainNav.classList.toggle("active");
});