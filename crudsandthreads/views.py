from django.http import JsonResponse
from django.urls import path, include
from rest_framework.response import Response

from crudsandthreads import models as ctmodels
from rest_framework import routers, serializers, viewsets, views


# no separate serializerspy file since it's only 2 serializers
# and adding another file only makes it difficult to navigate in this tiny MT
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ctmodels.Student
        fields = ['id', 'name', 'perfect_attendance']


class AttendanceSerializer(serializers.ModelSerializer):

    def get_student_name(self, obj):
        return obj.student.name

    student_name = serializers.SerializerMethodField()

    class Meta:
        model = ctmodels.Attendance
        fields = ['id', 'student', 'student_name', 'date', 'present']


class StudentDetailsSerializer(serializers.ModelSerializer):
    def get_attendance_record(self, obj):
        return AttendanceSerializer(ctmodels.Attendance.objects.filter(student=obj), many=True).data

    attendance_record = serializers.SerializerMethodField()

    class Meta:
        model = ctmodels.Student
        fields = ['id', 'name', 'perfect_attendance', 'attendance_record']


class StudentViewSet(viewsets.ModelViewSet):  # crud
    """
        TO view attendace list of a particular student, go to \n http://127.0.0.1:8000/students/<STUDENT_ID>
    """
    queryset = ctmodels.Student.objects.all()
    serializer_class = StudentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(StudentDetailsSerializer(instance).data)


class AttendanceViewSet(viewsets.ModelViewSet):  # crud
    queryset = ctmodels.Attendance.objects.all()
    serializer_class = AttendanceSerializer


class ThreadingExampleView(views.APIView):
    """
        Use POST to initiate threading functionality
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        return Response("use POST method to initiate threading. format {'x':123, 'y':123}")

    def post(self, request, format=None):
        return Response({"message": "Hello for today! See you tomorrow!"})
