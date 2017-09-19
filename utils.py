import random
import string


def get_uniq_name():
	return ''.join(random.sample(string.ascii_letters + string.digits, 7))
