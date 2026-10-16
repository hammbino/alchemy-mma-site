// Mobile menu
const menuBtn = document.querySelector('.menu');
const menu = document.getElementById('menu');
menuBtn.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  menuBtn.setAttribute('aria-expanded', open);
  menuBtn.textContent = open ? 'Close' : 'Menu';
  document.body.classList.toggle('menu-open', open);
});

// Carousels: previous / next buttons and a "2 of 7" counter
document.querySelectorAll('[data-rail]').forEach(section => {
  const rail = section.querySelector('.rail');
  const count = section.querySelector('.rail-count');
  const step = () => rail.firstElementChild.offsetWidth + 16;
  section.querySelectorAll('.rail-btns button').forEach(b =>
    b.addEventListener('click', () => rail.scrollBy({ left: b.dataset.dir * step(), behavior: 'smooth' }))
  );
  if (count) {
    const total = rail.children.length;
    const update = () => { count.textContent = `${Math.min(total, Math.round(rail.scrollLeft / step()) + 1)} of ${total}`; };
    rail.addEventListener('scroll', update, { passive: true });
    update();
  }
});

// 1-on-1 request form. Not wired to a mail service yet: it only shows the confirmation.
const form = document.querySelector('.form[data-demo]');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    form.classList.add('done');
    form.querySelector('.sent').focus();
  });
}

// Review markers: a toggle to hide the gold "For Brian" labels, remembered per browser
const reviewToggle = document.querySelector('.review-toggle');
if (reviewToggle) {
  const set = on => {
    document.body.classList.toggle('clean', on);
    reviewToggle.setAttribute('aria-pressed', on);
    reviewToggle.textContent = on ? 'Show markers for Brian' : 'Hide markers';
  };
  let saved = false;
  try { saved = localStorage.getItem('alchemy-clean') === '1'; } catch (e) {}
  set(saved);
  reviewToggle.addEventListener('click', () => {
    const on = !document.body.classList.contains('clean');
    set(on);
    try { localStorage.setItem('alchemy-clean', on ? '1' : '0'); } catch (e) {}
  });
}
