from django.conf.urls import url, include
from django.contrib import admin

import Picturer.settings as setting
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(u'^picture/', include('picture.urls')),
]+static(setting.MEDIA_URL, document_root=setting.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))