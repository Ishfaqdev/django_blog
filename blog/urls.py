from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog_list, name='blog'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>/update/', views.edit_post, name='edit_post'),
    path('blog_detail/<str:category_slug>/<str:post_slug>/',
         views.blog_detail, name='blog_detail'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('add-post', views.add_post, name='add_post'),
    path('delete/<int:post_id>/',
         views.delete_post, name='delete_post'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]
