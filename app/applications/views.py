from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic
from django.db.models import Q

from applications.forms import CVForm
from applications.models import CV, Application
from jobs.models import Company, Job
from users.forms import RecruitmentForm


class CompanyDetailView(generic.DetailView):
    template_name = "applications/company.html"
    model = Company
    context_object_name = "company"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detail Job"
        # Get all the recruitments belongs to that company
        context["recruitment"] = Job.objects.filter(company=self.object)
        return context


# Create your views here.
@login_required
def post_recruitment(request):
    if request.method == "POST":
        form = RecruitmentForm(request.POST, user=request.user)
        if form.is_valid():
            recruitment = form.save(commit=False)
            recruitment.slug = slugify(recruitment.title)
            recruitment.save()
            return redirect("core:home")
    else:
        if hasattr(request.user, "employer") and request.user.employer.company:
            form = RecruitmentForm(
                user=request.user, initial={
                    "company": request.user.employer.company}
            )
        else:
            return redirect("users:register-employer", pk=request.user.employer.id)
    return render(request, "applications/post_recruitment.html", {"form": form})


class SubmitCV(generic.CreateView):
    form_class = CVForm

    def form_valid(self, form):
        job = Job.objects.get(slug=self.request.POST.get("job_slug"))
        response = super().form_valid(form)
        cv = form.instance
        cv.user = self.request.user
        cv.job = job
        cv.save()
        return response

    def get_success_url(self):
        job_slug = self.request.POST.get("job_slug")
        return reverse_lazy("jobs:detail-job", kwargs={"slug": job_slug})


@login_required
def view_applicant_cv(request):
    if hasattr(request.user, "employer"):
        company = request.user.employer.company
        jobs = Job.objects.filter(
            company=company
        )  # Filter all the job that belongs to the company

        job_applications = {}
        for job in jobs:
            cvs = CV.objects.filter(
                job=job
            )  # Filter all the cv that applied to the job that belongs to the company
            job_applications[job] = (
                cvs  # Store the cv in the dictionary with the job as the key
            )

        return render(
            request,
            "applications/view_cv.html",
            {"job_applications": job_applications, "company": company},
        )
    return redirect("core:home")


def cv_detail(request, pk):
    cv = CV.objects.get(pk=pk)
    return render(request, "applications/cv_detail.html", {"cv": cv})


def reject_cv(request, cv_id):
    cv = CV.objects.get(pk=cv_id)
    cv.status = "Rejected"
    cv.save()

    return redirect("applications:view-applicant-cv")


def accept_cv(request, cv_id):
    cv = CV.objects.get(pk=cv_id)
    cv.status = "Accepted"
    cv.save()
    return redirect("applications:view-applicant-cv")


def search_job(request):
    if request.method == "GET":
        search = request.GET.get("q")
        jobs = Job.objects.filter(title__icontains=search)
        return render(
            request, "applications/searchForm.html", {
                "jobs": jobs, "q": search}
        )
    else:
        return render(request, "applications/searchForm.html")


def search_job_keyword(request):
    if request.method == "GET":
        search_title = request.GET.get("q", "")
        search_keyword = request.GET.get("city", "")
        search_experience = request.GET.get("experience", "")

        jobs = Job.objects.all()

        if search_experience:
            if search_experience == "<1":
                jobs = jobs.filter(experience_min__lte=1)
            elif search_experience == ">5":
                jobs = jobs.filter(experience_min__gt=5)
            else:
                try:
                    experience = int(search_experience)
                    if experience == 0:
                        jobs = jobs.filter(
                            experience_min__isnull=True, experience_max__isnull=True
                        )
                    else:
                        jobs = jobs.filter(
                            Q(experience_min__gte=experience)
                            & Q(experience_max__lte=experience)
                        )
                except ValueError:
                    return redirect("core:home")

        if search_title:
            jobs = jobs.filter(title__icontains=search_title)

        if search_keyword:
            jobs = jobs.filter(keywords__name__icontains=search_keyword)

        return render(
            request,
            "applications/searchForm.html",
            {
                "jobs": jobs,
                "q": search_title,
                "search_experience": search_experience,
                "search_keyword": search_keyword,
            },
        )


class CompanyListView(generic.ListView):
    model = Company
    template_name = "applications/companies_list.html"
    context_object_name = "companies"
    paginate_by = 10
    ordering = ["-created_at"]
    extra_context = {"title": "Company List"}


def user_applied_jobs(request):
    user = request.user
    candidate = user.candidate
    applications = Application.objects.filter(
        candidate=candidate).select_related("job")
    jobs = [app.job for app in applications]

    return render(request, "applications/applied_jobs.html", {"jobs": jobs})
