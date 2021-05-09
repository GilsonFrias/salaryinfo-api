"""salaryinfo_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from empleados.views import HomeView
from empleados.exceptions import my_exception_handler

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
]

#handler400 = 'rest_framework.exceptions.bad_request'
#'empleados.exceptions.my_exception_handler'#'empleados.views.error_400'
#handler403 = 'empleados.views.error_403'
#handler404 = 'empleados.views.error_404'
#handler500 = my_exception_handler.as_view()#'rest_framework.exceptions.server_error' 
#handler500 = 'empleados.exceptions.my_exception_handler'#'empleados.views.custom_exec_handler'
