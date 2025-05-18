from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/practice/', include('practice_test.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/answers/', include('user_answer.urls')),
    path('api/podskazki/', include('подсказки.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
