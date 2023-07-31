from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.get_home, name='home'),
    path('add-client-detail/', views.ClientDetail.as_view(),
         name='add-client-detail'),
    path('admin-screen/', views.AdminScreen.as_view(), name='admin-screen'),
    path('update-client-detail/<int:pk>/',
         views.UpdateClientDetails.as_view(), name='update'),
    path('delete-client/<int:pk>/', views.DeleteClient.as_view(), name='delete'),

    # Login and logout
    path('admin-login/', views.AdminLogin.as_view(), name='admin-login'),
    path('admin-logout/', LogoutView.as_view(next_page='home'), name='admin-logout'),

    # Category
    path('category/', views.ViewCategory.as_view(), name='category'),
    path('category-create/', views.CreateCategory.as_view(), name='category-create'),
    path('update-category/<int:pk>/',
         views.UpdateCategory.as_view(), name='update-category'),
    path('delete-category/<int:pk>/',
         views.DeleteCategory.as_view(), name='delete-category'),

    # sector
    path('sector/', views.ViewSector.as_view(), name='sector'),
    path('sector-create/', views.CreateSector.as_view(), name='sector-create'),
    path('update-sector/<int:pk>/',
         views.UpdateSector.as_view(), name='update-sector'),
    path('delete-sector/<int:pk>/',
         views.DeleteSector.as_view(), name='delete-sector'),

    # jobs
    path('job/', views.ViewJob.as_view(), name='jobs'),
    path('job-create/', views.CreateJob.as_view(), name='job-create'),
    path('update-job/<int:pk>/', views.UpdateJob.as_view(), name='update-job'),
    path('delete-job/<int:pk>/', views.DeleteJob.as_view(), name='delete-job'),

    # Users
    path('users/', views.ViewUsers.as_view(), name='user'),
    path('user-delete/<int:pk>/', views.DeleteUser.as_view(), name='user-delete'),
    path('update-user/<int:pk>/', views.update_user, name='update-user'),
    path('register-user/', views.register_user, name='register-user'),


    # Client
    path('client-login/', views.ClientLogin.as_view(), name='client-login'),
    path('client-detail-view/', views.ClientDetailShow.as_view(),
         name='client-detail-view'),







] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
