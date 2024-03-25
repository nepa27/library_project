from django.views.generic.edit import CreateView
from django.urls import path, reverse_lazy

from .forms import CustomUserCreationForm
from .views import UserUpdateView

app_name = 'users'

urlpatterns = [
    path('user/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration',
    ),
]
