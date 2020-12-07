from django.contrib import admin
from import_export import admin as csvadmin

from core.admin import ListAdminMixin
from evaluations.models import Test, Question, Answer, StudentAnswer, Grade


class QuestionInline(admin.TabularInline):
	model = Question


class AnswerInline(admin.TabularInline):
	model = Answer


class StudentAnswerInline(admin.TabularInline):
	model = StudentAnswer


class GradeInline(admin.TabularInline):
	model = Grade


class TestAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')
	inlines = [QuestionInline, GradeInline]


class QuestionAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')
	inlines = [AnswerInline]


class AnswerAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')


class StudentAnswerAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')


class GradeAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')


admin.site.unregister(Test)
admin.site.register(Test, TestAdmin)
admin.site.unregister(Question)
admin.site.register(Question, QuestionAdmin)
admin.site.unregister(Answer)
admin.site.register(Answer, AnswerAdmin)
admin.site.unregister(StudentAnswer)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
admin.site.unregister(Grade)
admin.site.register(Grade, GradeAdmin)
