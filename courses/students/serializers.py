from rest_framework import serializers

from core.enums import STATES
from courses.serializers import CourseBasicSerializer
from .models import Student, Progress


class StudentFullSerializer(serializers.ModelSerializer):
	course_count = serializers.SerializerMethodField()
	courses = serializers.SerializerMethodField()

	def get_course_count(self, obj):
		return obj.course_set.filter(is_active=True, state=STATES.Active).count()

	def get_courses(self, obj):
		return CourseBasicSerializer(obj.course_set.filter(is_active=True, state=STATES.Active), many=True, context={'user': self.context.get('user')}).data

	class Meta:
		model = Student
		fields = '__all__'


class StudentBasicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = ('slug', 'avatar', 'name', 'email', 'date_of_birth', 'facebook', 'twitter', 'linkedin')


class ProgressFullSerializer(serializers.ModelSerializer):
	class Meta:
		model = Progress
		fields = '__all__'
