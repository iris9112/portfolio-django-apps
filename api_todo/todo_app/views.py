from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from todo_app.models import Todo
from todo_app.permissions import IsOwner
from todo_app.serializers import TodoSerializer


class ListCreateTodo(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsOwner,)
    serializer_class = TodoSerializer

    def get_queryset(self):
        queryset = Todo.objects.filter(user=self.request.user).order_by('-id')
        description = self.request.query_params.get('description', None)
        if description:
            return queryset.filter(description__icontains=description)
        return queryset

    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = self.request.user
        serializer = TodoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyTodo(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwner,)
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
