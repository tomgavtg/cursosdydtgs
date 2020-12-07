from import_export import fields, widgets
from import_export.resources import ModelResource
from django.contrib import admin

from core.admin import ListAdminMixin
from core.enums import USER_TYPES, STATES
from core.mail import mail
from core.utils import random_password
from students.models import Student, Progress
from users.models import User
from import_export import admin as csvadmin


class StudentResource(ModelResource):
	delete = fields.Field(widget=widgets.BooleanWidget())

	class Meta:
		model = Student
		fields = ('id', 'name', 'email', 'date_of_birth', 'facebook', 'twitter', 'linkedin')

	def for_delete(self, row, instance):
		return self.fields["delete"].clean(row)


class StudentAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	resource_class = StudentResource
	fields = ('name', 'email', 'date_of_birth', 'facebook', 'twitter', 'linkedin', 'is_active', 'state')

	def save_model(self, request, obj, form, change):
		if not obj.pk:
			password = random_password()
			obj.user = User.objects.create_user(obj.email, obj.name, USER_TYPES.Student, STATES.Active, password)
			mail.send_forgot_password_email(obj.user)
		obj.save()


class ProgressAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')

	def save_model(self, request, obj, form, change):
		if not obj.pk:
			password = random_password()
			obj.user = User.objects.create_user(obj.email, obj.name, USER_TYPES.Student, STATES.Active, password)
			mail.send_forgot_password_email(obj.user)
		obj.save()


admin.site.unregister(Student)
admin.site.register(Student, StudentAdmin)
admin.site.unregister(Progress)
admin.site.register(Progress, ProgressAdmin)

