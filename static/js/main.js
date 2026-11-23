const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#nav');
const header = document.querySelector('.site-header');
const mobileQuery = window.matchMedia('(max-width: 720px)');

const setMenuState = (open) => {
  if (!toggle || !nav) return;
  toggle.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
  document.body.classList.toggle('nav-open', open);
  document.body.classList.toggle('menu-is-open', open);
  if (open) nav.querySelector('a')?.focus();
  else toggle.focus();
};

if (toggle) toggle.addEventListener('click', () => {
  setMenuState(toggle.getAttribute('aria-expanded') !== 'true');
});

nav?.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => setMenuState(false)));
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') setMenuState(false);
});
mobileQuery.addEventListener('change', (event) => {
  if (!event.matches) setMenuState(false);
});

const updateHeader = () => header?.classList.toggle('is-scrolled', window.scrollY > 12);
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
  const sections = document.querySelectorAll('main > section:not(.hero)');
  sections.forEach((section) => {
    section.classList.add('reveal');
    section.querySelectorAll('.eyebrow, h1, h2, .lede, .actions, .area-grid article, .process li, .service-detail article, .contact-info, .form-card').forEach((item, index) => {
      item.classList.add('reveal-item');
      item.style.setProperty('--reveal-index', index);
    });
  });
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });
  sections.forEach((section) => observer.observe(section));
}

const heroArt = document.querySelector('.hero-location');
if (heroArt && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  let ticking = false;
  const updateHeroDepth = () => {
    heroArt.style.setProperty('--map-shift', `${Math.min(window.scrollY * .045, 18)}px`);
    ticking = false;
  };
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(updateHeroDepth);
      ticking = true;
    }
  }, { passive: true });
  updateHeroDepth();
}
