"""django_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from ec3exceldump import views

urlpatterns = [
	path('ec3', views.index),
	path('ec3/viewreport/<int:id>', views.viewreport),
	path('ec3/exceptions/<int:id>', views.exceptions),
	path('ec3/retrieve/account/<int:id>', views.retrieveaccount),
	path('ec3/retrieve/meter/<int:id>', views.retrievemeter),
	path('ec3/updatexception/<int:id>', views.updatexception),
	path('ec3/createcsv/<int:id>', views.createcsv),
	path('ec3/reportupdate', views.reportupdate),
	url(r'^admin/', admin.site.urls),
]
