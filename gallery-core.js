// One native modal keeps enlarged images on the current page and traps focus.
const lightbox = document.createElement('dialog');
lightbox.className = 'lightbox';
lightbox.setAttribute('aria-label', 'Image viewer');
lightbox.innerHTML = `<div class="lightbox-panel">
  <button class="lightbox-close" type="button" aria-label="Close image viewer" autofocus>×</button>
  <img class="lightbox-image" alt="">
  <div class="lightbox-toolbar">
    <button class="lightbox-prev" type="button" aria-label="Previous image">←</button>
    <p class="lightbox-caption" aria-live="polite"></p>
    <button class="lightbox-next" type="button" aria-label="Next image">→</button>
  </div>
</div>`;
document.body.append(lightbox);
const enlarged = lightbox.querySelector('.lightbox-image');
const caption = lightbox.querySelector('.lightbox-caption');
const previousImage = lightbox.querySelector('.lightbox-prev');
const nextImage = lightbox.querySelector('.lightbox-next');
let imageGroup = [];
let imageIndex = 0;
let opener;
function showImage(index) {
  imageIndex = index;
  const link = imageGroup[index];
  const description = link.closest('figure')?.querySelector('figcaption')?.textContent || link.querySelector('img').alt;
  enlarged.src = link.href;
  enlarged.alt = link.querySelector('img').alt;
  caption.textContent = `${description} · ${index + 1} / ${imageGroup.length}`;
  previousImage.disabled = index === 0;
  nextImage.disabled = index === imageGroup.length - 1;
}
document.querySelectorAll('a.sketch, a.image-expand').forEach(link => {
  link.addEventListener('click', event => {
    // Respect explicit browser gestures, while ordinary clicks stay in-page.
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = link;
    imageGroup = [...link.closest('.sketch-wall, .carousel').querySelectorAll('a.sketch, a.image-expand')];
    showImage(imageGroup.indexOf(link));
    lightbox.showModal();
    document.body.classList.add('lightbox-open');
  });
});
previousImage.addEventListener('click', () => showImage(imageIndex - 1));
nextImage.addEventListener('click', () => showImage(imageIndex + 1));
lightbox.querySelector('.lightbox-close').addEventListener('click', () => lightbox.close());
lightbox.addEventListener('click', event => { if (event.target === lightbox) lightbox.close(); });
lightbox.addEventListener('keydown', event => {
  if (event.key === 'ArrowLeft' && imageIndex > 0) { event.preventDefault(); showImage(imageIndex - 1); }
  if (event.key === 'ArrowRight' && imageIndex < imageGroup.length - 1) { event.preventDefault(); showImage(imageIndex + 1); }
});
lightbox.addEventListener('close', () => {
  document.body.classList.remove('lightbox-open');
  enlarged.removeAttribute('src');
  opener?.focus({preventScroll:true});
});

document.querySelectorAll('.carousel').forEach(gallery => {
  const track = gallery.querySelector('.carousel-track');
  const slides = [...track.querySelectorAll('.slide')];
  const prev = gallery.querySelector('.prev');
  const next = gallery.querySelector('.next');
  const counter = gallery.querySelector('.gallery-count');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let ticking = false;
  const position = slide => slide.getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft;
  function update() {
    const max = track.scrollWidth - track.clientWidth;
    current = slides.reduce((best, slide, i) => Math.abs(position(slide) - track.scrollLeft) < Math.abs(position(slides[best]) - track.scrollLeft) ? i : best, 0);
    prev.disabled = track.scrollLeft < 2;
    next.disabled = track.scrollLeft >= max - 2;
    const box = track.getBoundingClientRect();
    const visible = slides.map((slide, i) => ({r:slide.getBoundingClientRect(), i})).filter(({r}) => r.left < box.right - 10 && r.right > box.left + 10);
    const first = visible[0]?.i + 1 || 1;
    const last = visible[visible.length - 1]?.i + 1 || first;
    counter.textContent = `${first}${last > first ? '–' + last : ''} / ${slides.length}`;
    slides.forEach(slide => {
      const r = slide.getBoundingClientRect();
      if (r.right <= box.left + 2 || r.left >= box.right - 2) slide.querySelectorAll('video').forEach(video => video.pause());
    });
    ticking = false;
  }
  function move(direction) {
    const target = Math.max(0, Math.min(slides.length - 1, current + direction));
    track.scrollTo({left: position(slides[target]), behavior: reduced.matches ? 'instant' : 'smooth'});
  }
  prev.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  track.addEventListener('keydown', event => {
    if (event.target !== track) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1);
    }
  });
  track.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, {passive:true});
  new ResizeObserver(update).observe(track);
  update();
});
