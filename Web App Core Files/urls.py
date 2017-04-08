from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Examples:
     url(r'^$', 'newsletter.views.home', name='home'),
     url(r'^contact/$','newsletter.views.contact', name='contact'),
     url(r'^about/$','newsletter.views.about', name='about'),
    # url(r'^blog/', include('blog.urls')),
     url(r'^index/$','twitter.views.index', name='index'),
     url(r'^main/$','twitter.views.main', name='main'),
     url(r'^crawling/$','twitter.views.crawling', name='crawling'),
     url(r'^summarization/$','twitter.views.summarization', name='summarization'),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^accounts/', include('registration.backends.default.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
