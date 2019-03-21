from .forms import AccountsUserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = AccountsUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
