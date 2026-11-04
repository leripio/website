# Contact form

The English and Portuguese services pages use the same Netlify Forms name,
`service-enquiry`, and the same field names, including optional country and state/region fields. A hidden `language` field identifies
the visitor's language. The form includes native required/email validation and
a honeypot field. It needs no API keys or custom server.

The project already publishes `_site` on Netlify. Before deploying the rendered
output, enable form detection in the site's Netlify Forms settings. Deploy the
complete output from `quarto render`, including both confirmation pages and
`contact-form.js`. Verify that `service-enquiry` appears in the Forms dashboard.
Send a test on the deployed site and verify the recorded submission. Configure
submission email notifications there if desired; they are account settings and
have not been changed by this implementation.

The local static preview cannot accept messages. Its JavaScript prevents a POST
and explicitly states that nothing was sent. On Netlify the browser performs a
normal form POST; the success page is reached only after the hosting service
processes it. Form detection and real delivery require verification after deploy.

If hosting moves away from Netlify, replace the form backend before publishing.
Setup reference: https://docs.netlify.com/manage/forms/setup/
