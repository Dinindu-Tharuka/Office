from typing import Any, Dict
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse
from .models import Client, Category, Sector, Job, Province, District, City
from .forms import FormFormat, ClientDetailForm, EmailLoginForm, CustomCategory, CustomSector, CustomJob
from .admin import ClientDetailResourse
from core.models import User
from django.contrib.auth import login, authenticate, logout

from .forms import RegistrationForm

# Generate PDF

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# PDF


def get_home(request):
    return render(request, 'api/home.html')

def create_client_detail(request):
    if request.method == 'POST':
        form = ClientDetailForm(request.POST)       
        if form.is_valid():
            form.save()
            
            # user = authenticate(username=username, password=password)
            # login(request, user)
            if request.user.is_staff:
                return redirect('user')
            return redirect('client-detail-view')
    else:
        form = ClientDetailForm()
        
    return render(request, 'api/add_client_detail.html', {'form': form})


class ClientDetail(CreateView):
    model = Client
    form_class = ClientDetailForm
    template_name = 'api/add_client_detail.html'

    def get_success_url(self) -> str:
        if not self.request.user.is_staff:
            return reverse_lazy('client-detail-view')
        return reverse_lazy('admin-screen')
    
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = ClientDetailForm()
        if not request.user.is_staff:
            form.fields['user'].queryset = User.objects.filter(id=request.user.id)
        return render(request, 'api/add_client_detail.html', {'form': form})

# Cient

# Admin


class AdminScreen(LoginRequiredMixin, ListView, FormView):
    model = Client
    context_object_name = 'clients'
    form_class = FormFormat
    template_name = 'api/admin_screen.html'
    paginate_by = 5

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        queary_set = self.get_queryset()
        dataset = ClientDetailResourse().export(queary_set)

        format = request.POST.get('format')

        if format != 'pdf':
            if format == 'xls':
                ds = dataset.xls

            response = HttpResponse(ds, content_type=f"{format}")
            response['Content-Disposition'] = f"attachment; filename=posts.{format}"

            return response
        # PDF
        template_path = 'api/pdf_client_detail_template.html'
        context = {
            'clients': self.get_queryset(),
        }
        # Render the template to a string
        template = get_template(template_path)
        html = template.render(context)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="client_list.pdf"'

        # Generate the PDF using ReportLab and xhtml2pdf
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Check if PDF generation was successful
        if pisa_status.err:
            return HttpResponse("PDF generation error", status=500)

        return response

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        province_id = self.request.GET.get('province')
        job_id = self.request.GET.get('job')
        sector_id = self.request.GET.get('sector')
        district_id = self.request.GET.get('district')
        city_id = self.request.GET.get('city')
        search_text = self.request.GET.get('search-area') or ''

        # Categories filter
        if category_id and not category_id == 'All Categories':
            queryset = queryset.filter(category_id=category_id)

        # Jobs filter
        if job_id and not job_id == 'All Jobs':
            queryset = queryset.filter(job_id=job_id)

        # Sectors filter
        if sector_id and not sector_id == 'All Sectors':
            queryset = queryset.filter(sector_id=sector_id)

        # Provinces filter
        if province_id and not province_id == 'All Provinces':
            queryset = queryset.filter(province_id=province_id)

        # Districts filter
        if district_id and not district_id == 'All Districts':
            queryset = queryset.filter(district_id=district_id)

        # Districts filter
        if city_id and not city_id == 'All Cities':
            queryset = queryset.filter(city_id=city_id)

        if search_text and search_text != '':
            queryset = queryset.filter(first_name__istartswith=search_text)

        return queryset

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Searching
        search_text = self.request.GET.get('search-area') or ''

        context['search_text'] = search_text
        context['count'] = Client.objects.all().count()

        # Filltering
        # Categories
        context['categories'] = Category.objects.all()

        # Jobs
        context['jobs'] = Job.objects.all()

        # Sectors
        context['sectors'] = Sector.objects.all()

        # Provinces
        context['provinces'] = Province.objects.all()

        # Districts
        context['districts'] = District.objects.all()

        # City
        context['cities'] = City.objects.all()

        return context

    ##################


class UpdateClientDetails(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientDetailForm
    template_name = 'api/add_client_detail.html'

    def get_success_url(self) -> str:
        if self.request.user.is_staff:
            return reverse_lazy('admin-screen')
        return reverse_lazy('client-detail-view')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['update'] = True
        return context
    
    def get(self, request: HttpRequest, pk, *args: str, **kwargs: Any) -> HttpResponse:
        client = Client.objects.filter(pk=pk).first()

        form =ClientDetailForm(instance=client)
       
        form.fields['user'].queryset = User.objects.filter(id=request.user.id)
        return render(request, 'api/add_client_detail.html', {'form': form})


class DeleteClient(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('admin-screen')

    def get_success_url(self) -> str:
        if self.request.user.is_staff:
            return reverse_lazy('admin-screen')
        return reverse_lazy('client-detail-view')


class AdminLogin(LoginView):
    template_name = 'api/admin_login.html'
    form_class = EmailLoginForm

    def get_success_url(self) -> str:
        if self.request.user.is_staff:
            return reverse_lazy('admin-screen')
        return reverse_lazy('admin-logout')


# Admin

# Category
class CreateCategory(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CustomCategory
    template_name = 'api/category_create.html'
    success_url = reverse_lazy('category')


class ViewCategory(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'api/category.html'
    paginate_by = 5

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['count'] = Category.objects.all().count()
        return context


class UpdateCategory(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CustomCategory
    success_url = reverse_lazy('category')
    template_name = 'api/category_create.html'


class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category')


# sector
class CreateSector(LoginRequiredMixin, CreateView):
    model = Sector
    form_class = CustomSector
    template_name = 'api/sector_create.html'
    success_url = reverse_lazy('sector')


class ViewSector(LoginRequiredMixin, ListView):
    model = Sector
    context_object_name = 'sectors'
    template_name = 'api/sector.html'
    paginate_by = 5

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['count'] = Sector.objects.all().count()
        return context


class UpdateSector(LoginRequiredMixin, UpdateView):
    model = Sector
    form_class = CustomSector
    success_url = reverse_lazy('sector')
    template_name = 'api/sector_create.html'


class DeleteSector(LoginRequiredMixin, DeleteView):
    model = Sector
    success_url = reverse_lazy('sector')


# Jobs
class CreateJob(LoginRequiredMixin, CreateView):
    model = Job
    form_class = CustomJob
    template_name = 'api/job_create.html'
    success_url = reverse_lazy('jobs')


class ViewJob(LoginRequiredMixin, ListView):
    model = Job
    context_object_name = 'jobs'
    template_name = 'api/jobs.html'
    paginate_by = 5


class UpdateJob(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = CustomJob
    success_url = reverse_lazy('jobs')
    template_name = 'api/job_create.html'


class DeleteJob(LoginRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('jobs')


# User
class ViewUsers(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'api/user.html'
    paginate_by = 6


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'api/user_confirm_delete.html'
    success_url = reverse_lazy('user')


# class UpdateUserView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = UserUpdateForm
#     template_name = 'authenticate/register_user.html'
#     success_url = reverse_lazy('user')

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context['is_update'] = True
#         return context


## Client

class ClientLogin(LoginView):
    template_name = 'api/client_login_register.html'
    form_class = EmailLoginForm

    def get_success_url(self) -> str:
        # id = self.request.user.id

        # client_id = Client.objects.get(user_id=id).id
        if not self.request.user.is_staff:
            return reverse_lazy('client-detail-view')
        else:
            return reverse_lazy('client-login')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class ClientDetailShow(ListView, LoginRequiredMixin):
    model = Client
    context_object_name = 'client'
    form_class = FormFormat
    template_name = 'api/client_detail_view.html'

    def get_queryset(self) -> QuerySet[Any]:
        user_id = self.request.user.id
        return super().get_queryset().filter(user_id=user_id).first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['client_available'] = True if self.get_queryset() != None else False
        return context


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # user = authenticate(username=username, password=password)
            # login(request, user)
            if request.user.is_staff:
                return redirect('user')
            return redirect('client-login')
    else:
        form = RegistrationForm()
    return render(request, 'authenticate/register_user.html', {'form': form})


def update_user(request, pk):    
    current_user = User.objects.get(id=request.user.id)

    if request.user.is_staff:        
        selected_user = User.objects.get(pk=pk)        
        form = RegistrationForm(request.POST or None, instance=selected_user)
        logout(request)
        login(request, selected_user)
        if form.is_valid():
            form.save()   

            login(request, current_user)
            return redirect('user')
        return render(request, 'authenticate/update_user.html', {'form':form, 'user': current_user})    
    elif not request.user.is_staff:        
        form = RegistrationForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()            
            login(request, current_user)  
            if current_user.is_staff:
                return redirect('user')          
            return redirect('client-detail-view')
        return render(request, 'authenticate/update_user.html', {'form':form, 'user':current_user})    
    else:
        return redirect('home')