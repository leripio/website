// The static preview cannot receive submissions. Production uses a native POST
// handled by Netlify Forms; never show a successful send without that response.
document.querySelectorAll('.contact-form').forEach((form) => {
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname)
    || window.location.protocol === 'file:';
  if (!local) return;
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const status = form.querySelector('.contact-form-status');
    status.hidden = false;
    status.textContent = form.dataset.language === 'pt-BR'
      ? 'Prévia local: sua mensagem não foi enviada. O envio ficará disponível após a publicação e a ativação do formulário.'
      : 'Local preview: your message has not been sent. Submissions will be available once the site is deployed and the form is enabled.';
  });
});
