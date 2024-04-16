from django.urls import path
from carousel1.views import HomeView


urlpatterns = [
    path('', HomeView),
]