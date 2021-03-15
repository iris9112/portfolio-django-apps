from django.urls import path
from todo_app.views import ListCreateTodo, RetrieveUpdateDestroyTodo


app_name = 'todo_app'


urlpatterns = [
    path('', ListCreateTodo.as_view(), name='list_create_todo'),
    path('<int:pk>/', RetrieveUpdateDestroyTodo.as_view(), name='detail_todo'),
]
