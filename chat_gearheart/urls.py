from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django_registration.backends.one_step.views import RegistrationView

#from chat_gearheart.views import index


urlpatterns = [
    #url(r'^$', index, name='homepage'),  # The start point for index view
    url(r'^login/$', LoginView.as_view(), name='login'),  # The base django login view
    url(r'^logout/$', LogoutView.as_view(), name='logout'),  # The base django logout view
url(r'^register/$',   RegistrationView.as_view(success_url='/'), name='register'),
    #url(r'^admin/', admin.site.urls),  # etc :D
]