import numpy as np

from api.models import *

# Crear carreras
career1 = Career.objects.create(name="IMT")
career2 = Career.objects.create(name="IND")


# Crear asignaturas
subject1 = Subject.objects.create(name="Control", career=career1)
subject2 = Subject.objects.create(name="Robotics", career=career1)
subject3 = Subject.objects.create(name="Embedded Systems", career=career1)

# Crear aulas
aula1 = Classroom.objects.create(name="B-11")
aula2 = Classroom.objects.create(name="B-115")

# Crear estudiantes
estudiante1 = Student.objects.create(
    name="Juan", lastname="Pérez", email="juan@example.com", cellphone="1234567890"
)
estudiante2 = Student.objects.create(
    name="María", lastname="González", email="maria@example.com", cellphone="9876543210"
)

# Crear inscripciones a asignaturas
inscripcion1 = SubjectInscription.objects.create()
inscripcion1.subject.add(subject1)
inscripcion1.student.add(estudiante1)

inscripcion2 = SubjectInscription.objects.create()
inscripcion2.subject.add(subject1)
inscripcion2.student.add(estudiante2)

# Crear horarios de asignaturas
horario1 = SubjectSchedule.objects.create(
    subject=subject1,
    classroom=aula1,
    weekday=1,
    start_time="08:00:00",
    end_time="10:00:00",
)
horario2 = SubjectSchedule.objects.create(
    subject=subject2,
    classroom=aula2,
    weekday=2,
    start_time="10:30:00",
    end_time="12:30:00",
)

# Crear registros de asistencia
asistencia1 = AttendanceControl.objects.create(
    subject=subject1,
    date="2024-01-24 09:00:00",
    student=estudiante1,
    assistance=True,
)
asistencia2 = AttendanceControl.objects.create(
    subject=subject1,
    date="2024-01-25 11:00:00",
    student=estudiante2,
    assistance=True,
)

# Crear embeddings
embedding1 = Embedding.objects.create(
    student=estudiante1,
    embedding=str(np.random.rand(1, 512)[0].tolist())
    .replace("[", "{")
    .replace("]", "}"),
)

embedding2 = Embedding.objects.create(
    student=estudiante2,
    embedding=str(np.random.rand(1, 512)[0].tolist())
    .replace("[", "{")
    .replace("]", "}"),
)
