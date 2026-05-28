const partialRefresh = {
  init() {
    document.querySelectorAll('[data-partial]').forEach((el) => {
      const url = el.dataset.partial;
      const interval = parseInt(el.dataset.refreshInterval || '0', 10);
      if (interval > 0) {
        setInterval(() => this.refresh(el, url), interval * 1000);
      }
    });
  },

  async refresh(container, url) {
    try {
      const res = await fetch(url, {
        headers: { 'X-Partial': '1' },
      });
      if (!res.ok) return;
      const html = await res.text();
      container.innerHTML = html;
      container.querySelectorAll('[data-reveal]').forEach((el) => {
        el.classList.add('revealed');
      });
    } catch (e) {
      // silent fail — do not interrupt the user
    }
  },
};

document.addEventListener('DOMContentLoaded', () => partialRefresh.init());
