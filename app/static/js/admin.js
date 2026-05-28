const adminToggle = document.getElementById('admin-toggle');
const sidebar = document.getElementById('admin-sidebar');
const sidebarBackdrop = document.getElementById('admin-sidebar-backdrop');
if (adminToggle && sidebar) {
  adminToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    sidebarBackdrop?.classList.toggle('open');
  });
}

if (sidebarBackdrop && sidebar) {
  sidebarBackdrop.addEventListener('click', () => {
    sidebar.classList.remove('open');
    sidebarBackdrop.classList.remove('open');
  });
}

document.querySelectorAll('[data-nav]').forEach((link) => {
  if (window.location.pathname === link.dataset.nav) {
    link.classList.add('active');
  }
});

const richText = document.querySelector('.rich-text');
if (richText) {
  richText.addEventListener('focus', () => {
    richText.style.minHeight = '200px';
  });
}
