from django.urls import path

from contents.views import ContentView, ReviewView


urlpatterns = [
    path("", ContentView.as_view()),
    path("<str:uuid>/reviews/", ReviewView.as_view()),
]