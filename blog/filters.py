import django_filters
from django_filters import CharFilter

from .models import Post


class Filter(django_filters.FilterSet):
	title = CharFilter(field_name='title', lookup_expr='icontains')
	tags = Post.tags.all()
	class Meta:
		model = Post
		fields = ['title', 'author']


