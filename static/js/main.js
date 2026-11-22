const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#nav');
if (toggle) toggle.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') === 'true';
  toggle.setAttribute('aria-expanded', String(!open));
  nav.classList.toggle('open', !open);
});
