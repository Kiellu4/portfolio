const typed = document.querySelector('#typed-command');
const command = 'whoami';
let typeIndex = 0;
function typeCommand() {
  if (typed && typeIndex < command.length) {
    typed.textContent += command[typeIndex++];
    window.setTimeout(typeCommand, 105);
  }
}
if (typed) window.setTimeout(typeCommand, 350);

const menuButton = document.querySelector('.menu-button');
const navLinks = document.querySelector('#nav-links');
if (menuButton && navLinks) {
  menuButton.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  navLinks.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  }));
}

const themeButton = document.querySelector('.theme-toggle');
const savedTheme = localStorage.getItem('portfolio-theme');
if (savedTheme === 'light') document.body.classList.add('light');
function updateThemeLabel() {
  if (!themeButton) return;
  const light = document.body.classList.contains('light');
  themeButton.setAttribute('aria-label', light ? 'Switch to dark theme' : 'Switch to light theme');
  themeButton.textContent = light ? '◐' : '☼';
}
updateThemeLabel();
if (themeButton) {
  themeButton.addEventListener('click', () => {
    document.body.classList.toggle('light');
    localStorage.setItem('portfolio-theme', document.body.classList.contains('light') ? 'light' : 'dark');
    updateThemeLabel();
  });
}

const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
  if (entry.isIntersecting) {
    entry.target.classList.add('visible');
    observer.unobserve(entry.target);
  }
}), { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();
