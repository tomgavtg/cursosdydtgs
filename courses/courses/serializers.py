from rest_framework import serializers

from core.enums import STATES
from students.models import Progress
from teachers.serializers import TeacherBasicSerializer
from .models import Course, Section, Module, File, Video


class CourseTeacherFullSerializer(serializers.ModelSerializer):
	students = serializers.SerializerMethodField()

	def get_students(self, obj):
		from students.serializers import StudentBasicSerializer
		return StudentBasicSerializer(obj.students.filter(is_active=True, state=STATES.Active).order_by('name'), many=True).data

	class Meta:
		model = Course
		fields = '__all__'


class CourseFullSerializer(serializers.ModelSerializer):
	teachers = serializers.SerializerMethodField()
	students = serializers.SerializerMethodField()
	modules = serializers.SerializerMethodField()
	progress = serializers.SerializerMethodField()
	files = serializers.SerializerMethodField()
	videos = serializers.SerializerMethodField()

	def get_teachers(self, obj):
		return TeacherBasicSerializer(obj.teachers.filter(is_active=True, state=STATES.Active).order_by('name'), many=True).data

	def get_students(self, obj):
		from students.serializers import StudentBasicSerializer
		return StudentBasicSerializer(obj.students.filter(is_active=True, state=STATES.Active).order_by('name'), many=True).data

	def get_modules(self, obj):
		return ModuleBasicSerializer(obj.module_set.filter(is_active=True, state=STATES.Active).order_by('order'), many=True, context={'user': self.context.get('user')}).data

	def get_progress(self, obj):
		progress = Progress.objects.filter(is_active=True, state=STATES.Active, completed=True, section__module__course__id=obj.id, student__id=self.context.get('user').student.id).count()
		sections = Section.objects.filter(is_active=True, state=STATES.Active, module__course__id=obj.id).count()
		return progress / sections if progress else 0

	def get_files(self, obj):
		return FileFullSerializer(obj.file_set.filter(is_active=True, state=STATES.Active).order_by('order'), many=True).data

	def get_videos(self, obj):
		return VideoFullSerializer(obj.video_set.filter(is_active=True, state=STATES.Active).order_by('order'), many=True).data

	class Meta:
		model = Course
		fields = '__all__'


class CourseBasicSerializer(serializers.ModelSerializer):
	teachers = serializers.SerializerMethodField()
	progress = serializers.SerializerMethodField()

	def get_teachers(self, obj):
		return TeacherBasicSerializer(obj.teachers.filter(is_active=True, state=STATES.Active), many=True).data

	def get_progress(self, obj):
		progress = Progress.objects.filter(is_active=True, state=STATES.Active, completed=True, section__module__course__id=obj.id, student__id=self.context.get('user').student.id).count()
		sections = Section.objects.filter(is_active=True, state=STATES.Active, module__course__id=obj.id).count()
		return progress / sections if progress else 0

	class Meta:
		model = Course
		fields = ('slug', 'name', 'duration', 'description', 'difficulty', 'previous_knowledge', 'language', 'progress', 'teachers', 'summary', 'tags', 'main_image')


class ModuleFullSerializer(serializers.ModelSerializer):
	course_slug = serializers.SerializerMethodField()
	next = serializers.SerializerMethodField()
	previous = serializers.SerializerMethodField()
	sections = serializers.SerializerMethodField()
	progress = serializers.SerializerMethodField()
	files = serializers.SerializerMethodField()
	videos = serializers.SerializerMethodField()

	def get_sections(self, obj):
		return SectionFullSerializer(obj.section_set.filter(is_active=True, state=STATES.Active).order_by('order'), many=True, context={'user': self.context.get('user')}).data

	def get_progress(self, obj):
		progress = Progress.objects.filter(is_active=True, state=STATES.Active, completed=True, section__module__id=obj.id, student__id=self.context.get('user').student.id).count()
		sections = Section.objects.filter(is_active=True, state=STATES.Active, module__id=obj.id).count()
		return progress / sections if progress else 0

	def get_files(self, obj):
		return FileFullSerializer(obj.file_set.filter(is_active=True, state=STATES.Active).order_by('order'), many=True).data

	def get_videos(self, obj):
		return VideoFullSerializer(obj.video_set.filter(is_active=True, state=STATES.Active).order_by('order'), many=True).data

	def get_course_slug(self, obj):
		return obj.course.slug

	def get_next(self, obj):
		next_module = obj.course.module_set.filter(is_active=True, state=STATES.Active, order=obj.order + 1).first()
		return next_module.slug if next_module is not None else None

	def get_previous(self, obj):
		previous_module = obj.course.module_set.filter(is_active=True, state=STATES.Active, order=obj.order - 1).first()
		return previous_module.slug if previous_module is not None else None

	class Meta:
		model = Module
		fields = '__all__'


class ModuleBasicSerializer(serializers.ModelSerializer):
	progress = serializers.SerializerMethodField()

	def get_progress(self, obj):
		progress = Progress.objects.filter(is_active=True, state=STATES.Active, completed=True, section__module__id=obj.id, student__id=self.context.get('user').student.id).count()
		sections = Section.objects.filter(is_active=True, state=STATES.Active, module__id=obj.id).count()
		return progress / sections if progress else 0

	class Meta:
		model = Module
		fields = ('slug', 'name', 'duration', 'summary', 'description', 'order', 'content1', 'content2', 'content3', 'progress')


class SectionFullSerializer(serializers.ModelSerializer):
	module_slug = serializers.SerializerMethodField()
	files = serializers.SerializerMethodField()
	videos = serializers.SerializerMethodField()
	completed = serializers.SerializerMethodField()
	next = serializers.SerializerMethodField()
	previous = serializers.SerializerMethodField()

	def get_next(self, obj):
		next_section = obj.module.section_set.filter(is_active=True, state=STATES.Active, order=obj.order + 1).first()
		return next_section.slug if next_section is not None else None

	def get_previous(self, obj):
		previous_section = obj.module.section_set.filter(is_active=True, state=STATES.Active, order=obj.order - 1).first()
		return previous_section.slug if previous_section is not None else None

	def get_files(self, obj):
		return FileFullSerializer(obj.file_set.filter(is_active=True, state=STATES.Active).order_by('order'), many=True).data

	def get_videos(self, obj):
		return VideoFullSerializer(obj.video_set.filter(is_active=True, state=STATES.Active).order_by('order'), many=True).data

	def get_completed(self, obj):
		progress = obj.progress_set.filter(is_active=True, state=STATES.Active, student__id=self.context.get('user').student.id).first()
		return progress and progress.completed

	def get_module_slug(self, obj):
		return obj.module.slug

	class Meta:
		model = Section
		fields = '__all__'


class FileFullSerializer(serializers.ModelSerializer):
	class Meta:
		model = File
		fields = '__all__'


class VideoFullSerializer(serializers.ModelSerializer):
	class Meta:
		model = Video
		fields = '__all__'
