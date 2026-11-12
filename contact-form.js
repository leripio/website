document.querySelectorAll('.contact-form').forEach((form) => {
  const portuguese = form.dataset.language === 'pt-BR';
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname)
    || window.location.protocol === 'file:';
  let submitting = false;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = form.querySelector('.contact-form-status');
    if (local) {
      status.hidden = false;
      status.textContent = portuguese
        ? 'Prévia local: sua mensagem não foi enviada. O envio ficará disponível após a publicação e a ativação do formulário.'
        : 'Local preview: your message has not been sent. Submissions will be available once the site is deployed and the form is enabled.';
      return;
    }
    if (submitting) return;
    submitting = true;
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    status.hidden = false;
    status.textContent = portuguese ? 'Enviando sua mensagem…' : 'Sending your message…';

    try {
      const response = await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString(),
      });
      if (!response.ok) throw new Error('Form submission failed');
      // Use the form language, regardless of browser or stored preferences.
      window.location.assign(portuguese ? '/pt/thank-you.html' : '/en/thank-you.html');
    } catch {
      status.textContent = portuguese
        ? 'Não foi possível confirmar o envio. Tente novamente em instantes.'
        : 'We could not confirm your submission. Please try again shortly.';
      submitting = false;
      button.disabled = false;
    }
  });
});
