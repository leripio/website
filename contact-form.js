// Keep Netlify's native submission and localize browser validation messages.
document.querySelectorAll('.contact-form').forEach((form) => {
  const portuguese = form.dataset.language === 'pt-BR';
  form.querySelectorAll('input, select, textarea').forEach((field) => {
    field.addEventListener('input', () => field.setCustomValidity(''));
    field.addEventListener('change', () => field.setCustomValidity(''));
    field.addEventListener('invalid', () => {
      field.setCustomValidity('');
      if (field.validity.valueMissing) {
        field.setCustomValidity(portuguese ? 'Preencha este campo.' : 'Please fill out this field.');
      } else if (field.validity.typeMismatch && field.type === 'email') {
        field.setCustomValidity(portuguese ? 'Informe um endereço de e-mail válido.' : 'Please enter a valid email address.');
      }
    });
  });

  const local = ['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname)
    || window.location.protocol === 'file:';
  form.addEventListener('submit', (event) => {
    if (!local) {
      try {
        sessionStorage.setItem('form-language', portuguese ? 'pt' : 'en');
        localStorage.setItem('site-language', portuguese ? 'pt' : 'en');
      } catch {}
      return;
    }
    event.preventDefault();
    const status = form.querySelector('.contact-form-status');
    status.hidden = false;
    status.textContent = portuguese
      ? 'Prévia local: sua mensagem não foi enviada. O envio ficará disponível após a publicação e a ativação do formulário.'
      : 'Local preview: your message has not been sent. Submissions will be available once the site is deployed and the form is enabled.';
  });
});
