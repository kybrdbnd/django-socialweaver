"""landing_steps_ajax URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from company_detail.views import (
    home, customer_landing_step, question_create, like)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='main_home'),
    url(r'^landing_steps/', customer_landing_step,
        name='customer_landing_step'),

    url(r'^company/', include('company_detail.urls', namespace="company")),
    url(r'^accounts/', include('allauth.urls')),
    # question create
    url(r'question/', question_create, name='question_create'),

    # likes/dislikes create
    url(r'like/', like, name='like'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
