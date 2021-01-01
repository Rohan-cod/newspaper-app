from import_export import resources
from import_export.fields import Field
from .models import Article

class ArticleResource(resources.ModelResource):
	author = Field()
	class Meta:
		model = Article
		fields = ['title','date']

	@staticmethod
	def dehydrate_author(article):
		return f'{article.author.username}'