from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from PIL import Image
from django.contrib.auth.models import User
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

class CustomUser(AbstractUser):
	GENDER_CHOICES=(
		('M', 'Male'),
		('F', 'Female'),
		('T', 'Transgender')
		)
	nick_name = models.CharField(max_length=100, null=True, blank=True)
	age = models.PositiveIntegerField(null=True, blank=True)
	pic = models.ImageField(upload_to='media/images/',default='media/images/profile.jpg')
	dob = models.DateField(null=True)
	gender = models.CharField(max_length=20, default="not mentioned", choices=GENDER_CHOICES)

	def save(self, *args, **kwargs):
		super().save()
		img = Image.open(self.pic.path)
		width, height = img.size  # Get dimensions

		if width > 300 and height > 300:
			# keep ratio but shrink down
			img.thumbnail((width, height))

		# check which one is smaller
		if height < width:
			# make square by cutting off equal amounts left and right
			left = (width - height) / 2
			right = (width + height) / 2
			top = 0
			bottom = height
			img = img.crop((left, top, right, bottom))

		elif width < height:
			# make square by cutting off bottom
			left = 0
			right = width
			top = 0
			bottom = width
			img = img.crop((left, top, right, bottom))

		if width > 300 and height > 300:
			img.thumbnail((300, 300))

		img.save(self.pic.path)

	

	def __str__(self):
		return self.nick_name


	def get_absolute_url(self):
		return reverse('user_detail', args=[str(self.id)])

	



