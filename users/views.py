from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'U successfully register an account for {username}')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request, name):
	posts = Post.objects.filter(author__username=name)
	return render(request, 'users/another_profile.html', {'posts': posts,
														  'name': name})

# posts = Post.objects.filter(author=request.user)


@login_required
def myprofile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'U successfully update your account')
			return redirect('my_profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	posts = Post.objects.filter(author=request.user)
	return render(request, 'users/profile.html', {'posts': posts,
												  'u_form': u_form,
												  'p_form': p_form})


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'body', 'tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'body', 'tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'


	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False