from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):

	body = forms.CharField(widget=forms.TextInput(
		attrs={
		'id':'bod',

		'placeholder' :'Write an article...',
		}

		))
	class Meta:
		model = Article
		fields = ['title', 'body', 'pic']