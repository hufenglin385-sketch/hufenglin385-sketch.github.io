(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const search = document.querySelector('#note-search');
  const items = [...document.querySelectorAll('.note-item')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const searchTrigger = document.querySelector('[data-open-search]');
  const toolbar = document.querySelector('.js-tools');
  let category = 'all';

  function filterNotes() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    items.forEach(item => {
      const match = (category === 'all' || item.dataset.category === category) &&
        (!query || item.dataset.search.toLocaleLowerCase().includes(query));
      item.hidden = !match;
      if (match) {
        visible++;
        item.classList.add('is-visible');
      }
    });
    const count = document.querySelector('.result-count');
    count.textContent = query || category !== 'all' ? '找到 ' + visible + ' 篇文章' : visible + ' 篇文章';
    document.querySelector('.empty-state').hidden = visible > 0;
  }
  if (search && toolbar) {
    toolbar.hidden = false;
    searchTrigger.hidden = false;
    search.addEventListener('input', filterNotes);
    filters.forEach(button => button.addEventListener('click', () => {
      category = button.dataset.filter;
      filters.forEach(filter => {
        const active = filter === button;
        filter.classList.toggle('is-active', active);
        filter.setAttribute('aria-pressed', String(active));
      });
      filterNotes();
    }));
    searchTrigger.addEventListener('click', () => {
      document.querySelector('#notes').scrollIntoView({behavior: reduced ? 'instant' : 'smooth'});
      search.focus({preventScroll: true});
    });
    document.querySelector('[data-reset-search]').addEventListener('click', () => {
      search.value = '';
      filters[0].click();
      search.focus({preventScroll: true});
    });
    search.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        search.value = '';
        filterNotes();
      }
    });
  } else if (searchTrigger) {
    searchTrigger.hidden = false;
    searchTrigger.addEventListener('click', () => { window.location.href = '/#notes'; });
  }
  if (!reduced && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold: 0.08});
    document.querySelectorAll('.reveal').forEach(element => {
      element.classList.add('will-reveal');
      observer.observe(element);
    });
  }
  const device = document.querySelector('.device-frame');
  const progress = document.querySelector('.reading-progress span');
  let scheduled = false;
  function updateScroll() {
    if (device && !reduced) {
      const shift = Math.min(window.scrollY * 0.05, 28);
      device.style.transform = 'translateY(' + shift + 'px)';
    }
    if (progress) {
      const range = document.documentElement.scrollHeight - window.innerHeight;
      const fraction = range > 0 ? Math.min(1, Math.max(0, window.scrollY / range)) : 1;
      progress.style.transform = 'scaleX(' + fraction + ')';
    }
    scheduled = false;
  }
  if (device || progress) {
    window.addEventListener('scroll', () => {
      if (!scheduled) { scheduled = true; window.requestAnimationFrame(updateScroll); }
    }, {passive:true});
    window.addEventListener('resize', updateScroll);
    updateScroll();
  }
  const copy = document.querySelector('[data-copy-link]');
  if (copy) {
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      const status = document.querySelector('.copy-status');
      const canonical = document.querySelector('link[rel="canonical"]').href;
      try {
        await navigator.clipboard.writeText(canonical);
        copy.textContent = '已复制';
        status.textContent = '文章链接已复制。';
        window.setTimeout(() => { copy.textContent = '复制文章链接'; }, 2000);
      } catch {
        status.textContent = '可以复制浏览器地址栏中的文章链接。';
      }
    });
  }
})();
