from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.enums import STATES
from core.permissions import IsTeacher
from courses.serializers import CourseTeacherFullSerializer
from teachers.models import Teacher
from teachers.serializers import TeacherFullSerializer


class TeachersViewSet(viewsets.ViewSet):

	@action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
	def get_teacher(self, request, *args, **kwargs):
		teacher = Teacher.objects.get_teacher(request.query_params.get('slug'))
		if teacher is not None:
			return Response(TeacherFullSerializer(teacher).data, status=status.HTTP_200_OK)
		return Response(_('errors.teacher.404'), status=status.HTTP_400_BAD_REQUEST)

	@action(methods=['get'], permission_classes=[IsTeacher], detail=False)
	def get_courses(self, request, *args, **kwargs):
		return Response(CourseTeacherFullSerializer(request.user.teacher.course_set.filter(is_active=True, state=STATES.Active), many=True).data, status=status.HTTP_200_OK)
