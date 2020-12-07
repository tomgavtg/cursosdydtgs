import datetime
import json
import uuid
from datetime import timedelta

from autoslug import AutoSlugField
from core.enums import STATES, USER_TYPES, AUTHTOKEN_TYPES, AUTHTOKEN_STATES, USER_PERMISSIONS
from core.utils import generate_token
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.datetime_safe import datetime


def jwt_get_secret_key(user_model):
	return user_model.jwt_secret


class UsersManager(BaseUserManager):
	def create_superuser(self, email, password, name=''):
		user = self.create_user(email, name, USER_TYPES.Admin, STATES.Active, password=password, is_staff=True)
		user.permissions = json.dumps([p[0] for p in USER_PERMISSIONS.choices])
		user.save()
		return user

	def create_user(self, email, name, user_type, state, password=None, is_staff=False):
		user = self.create_instance(email, name, user_type, state, password, is_staff)
		user.save()
		return user

	def register_user(self, name, email, password):
		user = self.create_instance(email, name, USER_TYPES.Admin, STATES.Active, password, False)
		user.save()
		return user

	def save_user(self, id, email, name, user_type, state, password, permissions=None):
		if not permissions:
			permissions = []
		else:
			permissions = json.loads(permissions)
		if id:
			user = self.get_user_by_id(id)
			if user is None:
				user = self.get_by_email(email)
		else:
			user = self.get_by_email(email)
		if user is None:
			user = self.create_instance(email, name, user_type, STATES.Active, password, False, permissions)
			user.save()
		else:
			user.name = name
			user.email = self.normalize_email(email)
			user.user_type = user_type
			user.state = state
			if password:
				user.set_password(password)
			if permissions and user_type == USER_TYPES.Admin:
				user.permissions = json.dumps(permissions)
			else:
				user.permissions = None
		user.save()
		return user

	def create_instance(self, email, name, user_type, state, password=None, is_staff=False, permissions=None):
		if not permissions:
			permissions = []
		if user_type not in [USER_TYPES.Admin, USER_TYPES.Teacher, USER_TYPES.Student]:
			user_type = USER_TYPES.Admin
		user = self.model(
			email=self.normalize_email(email),
			name=name,
			user_type=user_type,
			state=state,
			is_staff=is_staff
		)
		if permissions and user_type == USER_TYPES.Admin:
			user.permissions = json.dumps(permissions)
		else:
			user.permissions = None
		user.set_password(password)
		return user

	def has_perm(self, user_id, permissions=None):
		if not permissions:
			permissions = []
		user = self.get_user_by_id(user_id)
		return user.user_type == USER_TYPES.Admin or any(p in user.permissions for p in permissions)

	def reset_password(self, password, token):
		tok = AuthToken.objects.use_token(token, AUTHTOKEN_TYPES.PasswordChange)
		if tok is None:
			return None
		tok.user.set_password(password)
		tok.user.last_password_change = datetime.today()
		tok.user.save()
		return tok.user

	def check_email_exists(self, email, user_id=0):
		q = self.filter(email=self.normalize_email(email), is_active=True)
		if user_id:
			q = q.exclude(pk=user_id)
		return q.exists()

	def get_by_email(self, email, states=None):
		if states is None:
			try:
				return self.get(email=self.normalize_email(email), is_active=True)
			except ObjectDoesNotExist:
				return None
		try:
			return self.get(email=self.normalize_email(email), is_active=True, state__in=states)
		except ObjectDoesNotExist:
			return None

	def get_users(self):
		return self.filter(is_active=True).order_by('name')

	def get_user_by_id(self, user_id, state=None):
		try:
			if state is not None:
				return self.get(pk=user_id, is_active=True, state=state)
			else:
				return self.get(pk=user_id, is_active=True)
		except ObjectDoesNotExist:
			return None


class User(AbstractBaseUser):
	avatar = models.ImageField(
		upload_to="avatars/",
		max_length=255,
		blank=True,
		null=True
	)
	permissions = models.TextField(null=True, blank=True)
	user_type = models.CharField(max_length=1, choices=USER_TYPES.choices)
	state = models.CharField(max_length=1, choices=STATES.choices, default=STATES.Active)
	is_staff = models.BooleanField(default=False)
	slug = AutoSlugField(populate_from='email', unique=True)
	is_active = models.BooleanField(default=True)
	jwt_secret = models.UUIDField(default=uuid.uuid4)
	last_password_change = models.DateTimeField(default=None, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	name = models.TextField(max_length=255, null=True, blank=True)
	email = models.EmailField(max_length=255, unique=True)

	objects = UsersManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	def has_perm(self, perm, obj=None):
		return self.is_staff

	def has_module_perms(self, app_label):
		return self.is_staff

	def __str__(self):
		return self.email

	class Meta:
		unique_together = (("email", "is_active"),)


class AuthTokensManager(models.Manager):
	def create_password_token(self, user):
		token = self.create_instance(user, AUTHTOKEN_TYPES.PasswordChange)
		token.save()
		return token

	def create_instance(self, user, token_type):
		token = self.model(
			user=user,
			token_type=token_type,
			token=generate_token(user.email),
			expiry=datetime.now() + timedelta(days=settings.CUSTOM_TOKEN_EXPIRY_DAYS)
		)
		return token

	def check_token(self, token, token_type):
		try:
			return self.get(token=token, state=AUTHTOKEN_STATES.Pending, is_active=True, expiry__gte=datetime.now(), token_type=token_type)
		except self.model.DoesNotExist:
			return None

	def use_token(self, token, token_type):
		tok = self.check_token(token, token_type)
		if tok is None:
			return None
		tok.state = AUTHTOKEN_STATES.Used
		tok.save()
		return tok

	def get_pending_token(self, token_type, email):
		return self.filter(state=AUTHTOKEN_STATES.Pending, is_active=True, expiry__gte=datetime.now(), token_type=token_type, user__email=User.objects.normalize_email(email)).order_by('-expiry').first()


class AuthToken(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	state = models.CharField(max_length=1, choices=AUTHTOKEN_STATES.choices, default=AUTHTOKEN_STATES.Pending)
	token_type = models.CharField(max_length=1, choices=AUTHTOKEN_TYPES.choices)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	token = models.CharField(max_length=255, db_index=True)
	expiry = models.DateTimeField()

	objects = AuthTokensManager()

	def __str__(self):
		return self.token