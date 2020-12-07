import hashlib
import random
import string
from datetime import datetime
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.files import File


def generate_token(data):
	random_string = str(random.random()).encode('utf8')
	salt = hashlib.sha1(random_string).hexdigest()[:5]
	salted = (salt + data).encode('utf8')
	return hashlib.sha1(salted).hexdigest()


def build_api_url(*args):
	return '/'.join((settings.CURRENT_SERVER_HOME, 'api', settings.CURRENT_API_VERSION, *args)) + '/'


def build_site_url(*args):
	return '/'.join((settings.CURRENT_CLIENT_HOME, *args))


def random_password(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return ''.join(random.choice(chars) for _ in range(size))


def upper_code_generator(prefix='', size=10, chars=string.ascii_uppercase + string.digits):
	return prefix + ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def lower_code_generator(prefix='', size=10, chars=string.ascii_lowercase + string.digits):
	return prefix + ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def mix_code_generator(prefix='', size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
	return prefix + ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def number_code_generator(prefix='', size=6, chars=string.digits):
	return prefix + ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def date_number_code_generator(prefix='', size=6, chars=string.digits):
	d = datetime.now()
	return prefix + ''.join([str(d.year), str(d.month), str(d.day), str(d.hour), str(d.minute), str(d.second)]) + ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def compress(image, image_type):
	im = Image.open(image)
	im_io = BytesIO()
	im.save(im_io, image_type, quality=70)
	new_image = File(im_io, name=image.name)
	return new_image
