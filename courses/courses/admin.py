from django.contrib import admin
from import_export import admin as csvadmin

from core.admin import ListAdminMixin
from courses.models import Course, Module, Section, File, Video


class FileInline(admin.TabularInline):
	model = File


class VideoInline(admin.TabularInline):
	model = Video


class ModuleInline(admin.TabularInline):
	model = Module


class SectionInline(admin.TabularInline):
	model = Section


class CourseAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')
	inlines = [FileInline, VideoInline, ModuleInline]


class ModuleAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')
	inlines = [FileInline, VideoInline, SectionInline]


class SectionAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')
	inlines = [FileInline, VideoInline]


class FileAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')


class VideoAdmin(ListAdminMixin, csvadmin.ImportExportModelAdmin):
	exclude = ('created_at', 'updated_at')


admin.site.unregister(Course)
admin.site.register(Course, CourseAdmin)
admin.site.unregister(Module)
admin.site.register(Module, ModuleAdmin)
admin.site.unregister(Section)
admin.site.register(Section, SectionAdmin)
admin.site.unregister(File)
admin.site.register(File, FileAdmin)
admin.site.unregister(Video)
admin.site.register(Video, VideoAdmin)
