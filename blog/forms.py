from django import forms
from .models import Comment, Post



class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')


class FindForm(forms.Form):
	tag = forms.ModelChoiceField(queryset=Post.tags.all())


class SearchForm(forms.Form):
	query = forms.CharField()