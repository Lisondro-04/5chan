from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment, Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django import forms


# Blog Views
class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog_form.html'

    def dispatch(self, request, *args, **kwargs):
        # Limitar a una publicación por usuario
        if Blog.objects.filter(author=request.user).exists():
            messages.error(request, "Ya has publicado un blog. No puedes subir más publicaciones por ahora.")
            return redirect('blogapp:blog_list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_input'] = self.request.POST.get('tags', '')  # Para repoblar si hay error
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        tags_str = self.request.POST.get('tags', '')
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            self.object.tags.add(tag)
        return response

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})


# Review Views - corregido para evitar error y controlar duplicados
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])

        # Evitar que el usuario publique más de una reseña en el mismo blog
        if Review.objects.filter(blog=self.blog, reviewer=request.user).exists():
            messages.warning(request, "Ya has dejado una reseña para este blog.")
            return redirect('blogapp:blog_detail', pk=self.blog.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog = self.blog  # asignación correcta
        messages.success(self.request, "Tu reseña fue enviada con éxito.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.blog.pk})


# Comment Views
class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})


# User Signup View
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('blogapp:blog_list')
            else:
                form.add_error(None, 'Error al autenticar al nuevo usuario.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# Tag Detail View
def tag_detail(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    blogs = tag.blogs.all()
    return render(request, 'blog/tag_detail.html', {'tag': tag, 'blogs': blogs})


# User Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('blogapp:blog_list')
        return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas'})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')


# User Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('blogapp:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blogapp/profile.html', {'form': form})


# Vista de perfil público
def public_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'blogapp/public_profile.html', {'user': user})
