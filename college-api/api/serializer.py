from rest_framework import serializers

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


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class EmbeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embedding
        fields = "__all__"


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"


class AttendanceControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceControl
        fields = "__all__"


class SubjectInscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectInscription
        fields = "__all__"


class SubjectScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectSchedule
        fields = "__all__"
