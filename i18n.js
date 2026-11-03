// English HTML is the fallback; translations are bundled by build.py.
(() => {
  const storageKey = 'portfolio-language';
  const dictionary = PORTFOLIO_ZH;
  const prefixes = ['Open full image: ', 'Read PDF: ', 'DOI for ', 'View drawing: ', '← '];
  const suffixes = ['; use left and right arrow keys', ' figures', ' gallery', ' ↗', ' →'];
  function translate(value) {
    if (Object.hasOwn(dictionary, value)) return dictionary[value];
    const trimmed = value.trim();
    if (trimmed !== value) return value.slice(0, value.indexOf(trimmed)) + translate(trimmed) + value.slice(value.indexOf(trimmed) + trimmed.length);
    for (const prefix of prefixes) {
      if (value.startsWith(prefix)) return (dictionary[prefix] || prefix) + translate(value.slice(prefix.length));
    }
    for (const suffix of suffixes) {
      if (value.endsWith(suffix)) return translate(value.slice(0, -suffix.length)) + (dictionary[suffix] || suffix);
    }
    if (/^\d+ of \d+$/.test(value)) {
      const [index, total] = value.split(' of ');
      return `第 ${index} 张，共 ${total} 张`;
    }
    if (value.includes(' · ')) return value.split(' · ').map(translate).join(' · ');
    return value;
  }
  const records = [];
  const excluded = 'script, style, .gallery-count, .lightbox-caption, .lightbox-image';
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (!node.textContent.trim() || node.parentElement.closest(excluded)) continue;
    const original = node.textContent;
    const chinese = translate(original);
    if (original !== chinese) records.push(lang => { node.textContent = lang === 'zh' ? chinese : original; });
  }
  for (const element of document.querySelectorAll('[alt], [aria-label], [title], meta[name="description"], meta[property="og:title"], meta[property="og:description"]')) {
    if (element.matches(excluded)) continue;
    for (const attr of ['alt', 'aria-label', 'title', 'content']) {
      if (!element.hasAttribute(attr)) continue;
      const original = element.getAttribute(attr);
      const chinese = translate(original);
      if (original !== chinese) records.push(lang => element.setAttribute(attr, lang === 'zh' ? chinese : original));
    }
  }
  const originalTitle = document.title;
  const links = [...document.querySelectorAll('a[href]')].flatMap(link => {
    const href = link.getAttribute('href');
    if (/^(?:[a-z]+:|\/\/)/i.test(href)) return [];
    const url = new URL(href, location.href);
    if (url.origin !== location.origin || !(url.pathname.endsWith('/') || url.pathname.endsWith('/index.html'))) return [];
    return [{link, href}];
  });
  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'language-toggle';
  document.querySelector('nav').append(toggle);
  let language = 'en';
  function apply(lang, updateURL = false) {
    language = lang;
    document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
    for (const update of records) update(lang);
    document.title = lang === 'zh' ? translate(originalTitle) : originalTitle;
    toggle.textContent = lang === 'zh' ? 'English' : '中文';
    toggle.lang = lang === 'zh' ? 'en' : 'zh-CN';
    toggle.setAttribute('aria-label', lang === 'zh' ? 'Switch to English' : '切换到中文');
    for (const {link, href} of links) {
      const [pathAndQuery, hash] = href.split('#');
      const [path, query] = pathAndQuery.split('?');
      const params = new URLSearchParams(query);
      params.set('lang', lang);
      link.setAttribute('href', `${path}?${params}${hash === undefined ? '' : '#' + hash}`);
    }
    try { localStorage.setItem(storageKey, lang); } catch { /* Private browsing may block storage. */ }
    if (updateURL) {
      const url = new URL(location.href);
      url.searchParams.set('lang', lang);
      history.replaceState(null, '', url);
    }
    if (lightbox.open && imageGroup.length) showImage(imageIndex);
  }
  function preferredLanguage() {
    const requested = new URLSearchParams(location.search).get('lang');
    if (requested === 'zh' || requested === 'en') return requested;
    try { return localStorage.getItem(storageKey) === 'zh' ? 'zh' : 'en'; } catch { return 'en'; }
  }
  toggle.addEventListener('click', () => apply(language === 'en' ? 'zh' : 'en', true));
  window.addEventListener('pageshow', () => apply(preferredLanguage()));
  window.addEventListener('popstate', () => apply(preferredLanguage()));
  apply(preferredLanguage());
})();
