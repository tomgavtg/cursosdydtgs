from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core.enums import STATES


class StudentsManager(models.Manager):
	def get_student(self, slug):
		try:
			return self.get(slug=slug, is_active=True, state=STATES.Active)
		except ObjectDoesNotExist:
			return None


class Student(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.deletion.SET_NULL, null=True)
	avatar = models.ImageField(
		upload_to="avatars/",
		max_length=255,
		blank=True,
		null=True
	)
	name = models.TextField(max_length=255, blank=True)
	email = models.EmailField(max_length=255, unique=True)
	date_of_birth = models.DateField(null=True)
	facebook = models.URLField(blank=True)
	twitter = models.URLField(blank=True)
	linkedin = models.URLField(blank=True)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	slug = AutoSlugField(populate_from='name', unique=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = StudentsManager()

	def __str__(self):
		return self.name


class ProgressManager(models.Manager):
	pass


class Progress(models.Model):
	from evaluations.models import Test
	student = models.ForeignKey(Student, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	from courses.models import Section
	section = models.ForeignKey(Section, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	test = models.ForeignKey(Test, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	completed = models.BooleanField(default=False)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ProgressManager()

	def __str__(self):
		return self.id
