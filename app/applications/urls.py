from django.urls import path

from . import views

app_name = "applications"

urlpatterns = [
    path('post-recruitment/', views.post_recruitment, name='post-recruitment'),
]
