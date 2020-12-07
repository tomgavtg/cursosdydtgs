from django.utils.translation import gettext as _
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.enums import STATES
from core.permissions import IsStudent
from core.serializers import PaginationSerializer, paginate_items
from courses.models import Course, Module, Section
from courses.serializers import CourseBasicSerializer, CourseFullSerializer, ModuleFullSerializer, SectionFullSerializer
from students.models import Student
from students.serializers import StudentFullSerializer


class StudentsViewSet(viewsets.ViewSet):

	@action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
	def get_student(self, request, *args, **kwargs):
		student = Student.objects.get_student(request.query_params.get('slug'))
		if student is not None:
			return Response(StudentFullSerializer(student, context={'user': request.user}).data, status=status.HTTP_200_OK)
		return Response(_('errors.student.404'), status=status.HTTP_400_BAD_REQUEST)

	@action(methods=['get'], permission_classes=[IsStudent], detail=False)
	def get_course(self, request, *args, **kwargs):
		course = Course.objects.get_course(request.query_params.get('slug'))
		if course is not None and request.user.student.course_set.filter(is_active=True, state=STATES.Active, id=course.id).exists():
			return Response(CourseFullSerializer(course, context={'user': request.user}).data, status=status.HTTP_200_OK)
		return Response(_('errors.course.404'), status=status.HTTP_400_BAD_REQUEST)

	@action(methods=['get'], permission_classes=[IsStudent], detail=False)
	def get_courses(self, request, *args, **kwargs):
		p_serializer = PaginationSerializer(data=request.query_params)
		if p_serializer.is_valid():
			student = request.user.student
			sort_by = 'name'
			if getattr(Course, p_serializer.validated_data.get('sortBy'), False):
				sort_by = p_serializer.validated_data.get('sortBy')
			if p_serializer.validated_data.get('descending'):
				sort_by = '-' + sort_by
			courses = student.course_set.filter(is_active=True, state=STATES.Active).order_by(sort_by)
			if p_serializer.validated_data.get('filter'):
				go_filter = p_serializer.validated_data.get('filter')
				courses = courses.filter(Q(name__icontains=go_filter) | Q(description__icontains=go_filter))
			data = paginate_items(courses, p_serializer.validated_data.get('itemsPerPage'), p_serializer.validated_data.get('page'), CourseBasicSerializer, {'user': request.user})
			return Response(data, status=status.HTTP_200_OK)
		return Response(p_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@action(methods=['get'], permission_classes=[IsStudent], detail=False)
	def get_module(self, request, *args, **kwargs):
		module = Module.objects.get_module(request.query_params.get('slug'))
		if module is not None and request.user.student.course_set.filter(is_active=True, state=STATES.Active, id=module.course.id).exists():
			return Response(ModuleFullSerializer(module, context={'user': request.user}).data, status=status.HTTP_200_OK)
		return Response(_('errors.module.404'), status=status.HTTP_400_BAD_REQUEST)

	@action(methods=['get'], permission_classes=[IsStudent], detail=False)
	def get_section(self, request, *args, **kwargs):
		section = Section.objects.get_section(request.query_params.get('slug'))
		if section is not None and request.user.student.course_set.filter(is_active=True, state=STATES.Active, id=section.module.course.id).exists():
			return Response(SectionFullSerializer(section, context={'user': request.user}).data, status=status.HTTP_200_OK)
		return Response(_('errors.section.404'), status=status.HTTP_400_BAD_REQUEST)

	@action(methods=['post'], permission_classes=[IsStudent], detail=False)
	def complete_section(self, request, *args, **kwargs):
		section = Section.objects.get_section(request.data.get('slug'))
		if section is not None and request.user.student.course_set.filter(is_active=True, state=STATES.Active, id=section.module.course.id).exists():
			Section.objects.complete_section(request.user.student, section)
			return Response(True, status=status.HTTP_200_OK)
		return Response(_('errors.section.404'), status=status.HTTP_400_BAD_REQUEST)
