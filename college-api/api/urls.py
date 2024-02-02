from django.urls import include, path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r"AttendanceControl", views.AttendanceControlViewSet)
router.register(r"Career", views.CareerViewSet)
router.register(r"Classroom", views.ClassroomViewSet)
router.register(r"Embedding", views.EmbeddingViewSet)
router.register(r"Subject", views.SubjectViewSet)
router.register(r"Students", views.StudentViewSet)
router.register(r"SubjectInscription", views.SubjectInscriptionViewSet)
router.register(r"SubjectSchedule", views.SubjectScheduleViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("class_embeddings/<int:class_id>", views.class_embeddings),
    path("class_schedule/<int:class_id>/<int:weekday>", views.class_schedule),
    path("attendance_control_list", views.attendance_control_list),
]
