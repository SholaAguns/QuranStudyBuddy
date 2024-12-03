from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'

def delete_user_confirm(request):
    user = request.user

    if request.method == 'POST':
        user.delete()
        return redirect('home')
    else:
        return render(request, 'accounts/user_confirm_delete.html')



