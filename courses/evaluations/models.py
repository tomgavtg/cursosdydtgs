from autoslug import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from core.enums import STATES, QUESTION_TYPES
from courses.models import Module, Course


class TestsManager(models.Manager):
	pass


class Test(models.Model):
	module = models.ForeignKey(Module, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	title = models.TextField(max_length=255, blank=True)
	description = RichTextField(blank=True)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	slug = AutoSlugField(populate_from='title', unique=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = TestsManager()

	def __str__(self):
		return self.title


class QuestionsManager(models.Manager):
	pass


class Question(models.Model):
	test = models.ForeignKey(Test, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	question = RichTextField(blank=True)
	type = models.CharField(max_length=1, choices=QUESTION_TYPES.choices)
	order = models.IntegerField()
	value = models.PositiveIntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(100)])

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = QuestionsManager()

	def __str__(self):
		return self.question


class AnswersManager(models.Manager):
	pass


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.deletion.SET_NULL, null=True, limit_choices_to={'type': QUESTION_TYPES.Multiple}, blank=True)
	answer = RichTextField(blank=True)
	order = models.IntegerField()
	correct = models.BooleanField(default=True)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = AnswersManager()

	def __str__(self):
		return self.answer


class StudentAnswersManager(models.Manager):
	pass


class StudentAnswer(models.Model):
	from students.models import Student
	student = models.ForeignKey(Student, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	question = models.ForeignKey(Question, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	answer = models.ForeignKey(Answer, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	answer_text = models.TextField(blank=True)
	correct = models.BooleanField(default=False)

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = StudentAnswersManager()

	def __str__(self):
		return self.id


class GradesManager(models.Manager):
	pass


class Grade(models.Model):
	from students.models import Student
	test = models.ForeignKey(Test, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	course = models.ForeignKey(Course, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	student = models.ForeignKey(Student, on_delete=models.deletion.SET_NULL, null=True, blank=True)
	grade = models.PositiveIntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])

	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = GradesManager()

	def __str__(self):
		return self.id

