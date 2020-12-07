from django.utils.translation import gettext as _


class USER_TYPES:
	Admin = 'Z'
	Teacher = 'T'
	Student = 'S'
	choices = (
		(Admin, _("enums.user_types.admin")),
		(Teacher, _("enums.user_types.teacher")),
		(Student, _("enums.user_types.student")),
	)


class STATES:
	Active = 'A'
	Inactive = 'I'
	choices = (
		(Active, _("enums.states.active")),
		(Inactive, _("enums.states.inactive")),
	)


class LANGUAGES:
	English = 'en'
	Spanish = 'es'
	choices = (
		(English, _("enums.languages.english")),
		(Spanish, _("enums.languages.spanish")),
	)


class AUTHTOKEN_STATES:
	Used = 'U'
	Pending = 'P'
	choices = (
		(Used, _("enums.authtoken_states.used")),
		(Pending, _("enums.authtoken_states.pending"))
	)


class AUTHTOKEN_TYPES:
	PasswordChange = 'P'
	choices = (
		(PasswordChange, _("enums.authtoken_types.password_change")),
	)


class USER_PERMISSIONS:
	Users_R = 'users_r'
	Users_W = 'users_w'
	choices = (
		(Users_R, _('enums.user_permissions.users_r')),
		(Users_W, _('enums.user_permissions.users_w')),
	)


class QUESTION_TYPES:
	Multiple = 'M'
	Open = 'O'
	choices = (
		(Multiple, _("enums.question_types.multiple")),
		(Open, _("enums.question_types.open")),
	)
