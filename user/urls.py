from django.urls import path

from user.views import UserRegisterView, ManageUserView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-registration"),
    # path("login/", LoginUserView.as_view(), name="login"),
    path("me/", ManageUserView.as_view(), name="manage-user"),
]

app_name = "user"
