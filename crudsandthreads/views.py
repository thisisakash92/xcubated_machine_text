from django.urls import path, include
from crudsandthreads import models as ctmodels
from rest_framework import routers, serializers, viewsets


# no separate serializerspy file since it's only 2 serializers
# and adding another file only makes it difficult to navigate in this tiny MT
class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ctmodels.Student
        fields = ['name', 'perfect_attendance']


class AttendanceSerializer(serializers.HyperlinkedModelSerializer):

    def get_student_name(self, obj):
        return obj.student.name

    student_name = serializers.SerializerMethodField()

    class Meta:
        model = ctmodels.Attendance
        fields = ['student', 'student_name', 'date', 'present']


class StudentViewSet(viewsets.ModelViewSet):  # crud
    queryset = ctmodels.Student.objects.all()
    serializer_class = StudentSerializer


class AttendanceViewSet(viewsets.ModelViewSet):  # crud
    queryset = ctmodels.Attendance.objects.all()
    serializer_class = AttendanceSerializer
