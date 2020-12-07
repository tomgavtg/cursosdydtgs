from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.enums import USER_TYPES, STATES, USER_PERMISSIONS, LANGUAGES
from core.mail.mail import send_test_email
from core.permissions import IsAdmin


class SharingView(TemplateView):
	template_name = 'share.html'

	def get_context_data(self, **kwargs):
		context = super(SharingView, self).get_context_data(**kwargs)
		# page = Page.objects.get_product_by_slug(self.kwargs['slug'], [STATES.Active])
		# if page:
		# 	context['share'] = {'name': page.name, 'description': page.text_set.first(), 'slug': page.slug, 'main_image': page.image_set.first()}
		return context

	def dispatch(self, *args, **kwargs):
		return super(SharingView, self).dispatch(*args, **kwargs)


class CoreViewSet(viewsets.ViewSet):
	@action(methods=['get'], permission_classes=[AllowAny], detail=False)
	def mail_test(self, request, *args, **kwargs):
		return Response(send_test_email('Test', 'Test message', settings.EMAIL_TEST, 'Test phone'), status=status.HTTP_200_OK)

	def sequence_reset(self):
		from django.core.management import call_command
		from django.db import connection
		from django.apps import apps
		from io import StringIO
		commands = StringIO()
		cursor = connection.cursor()
		for app in apps.get_app_configs():
			call_command('sqlsequencereset', app.label, stdout=commands)
		cursor.execute(commands.getvalue())

	@action(methods=['get'], permission_classes=[IsAdmin], detail=False)
	def sequencereset(self, request, *args, **kwargs):
		self.sequence_reset()
		return Response(True, status=status.HTTP_200_OK)

	@action(methods=['get'], permission_classes=[IsAdmin], detail=False)
	def get_user_types(self, request, *args, **kwargs):
		types = []
		for a in USER_TYPES.choices:
			types.append({'value': a[0], 'label': a[1]})
		return Response(types, status=status.HTTP_200_OK)

	@action(methods=['get'], permission_classes=[IsAdmin], detail=False)
	def get_user_states(self, request, *args, **kwargs):
		types = []
		for a in STATES.choices:
			types.append({'value': a[0], 'label': a[1]})
		return Response(types, status=status.HTTP_200_OK)

	@action(methods=['get'], permission_classes=[IsAdmin], detail=False)
	def get_user_permissions(self, request, *args, **kwargs):
		types = []
		for a in USER_PERMISSIONS.choices:
			types.append({'value': a[0], 'label': a[1]})
		return Response(types, status=status.HTTP_200_OK)

	@action(methods=['get'], permission_classes=[AllowAny], detail=False)
	def get_languages(self, request, *args, **kwargs):
		types = []
		for a in LANGUAGES.choices:
			types.append({'value': a[0], 'label': a[1]})
		return Response(types, status=status.HTTP_200_OK)
