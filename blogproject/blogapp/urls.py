from django.urls import path
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView
from .views import user_signup
from django.contrib.auth import views as auth_views
from . import views



app_name = 'blogapp'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # ✅ logout funcional
    path('signup/', user_signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.public_profile_view, name='public_profile'),
    path('tag/<str:tag_name>/', views.tag_detail, name='tag_detail')
]
