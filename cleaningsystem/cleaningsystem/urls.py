from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('groups/', include('groups.urls')),
    path('tasks/', include('tasks.urls')),
    path('approvals/', include('approvals.urls'))
]
