from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from scorecard.models import Scorecard
from . import forms

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        # Save the new user
        user = form.save()

        # Create a Scorecard for the new user
        Scorecard.objects.create(user=user)

        # Log the user in (optional)
        login(self.request, user)

        return redirect(self.success_url)  # Redirect to success page

def delete_user_confirm(request):
    user = request.user

    if request.method == 'POST':
        user.delete()
        return redirect('home')
    else:
        return render(request, 'accounts/user_confirm_delete.html')



