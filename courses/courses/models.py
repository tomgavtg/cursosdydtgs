from autoslug import AutoSlugField
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from core.enums import STATES
from teachers.models import Teacher
from ckeditor.fields import RichTextField


class CoursesManager(models.Manager):
	def get_course(self, slug):
		try:
			return self.get(slug=slug, is_active=True, state=STATES.Active)
		except ObjectDoesNotExist:
			return None


class Course(models.Model):
	teachers = models.ManyToManyField(Teacher)
	from students.models import Student
	students = models.ManyToManyField(Student)
	main_image = models.ImageField(
		upload_to="courses/",
		max_length=255,
		blank=True,
		null=True
	)
	name = models.TextField(max_length=255, blank=True)
	duration = models.TextField(max_length=255, blank=True)
	language = models.TextField(max_length=255, blank=True)
	summary = models.TextField(max_length=255, blank=True)
	tags = models.TextField(max_length=255, blank=True)
	description = RichTextField(blank=True)
	previous_knowledge = RichTextField(blank=True)
	difficulty = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	slug = AutoSlugField(populate_from='name', unique=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = CoursesManager()

	def __str__(self):
		return self.name


class ModulesManager(models.Manager):
	def get_module(self, slug):
		try:
			return self.get(slug=slug, is_active=True, state=STATES.Active)
		except ObjectDoesNotExist:
			return None


class Module(models.Model):
	course = models.ForeignKey(Course, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	name = models.TextField(max_length=255, blank=True)
	order = models.IntegerField()
	duration = models.TextField(max_length=255, blank=True)
	summary = models.TextField(max_length=255, blank=True)
	description = RichTextField(blank=True)
	content1 = RichTextField(blank=True)
	content2 = RichTextField(blank=True)
	content3 = RichTextField(blank=True)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	slug = AutoSlugField(populate_from='name', unique=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ModulesManager()

	def __str__(self):
		return self.name


class SectionsManager(models.Manager):
	def get_section(self, slug):
		try:
			return self.get(slug=slug, is_active=True, state=STATES.Active)
		except ObjectDoesNotExist:
			return None

	def complete_section(self, student, section=None, test=None):
		progress = None
		if section:
			progress = section.progress_set.filter(is_active=True, state=STATES.Active, student__id=student.id).first()
		elif test:
			progress = test.progress_set.filter(is_active=True, state=STATES.Active, student__id=student.id).first()
		if progress:
			progress.complete = True
			progress.save()
		else:
			from students.models import Progress
			progress = Progress(student=student, section=section, test=test, completed=True, state=STATES.Active, is_active=True)
			progress.save()


class Section(models.Model):
	module = models.ForeignKey(Module, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	name = models.TextField(max_length=255, blank=True)
	order = models.IntegerField()
	summary = models.TextField(max_length=255, blank=True)
	description = RichTextField(blank=True)
	content1 = RichTextField(blank=True)
	content2 = RichTextField(blank=True)
	content3 = RichTextField(blank=True)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	slug = AutoSlugField(populate_from='name', unique=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = SectionsManager()

	def __str__(self):
		return self.name


class FilesManager(models.Manager):
	pass


class File(models.Model):
	course = models.ForeignKey(Course, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	module = models.ForeignKey(Module, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	section = models.ForeignKey(Section, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	name = models.TextField(max_length=255, blank=True)
	order = models.IntegerField()
	description = RichTextField(blank=True)
	file = models.FileField(
		upload_to="files/",
		blank=True,
		null=True
	)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = FilesManager()

	def __str__(self):
		return self.name


class VideosManager(models.Manager):
	pass


class Video(models.Model):
	course = models.ForeignKey(Course, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	module = models.ForeignKey(Module, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	section = models.ForeignKey(Section, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	title = models.TextField(max_length=255, blank=True)
	order = models.IntegerField()
	description = RichTextField(blank=True)
	link = models.CharField(max_length=500, blank=True)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = VideosManager()

	def __str__(self):
		return self.title