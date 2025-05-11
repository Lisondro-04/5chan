from django.urls import path
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView, UserProfileUpdateView, UserProfileDetailView
from django.contrib.auth import views as auth_views

app_name = 'blogapp'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # ✅ logout funcional
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='user_profile'),
    path('profile/<int:pk>/edit/', UserProfileUpdateView.as_view(), name='edit_profile'),
]
