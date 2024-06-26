from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from jobs.models import Company
from users.forms import CustomUserCreationForm, EmployerForm, CompanyForm, CandidateForm
from users.models import Employer


# Create your views here.
class Login(LoginView):
    template_name = "users/login.html"
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context

    def get_success_url(self):
        return reverse_lazy("core:home")


class Register(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("core:home")
    template_name = "users/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Register"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        user.is_employer = form.cleaned_data.get("is_employer")
        user.save()
        login(self.request, user)
        return response


class RegisterEmployer(generic.UpdateView):
    form_class = EmployerForm
    template_name = "users/register_employer.html"
    success_url = reverse_lazy("core:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Register Employer"
        context["company_form"] = CompanyForm()
        context["companies"] = Company.objects.all()
        return context

    def get_object(self):
        # Assuming 'pk' is the primary key of the Employer instance to update
        employer_id = self.kwargs.get("pk")
        return get_object_or_404(Employer, pk=employer_id)

    def form_valid(self, form):
        employer = form.save(commit=False)
        employer.user = self.request.user
        employer.company = Company.objects.get(
            id=self.request.POST.get("company"))
        gender = self.request.POST.get("gender")
        gender_bool = True if gender == "male" else False
        employer.gender = gender_bool
        # if avatar:
        #     employer.avatar = avatar
        employer.save()
        return redirect("core:home")


@login_required
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("core:home")


class RegisterCandidate(generic.CreateView):
    form_class = CandidateForm
    success_url = reverse_lazy("users:profile")
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Profile"
        if hasattr(self.request.user, "candidate"):
            context["profile"] = self.request.user.candidate
        elif hasattr(self.request.user, "employer"):
            context["profile"] = self.request.user.employer

        return context

    def form_valid(self, form):
        candidate = form.save(commit=False)
        candidate.user = self.request.user
        candidate.save()
        messages.success(self.request, "Profile updated successfully")
        return redirect("users:profile")


def update_profile(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        print(phone)
        if request.user.is_employer == False:
            candidate = request.user.candidate
            candidate.full_name = full_name
            candidate.phone = phone
            candidate.save()
            return JsonResponse({"message": "Profile updated successfully"}, status=200)
        elif request.user.is_employer == True:
            employer = request.user.employer
            employer.full_name = full_name
            employer.phone = phone
            employer.save()
            return JsonResponse({"message": "Profile updated successfully"}, status=200)

    return JsonResponse({"message": "Profile updated successfully"}, status=200)
