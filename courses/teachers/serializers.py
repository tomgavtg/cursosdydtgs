from django.db.models import Count
from rest_framework import serializers

from core.enums import STATES
from .models import Teacher


class TeacherFullSerializer(serializers.ModelSerializer):
	course_count = serializers.SerializerMethodField()
	student_count = serializers.SerializerMethodField()

	def get_course_count(self, obj):
		return obj.course_set.filter(is_active=True, state=STATES.Active).count()

	def get_student_count(self, obj):
		return obj.course_set.filter(is_active=True, state=STATES.Active).aggregate(Count('students')).get('students__count')

	class Meta:
		model = Teacher
		fields = '__all__'


class TeacherBasicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Teacher
		fields = ('slug', 'avatar', 'name', 'email', 'date_of_birth', 'experience', 'facebook', 'twitter', 'linkedin', 'title')
