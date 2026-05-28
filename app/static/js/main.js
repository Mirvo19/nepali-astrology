const header = document.getElementById('site-header');
const navToggle = document.getElementById('nav-toggle');
const mobileMenu = document.getElementById('mobile-menu');

if (navToggle && mobileMenu) {
  navToggle.addEventListener('click', () => {
    navToggle.classList.toggle('open');
    mobileMenu.classList.toggle('open');
    const isOpen = mobileMenu.classList.contains('open');
    mobileMenu.setAttribute('aria-hidden', String(!isOpen));
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });
}

window.addEventListener('scroll', () => {
  if (window.scrollY > 60) {
    header?.classList.add('scrolled');
  } else {
    header?.classList.remove('scrolled');
  }
});

document.querySelectorAll('.nav-links a').forEach((link) => {
  if (link.getAttribute('href') === window.location.pathname) {
    link.classList.add('active');
  }
});

const reveals = document.querySelectorAll('[data-reveal]');
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
      }
    });
  },
  { threshold: 0.15 }
);
reveals.forEach((item) => revealObserver.observe(item));

const counters = document.querySelectorAll('[data-counter]');
const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      if (el.dataset.done) return;
      el.dataset.done = 'true';
      const target = parseInt(el.dataset.counter, 10);
      const suffix = el.dataset.counterSuffix || '';
      const duration = 1800;
      const start = performance.now();
      const easeOutQuart = (t) => 1 - Math.pow(1 - t, 4);
      const update = (time) => {
        const progress = Math.min(1, (time - start) / duration);
        const value = Math.floor(target * easeOutQuart(progress));
        el.textContent = `${value}${suffix}`;
        if (progress < 1) requestAnimationFrame(update);
      };
      requestAnimationFrame(update);
    });
  },
  { threshold: 0.3 }
);
counters.forEach((item) => counterObserver.observe(item));

const wheel = document.getElementById('zodiac-wheel');
if (wheel) {
  const glyphs = wheel.querySelectorAll('.zodiac-glyph');
  glyphs.forEach((glyph, index) => {
    const angle = index * 30;
    glyph.style.transform = `rotateY(${angle}deg) translateZ(180px)`;
  });
}

const title = document.getElementById('hero-title');
if (title) {
  const words = title.textContent.trim().split(' ');
  title.textContent = '';
  words.forEach((word, index) => {
    const span = document.createElement('span');
    span.textContent = word + (index < words.length - 1 ? ' ' : '');
    span.style.setProperty('--delay', `${index * 60}ms`);
    title.appendChild(span);
  });
}

window.addEventListener('load', () => {
  document.body.classList.remove('loading');
});

const canvas = document.getElementById('starfield');
if (canvas) {
  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);
  let animationFrame;
  let scrollOffset = 0;
  const mouse = { x: width / 2, y: height / 2 };
  const stars = Array.from({ length: 180 }).map(() => ({
    x: Math.random() * width,
    y: Math.random() * height,
    r: Math.random() * 1 + 0.5,
    o: Math.random() * 0.4 + 0.2,
    s: Math.random() * 0.6 + 0.4,
    offset: Math.random() * Math.PI * 2,
  }));

  const resize = () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  };
  window.addEventListener('resize', resize);
  window.addEventListener('scroll', () => {
    scrollOffset = window.scrollY * 0.3;
  });
  window.addEventListener('mousemove', (event) => {
    mouse.x = event.clientX;
    mouse.y = event.clientY;
  });

  const draw = (time) => {
    ctx.clearRect(0, 0, width, height);
    stars.forEach((star) => {
      const driftX = (mouse.x - width / 2) * 0.00005 * star.s;
      const driftY = (mouse.y - height / 2) * 0.00005 * star.s;
      const twinkle = (Math.sin(time * 0.001 * star.s + star.offset) + 1) / 2;
      const opacity = Math.min(0.6, Math.max(0.2, star.o * (0.5 + twinkle)));
      ctx.fillStyle = `rgba(255,255,255,${opacity})`;
      ctx.beginPath();
      ctx.arc(star.x + driftX * width, star.y + driftY * height + scrollOffset, star.r, 0, Math.PI * 2);
      ctx.fill();
    });
    animationFrame = requestAnimationFrame(draw);
  };

  const hero = document.getElementById('hero');
  if (hero) {
    const heroObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            if (!animationFrame) animationFrame = requestAnimationFrame(draw);
          } else {
            cancelAnimationFrame(animationFrame);
            animationFrame = null;
          }
        });
      },
      { threshold: 0.1 }
    );
    heroObserver.observe(hero);
  } else {
    animationFrame = requestAnimationFrame(draw);
  }
}

const carousel = document.getElementById('testimonial-carousel');
const dotsContainer = document.getElementById('testimonial-dots');
if (carousel && dotsContainer) {
  const items = Array.from(carousel.children);
  const dots = items.map((_, index) => {
    const dot = document.createElement('div');
    dot.className = 'carousel-dot' + (index === 0 ? ' active' : '');
    dot.addEventListener('click', () => scrollToIndex(index));
    dotsContainer.appendChild(dot);
    return dot;
  });
  let index = 0;
  let intervalId;

  const scrollToIndex = (nextIndex) => {
    if (!items[nextIndex]) return;
    index = nextIndex;
    carousel.scrollTo({ left: items[index].offsetLeft, behavior: 'smooth' });
    dots.forEach((dot, i) => dot.classList.toggle('active', i === index));
  };

  const startAuto = () => {
    intervalId = setInterval(() => {
      scrollToIndex((index + 1) % items.length);
    }, 5000);
  };

  const stopAuto = () => {
    clearInterval(intervalId);
  };

  document.querySelectorAll('[data-carousel]').forEach((button) => {
    button.addEventListener('click', () => {
      const direction = button.dataset.carousel;
      if (direction === 'prev') {
        scrollToIndex((index - 1 + items.length) % items.length);
      } else {
        scrollToIndex((index + 1) % items.length);
      }
    });
  });

  carousel.addEventListener('mouseenter', stopAuto);
  carousel.addEventListener('mouseleave', startAuto);
  carousel.addEventListener('touchstart', stopAuto, { passive: true });
  carousel.addEventListener('touchend', startAuto);
  startAuto();
}

const accordion = document.getElementById('faq-accordion');
if (accordion) {
  accordion.addEventListener('click', (event) => {
    const header = event.target.closest('.accordion-header');
    if (!header) return;
    const item = header.parentElement;
    item.classList.toggle('active');
  });
}

const bookingForm = document.getElementById('booking-form');
const slotList = document.getElementById('slot-list');
const slotSpinner = document.getElementById('slot-spinner');
const appointmentDate = document.getElementById('appointment-date');
const appointmentTime = document.getElementById('appointment-time');
const slotPicker = document.querySelector('.slot-picker');

if (appointmentDate && slotPicker && slotList) {
  appointmentDate.addEventListener('change', async () => {
    slotList.innerHTML = '';
    appointmentTime.value = '';
    const skeletons = Array.from({ length: 6 }).map(() => {
      const skeleton = document.createElement('div');
      skeleton.className = 'slot-skeleton';
      slotList.appendChild(skeleton);
      return skeleton;
    });
    slotSpinner.style.display = 'none';
    const astrologerId = slotPicker.dataset.astrologer;
    const serviceId = slotPicker.dataset.service;
    const response = await fetch(`/api/slots/${astrologerId}?date=${appointmentDate.value}&service_id=${serviceId}`);
    const data = await response.json();
    slotList.innerHTML = '';
    if (!data.slots.length) {
      slotList.innerHTML = '<p>No slots available for this date.</p>';
      return;
    }
    data.slots.forEach((slot, index) => {
      const pill = document.createElement('div');
      pill.className = 'slot-pill';
      pill.style.transitionDelay = `${index * 40}ms`;
      pill.textContent = slot;
      requestAnimationFrame(() => {
        pill.style.opacity = '1';
        pill.style.transform = 'translateY(0)';
      });
      pill.addEventListener('click', () => {
        document.querySelectorAll('.slot-pill').forEach((el) => el.classList.remove('active'));
        pill.classList.add('active');
        appointmentTime.value = slot;
      });
      slotList.appendChild(pill);
    });
  });
}

if (bookingForm) {
  bookingForm.addEventListener('submit', (event) => {
    if (!appointmentTime.value) {
      event.preventDefault();
      alert('Please select a time slot.');
    }
  });
}

const contactForm = document.getElementById('contact-form');
if (contactForm) {
  contactForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = document.getElementById('contact-status');
    status.textContent = 'Sending...';
    const payload = Object.fromEntries(new FormData(contactForm));
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': window.csrfToken },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      showToast('Service temporarily unavailable. We are working on it soon.');
      status.textContent = 'Unavailable.';
      return;
    }
    status.textContent = 'Message sent.';
    contactForm.reset();
  });
}

function showToast(message) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

const serviceFilter = document.getElementById('service-filter');
const filterButtons = document.querySelectorAll('.filter-pill');
const filterCards = document.querySelectorAll('#astrologer-grid .astro-card');

const applyFilter = (value) => {
  filterCards.forEach((card) => {
    if (value === 'all' || card.dataset.services.includes(value)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
};

if (serviceFilter) {
  serviceFilter.addEventListener('change', () => {
    applyFilter(serviceFilter.value);
  });
}

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    filterButtons.forEach((btn) => btn.classList.remove('active'));
    button.classList.add('active');
    const value = button.dataset.filter;
    if (serviceFilter) serviceFilter.value = value;
    applyFilter(value);
  });
});

const availabilityBox = document.querySelector('.availability');
if (availabilityBox) {
  availabilityBox.innerHTML = `
    <h3>Check availability</h3>
    <input type="date" id="availability-date" />
    <div class="slot-list" id="availability-slots"></div>
  `;
  const dateInput = document.getElementById('availability-date');
  const slotsContainer = document.getElementById('availability-slots');
  dateInput.addEventListener('change', async () => {
    const astrologerId = availabilityBox.dataset.astrologer;
    const serviceId = availabilityBox.dataset.service;
    if (!serviceId) return;
    slotsContainer.innerHTML = '';
    const response = await fetch(`/api/slots/${astrologerId}?date=${dateInput.value}&service_id=${serviceId}`);
    if (!response.ok) return;
    const data = await response.json();
    if (!data.slots.length) {
      slotsContainer.innerHTML = '<p>No slots available for this date.</p>';
      return;
    }
    data.slots.forEach((slot, index) => {
      const pill = document.createElement('div');
      pill.className = 'slot-pill';
      pill.style.transitionDelay = `${index * 40}ms`;
      pill.textContent = slot;
      requestAnimationFrame(() => {
        pill.style.opacity = '1';
        pill.style.transform = 'translateY(0)';
      });
      slotsContainer.appendChild(pill);
    });
  });
}

const page = document.querySelector('.page-transition');
if (page) {
  document.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      if (link.target === '_blank' || link.href.includes('#')) return;
      page.classList.add('fade-out');
    });
  });
}
