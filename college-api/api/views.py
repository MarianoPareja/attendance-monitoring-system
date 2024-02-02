from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import (
    AttendanceControl,
    Career,
    Classroom,
    Embedding,
    Student,
    Subject,
    SubjectInscription,
    SubjectSchedule,
)
from .serializer import (
    AttendanceControlSerializer,
    CareerSerializer,
    ClassroomSerializer,
    EmbeddingSerializer,
    StudentSerializer,
    SubjectInscriptionSerializer,
    SubjectScheduleSerializer,
    SubjectSerializer,
)


class AttendanceControlViewSet(viewsets.ModelViewSet):
    queryset = AttendanceControl.objects.all()
    serializer_class = AttendanceControlSerializer


class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class EmbeddingViewSet(viewsets.ModelViewSet):
    queryset = Embedding.objects.all()
    serializer_class = EmbeddingSerializer


class SubjectInscriptionViewSet(viewsets.ModelViewSet):
    queryset = SubjectInscription.objects.all()
    serializer_class = SubjectInscriptionSerializer


class SubjectScheduleViewSet(viewsets.ModelViewSet):
    queryset = SubjectSchedule.objects.all()
    serializer_class = SubjectScheduleSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


@api_view(["GET"])
def class_embeddings(request, class_id):
    """
    Return a list containing the embeddings of all the student within a class
    """

    if request.method == "GET":
        students = SubjectInscription.objects.filter(subject=class_id).values("student")
        student_list = list(students)
        student_list = [student["student"] for student in students]

        embeddings = Embedding.objects.filter(student__in=student_list)

        serializer = EmbeddingSerializer(embeddings, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def class_schedule(request, class_id, weekday):
    """
    Retrieves subject schedule based on class_id
    """
    if request.method == "GET":
        schedule = SubjectSchedule.objects.filter(subject=class_id, weekday=weekday)
        serializer = SubjectScheduleSerializer(schedule, many=True)
        return Response(serializer.data)


@api_view(["POST"])
def attendance_control_list(request):
    """
    Recieves assistance list for a class
    """
    if request.method == "POST":
        for student_assist in request.data:
            AttendanceControl.objects.create(
                subject=Subject.objects.get(pk=student_assist["subject"]),
                date=student_assist["date"],
                student=Student.objects.get(pk=student_assist["student"]),
                assistance=student_assist["assistance"],
            )

        return Response(
            {"message": "Attendance controls created successfully"},
            status=status.HTTP_201_CREATED,
        )
