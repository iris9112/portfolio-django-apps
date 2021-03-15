from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

# documentation
schema_view = get_schema_view(
    title='ToDo API',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer]
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # api ToDo
    path('todo/', include('todo_app.urls', namespace='todo_app')),

    # authentication users
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),

    # documentation
    path('docs/', schema_view, name="docs"),
]
