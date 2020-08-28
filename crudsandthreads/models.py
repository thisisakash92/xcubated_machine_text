from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=50)
    perfect_attendance = models.BooleanField(default=True)  # True if attended all classes.


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.present:
            student = Student.objects.get(id=self.student.id)
            student.perfect_attendance = False
            student.save()
        super(Attendance, self).save(*args, **kwargs)
