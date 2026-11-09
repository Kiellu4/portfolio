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

const navClock = document.querySelector('.nav-clock');
if (navClock) {
  const time = navClock.querySelector('span');
  const date = navClock.querySelector('small');
  const updateNavClock = () => {
    const now = new Date();
    time.textContent = now.toLocaleTimeString('en-GB', { hour12: false });
    date.textContent = now.toLocaleDateString('en-GB', { day: '2-digit', month: '2-digit', year: '2-digit' });
  };
  updateNavClock();
  window.setInterval(updateNavClock, 1000);
}

const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
  if (entry.isIntersecting) {
    entry.target.classList.add('visible');
    observer.unobserve(entry.target);
  }
}), { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));

const navPillContainer = document.querySelector('.nav-links');
if (navPillContainer) {
  const navPillLinks = [...navPillContainer.querySelectorAll('a[href^="#"]')];
  if (navPillLinks[0]) navPillLinks[0].classList.add('nav-active');
  const navSections = navPillLinks
    .map((link) => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);
  if (navSections.length) {
    const navObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const activeLink = navPillLinks.find((link) => link.getAttribute('href') === `#${entry.target.id}`);
        if (!activeLink) return;
        navPillLinks.forEach((link) => link.classList.toggle('nav-active', link === activeLink));
      });
    }, { threshold: 0.3 });
    navSections.forEach((section) => navObserver.observe(section));
  }
}

const year = document.querySelector('#year');
if (year) year.textContent = new Date().getFullYear();

const viewableImageSelector = [
  '.project-image',
  '.achievement-card img',
  '.cert-grid img',
  '.writeup-card > img',
  '.writeup-hero img',
  '.writeup-figure',
  '.writeup-figure img',
  '.challenge-body figure img'
].join(', ');
const viewableImages = [...new Set(document.querySelectorAll(viewableImageSelector))];

if (viewableImages.length) {
  const lightbox = document.createElement('div');
  lightbox.className = 'image-lightbox';
  lightbox.hidden = true;
  lightbox.innerHTML = '<div class="image-lightbox-dialog" role="dialog" aria-modal="true" aria-labelledby="image-lightbox-caption"><button class="image-lightbox-close" type="button" aria-label="Close image viewer">×</button><img class="image-lightbox-image" alt=""><p class="image-lightbox-caption" id="image-lightbox-caption"></p></div>';
  document.body.append(lightbox);

  const lightboxImage = lightbox.querySelector('.image-lightbox-image');
  const lightboxCaption = lightbox.querySelector('.image-lightbox-caption');
  const closeButton = lightbox.querySelector('.image-lightbox-close');
  let lastFocusedElement = null;
  let hoverPreview = null;

  const closeLightbox = () => {
    if (lightbox.hidden) return;
    lightbox.hidden = true;
    document.body.classList.remove('image-lightbox-open');
    lightboxImage.removeAttribute('src');
    if (lastFocusedElement?.isConnected) lastFocusedElement.focus();
  };

  const openLightbox = (image) => {
    lastFocusedElement = document.activeElement;
    lightboxImage.src = image.currentSrc || image.src;
    lightboxImage.alt = image.alt;
    lightboxCaption.textContent = image.alt || 'Expanded image';
    lightbox.hidden = false;
    document.body.classList.add('image-lightbox-open');
    closeButton.focus();
  };

  const removeHoverPreview = () => {
    if (hoverPreview) hoverPreview.remove();
    hoverPreview = null;
  };

  const showHoverPreview = (image) => {
    if (!window.matchMedia('(hover: hover)').matches) return;
    removeHoverPreview();
    hoverPreview = document.createElement('div');
    hoverPreview.className = 'image-hover-preview';
    hoverPreview.setAttribute('aria-hidden', 'true');
    const previewImage = document.createElement('img');
    previewImage.src = image.currentSrc || image.src;
    previewImage.alt = '';
    hoverPreview.append(previewImage);
    document.body.append(hoverPreview);

    const imageRect = image.getBoundingClientRect();
    const previewWidth = Math.min(Math.max(imageRect.width * 1.45, 320), window.innerWidth * 0.62);
    const previewHeight = Math.min(window.innerHeight * 0.72, previewWidth * 0.78);
    const left = imageRect.right + 16 + previewWidth > window.innerWidth
      ? Math.max(16, imageRect.left - previewWidth - 16)
      : imageRect.right + 16;
    const top = Math.min(Math.max(16, imageRect.top), window.innerHeight - previewHeight - 16);
    hoverPreview.style.setProperty('--preview-width', `${previewWidth}px`);
    hoverPreview.style.left = `${left}px`;
    hoverPreview.style.top = `${top}px`;
  };

  viewableImages.forEach((image) => {
    image.classList.add('viewable-image');
    image.tabIndex = 0;
    image.setAttribute('role', 'button');
    image.setAttribute('aria-haspopup', 'dialog');
    image.setAttribute('aria-label', `View full image: ${image.alt || 'image'}`);
    image.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openLightbox(image);
      }
    });
    image.addEventListener('pointerenter', () => showHoverPreview(image));
    image.addEventListener('pointerleave', removeHoverPreview);
    image.addEventListener('focus', removeHoverPreview);
  });

  document.addEventListener('click', (event) => {
    const image = event.target.closest(
      '.writeup-figure img, .challenge-body figure img, .writeup-hero img, img.writeup-figure'
    );
    if (!image || lightbox.contains(image)) return;
    openLightbox(image);
  });

  closeButton.addEventListener('click', closeLightbox);
  lightboxImage.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) closeLightbox();
  });
  document.addEventListener('keydown', (event) => {
    if (lightbox.hidden) return;
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'Tab') {
      event.preventDefault();
      closeButton.focus();
    }
  });
}
