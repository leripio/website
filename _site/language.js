// Explicit language URLs stay in their chosen language.
(() => {
  let preference;
  try {
    preference = localStorage.getItem('site-language');
  } catch {}

  const path = window.location.pathname;
  if (path === '/form-confirmation' || path === '/form-confirmation.html') {
    let submittedLanguage;
    try {
      submittedLanguage = sessionStorage.getItem('form-language');
    } catch {}
    const language = ['pt', 'en'].includes(submittedLanguage) ? submittedLanguage
      : (['pt', 'en'].includes(preference) ? preference
        : ((navigator.language || '').toLowerCase().startsWith('pt') ? 'pt' : 'en'));
    window.location.replace('/' + language + '/thank-you.html');
    return;
  }
  if (path === '/' || path === '/index.html') {
    const language = ['pt', 'en'].includes(preference)
      ? preference
      : ((navigator.languages?.[0] || navigator.language || '').toLowerCase().startsWith('pt') ? 'pt' : 'en');
    window.location.replace('/' + language + '/' + window.location.search + window.location.hash);
    return;
  }

  const legacy = path.match(/^\/(index|services|talks|resume|thank-you)(-pt)?(?:\.html)?$/);
  if (legacy) {
    const language = legacy[2] ? 'pt' : 'en';
    const page = legacy[1] === 'index' ? '' : legacy[1] + '.html';
    window.location.replace('/' + language + '/' + page + window.location.search + window.location.hash);
    return;
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.language-switch').forEach((link) => {
      link.addEventListener('click', () => {
        try {
          localStorage.setItem('site-language', link.getAttribute('hreflang').startsWith('pt') ? 'pt' : 'en');
        } catch {}
        link.hash = window.location.hash;
      });
    });
  });
})();
