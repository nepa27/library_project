from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)
from django.views.generic import UpdateView


User = get_user_model()


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['username', 'email']
    template_name = 'users/user_edit.html'
    success_url = reverse_lazy('library:profile')

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']
