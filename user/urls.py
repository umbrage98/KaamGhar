from django.urls import path
from .views import LoginView, CreateUserView, UserLogoutView, CurrentUserView, UpdateProfileView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  # Endpoint for user login
    path('create/', CreateUserView.as_view(), name='create_user'),  # Endpoint for user registration
    path('logout/', UserLogoutView.as_view(), name='logout_user'),  # Endpoint for user registration
    path('me/', CurrentUserView.as_view(), name='me_user'),  # Endpoint for user registration
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),


]
