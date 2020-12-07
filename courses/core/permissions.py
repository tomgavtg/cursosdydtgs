from functools import wraps

from django.utils.translation import gettext as _
from rest_framework import permissions, status
from rest_framework.response import Response

from core.enums import USER_TYPES
from users.models import User


class IsNotAuthenticated(permissions.BasePermission):
	def has_permission(self, request, view):
		return not request.user.is_authenticated


class IsAdmin(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.user.is_authenticated:
			if request.user.user_type == USER_TYPES.Admin:
				return True
		return False


class IsTeacher(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.user.is_authenticated:
			if request.user.user_type in [USER_TYPES.Teacher]:
				return True
		return False


class IsStudent(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.user.is_authenticated:
			if request.user.user_type in [USER_TYPES.Student]:
				return True
		return False


def check_permissions(perms):
	def decorator(view_func):
		@wraps(view_func)
		def _wrapped_view(self, request, *args, **kwargs):
			if User.objects.has_perm(request.user.id, perms):
				return view_func(self, request, *args, **kwargs)
			return Response(_("errors.permissions.403"), status=status.HTTP_403_FORBIDDEN)

		return _wrapped_view

	return decorator
