from django.contrib import admin
from django.urls import re_path, include, path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('auth/', include('auth.urls')),
    path("api/", include("core.urls")),
    # path('members/', include('django.contrib.auth.urls')),
    # path('', include('mortest_frontend.urls')),
    path("api/users/", include("users.urls")),
    # path('', include('mortest_frontend.urls')),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Catch-All: These urls are handled by the single page BaseApp and react-router
    # path(r'^.*/', TemplateView.as_view(template_name="base-react.html"), name='base')
    # path(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
