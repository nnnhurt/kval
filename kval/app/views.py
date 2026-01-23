from django.http import JsonResponse
from rest_framework import viewsets
from .models import Students
from .serializers import StudentSerializer

def health_check(request):
    return JsonResponse({"status":"ok"})

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = []
