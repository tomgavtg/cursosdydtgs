from import_export import fields, widgets
from import_export.resources import ModelResource
#
#
from django.contrib import admin

from core.admin import ListAdminMixin
from core.enums import USER_TYPES, STATES
#from core.mail import mail
from core.utils import random_password
from teachers.models import Teacher
from users.models import User
from import_export import admin as csvadmin


class TeacherResource(ModelResource):
	delete = fields.Field(widget=widgets.BooleanWidget())

	class Meta:
		model = Teacher
		fields = ('id', 'name', 'email', 'date_of_birth', 'experience', 'facebook', 'twitter', 'linkedin', 'title')

	def for_delete(self, row, instance):
		return self.fields["delete"].clean(row)


class TeacherAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	resource_class = TeacherResource
	fields = ('name', 'title', 'email', 'date_of_birth', 'experience', 'facebook', 'twitter', 'linkedin', 'is_active', 'state')

	def save_model(self, request, obj, form, change):
		if not obj.pk:
			password = random_password()
			obj.user = User.objects.create_user(obj.email, obj.name, USER_TYPES.Teacher, STATES.Active, password)
			#mail.send_forgot_password_email(obj.user)
		obj.save()


admin.site.unregister(Teacher)
admin.site.register(Teacher, TeacherAdmin)
