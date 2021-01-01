from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from PIL import Image



class Article(models.Model):
	title = models.CharField(max_length=255)
	body = models.TextField()
	pic = models.ImageField(upload_to='images/',default='IMG')
	date = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)
	author = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE,
		)

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
		return self.title


	def get_absolute_url(self):
		return reverse('article_detail', args=[str(self.id)])


class Comment(models.Model): # new
	article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments',)
	comment = models.CharField(max_length=140)
	author = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE,
	)

	def __str__(self):
		return self.comment

	@staticmethod
	def get_absolute_url():
		return reverse('article_list')

