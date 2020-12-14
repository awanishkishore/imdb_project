from django.urls import path

from accounts.views import SignUpView, LoginView
from contents.views import MyReviewView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("my-reviews/", MyReviewView.as_view(), name="my-reviews"),
]