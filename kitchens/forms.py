from django.forms import ModelForm
from .models import Kitchen


# creating a form
class KitchensForm(ModelForm):

	# create meta class
	class Meta:
		# specify model to be used
		model = Kitchen

		# specify fields to be used
		fields = [
			"kitchen_name",
			"kitchen_desc",
			"cuisine_type",
			"kitchen_address",
		]
