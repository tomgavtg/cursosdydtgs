import os
from string import Template

from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from core.utils import build_site_url
from users.models import AuthToken
from courses.settings import BASE_DIR


class EMAIL_TEMPLATES():
	CambioPassword = {
		'template': 'change_password',
		'subject': _("mails.change_password.title"),
		'from_email': settings.EMAIL_FROM,
	}
	Contacto = {
		'template': 'contact',
		'subject': _("mails.contact.title"),
		'from_email': settings.EMAIL_FROM,
	}
	choices = (
		(CambioPassword, _("enums.mails.change_password")),
		(Contacto, _("enums.mails.contact")),
	)


def send_email(template, email_to, variables=None, attachments=None):
	if not settings.SEND_MAILS:
		return True
	if variables is None:
		variables = {}
	file_in_html = open(os.path.join(BASE_DIR, 'core/mail/templates/' + template.get('template') + '.html'))
	src_html = Template(file_in_html.read())
	filein = open(os.path.join(BASE_DIR, 'core/mail/templates/' + template.get('template') + '.txt'))
	src = Template(filein.read())
	sent = send_mail(template.get('subject'), src.safe_substitute(variables), template.get('from_email'), [email_to], html_message=src_html.safe_substitute(variables))
	return sent


def send_forgot_password_email(user):
	variables = {
		'name': user.name,
		'url': build_site_url('reset-password', AuthToken.objects.create_password_token(user).token)
	}
	return send_email(EMAIL_TEMPLATES.CambioPassword, user.email, variables)


def send_contact_email(name, message, email, phone):
	variables = {
		'name': name,
		'message': message,
		'email': email,
		'phone': phone,
	}
	return send_email(EMAIL_TEMPLATES.Contacto, settings.EMAIL_FROM, variables)


def send_test_email(name, message, email, phone):
	variables = {
		'name': name,
		'message': message,
		'email': email,
		'phone': phone,
	}
	return send_email(EMAIL_TEMPLATES.Contacto, email, variables)
