from django.urls import path
from users import views as users_view
from .views import post_detail, post_list, post_search

urlpatterns = [
	path('', post_list, name='post_list'),
	# path('<int:pk>/info/', PostDetailView.as_view(), name='post_detail'),
	path('<int:pk>/', post_detail, name='post_detail'),
	path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
	path('<int:pk>/update/', users_view.PostUpdateView.as_view(), name='post_update'),
	path('<int:pk>/delete/', users_view.PostDeleteView.as_view(), name='post_delete'),

]


