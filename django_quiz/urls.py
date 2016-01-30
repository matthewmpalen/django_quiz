# Django
from django.conf.urls import include, url
from django.contrib import admin

# Local
from .views import HomepageView

urlpatterns = [
    url(r'^$', HomepageView.as_view(), name='homepage'), 
    url(r'^admin/', admin.site.urls), 
    url(r'^content/', include('django_quiz.content.urls'))
]
