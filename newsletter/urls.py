from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Newsletter API",
        default_version='v1',
        description="API that allows us to make a CRUD of newsletters, these newsletters can be classified by tags to "
                    "improve searches. "
                    "The necessary endpoints will also be built so that common users can subscribe to the newsletters "
                    "and "
                    "unsubscribe from them. "
                    "They will only be able to subscribe to the bulletins that have reached the target that was "
                    "defined when creating the "
                    "bulletin, in case the bulletins have not reached the target they will be available so that they "
                    "can vote for them.",
        contact=openapi.Contact(email="jacu29@gmiail.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('accounts.urls')),
    path('', include('newsletters.urls')),
]
