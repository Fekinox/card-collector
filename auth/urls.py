from django.urls import path
from auth.views import (
    Login, Signup, Refresh
)

urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('signup/', Signup.as_view(), name="signup"),
    path('refresh/', Refresh.as_view(), name="refresh"),
]
