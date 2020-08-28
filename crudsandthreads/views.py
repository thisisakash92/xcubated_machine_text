import json
import subprocess
from django.http import JsonResponse
from django.urls import path, include
from rest_framework.response import Response
import crudsandthreads.multithreading_example as mtx
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
        Use GET method to initiale multiprocess example using a function in this program.
        The default get response is a rest api template
        goto http://127.0.0.1:8000/threading_example?format=json for GETting plain JSON output.

        Use POST method(without inputs) to initiate the mutiprocess example from a separate py script

        Each element of the output is in the following format {process count: sum of two random numbers}
    """

    def is_valid_json(self, maybe_json):
        try:
            if type(maybe_json) is 'dict':
                json.dumps(maybe_json)
            elif type(maybe_json) is 'str':
                json.loads(maybe_json)
            else:
                Exception('Input must be string or dict type')
        except ValueError as err:
            return False
        return True

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        proc_result_dict = mtx.start_multiprocessing()
        if self.is_valid_json(proc_result_dict):
            return Response(proc_result_dict)
        else:
            raise Exception('Invalid JSON data received from child process.')

    def post(self, request, format=None):
        output_data = dict()
        proc = subprocess.Popen(['python3', './crudsandthreads/multithreading_example.py', ], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        proc_result_str = proc.communicate()[0].rstrip()
        if self.is_valid_json(proc_result_str):
            return Response(proc_result_str)
        else:
            raise Exception('Invalid JSON data received from child process.')
