from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("residents/create/", ResidentCreateAPIView.as_view(), name="add_resident"),
    path("residents/", ResidentListAPIView.as_view(), name="view_residents"),
    path(
        "residents/<int:resident_id>",
        ResidentDetailAPIView.as_view(),
        name="view_resident",
    ),
    path(
        "residents/update/<int:resident_id>",
        ResidentUpdateAPIView.as_view(),
        name="edit_resident",
    ),
    path(
        "residents/delete/<int:resident_id>",
        ResidentDeleteAPIView.as_view(),
        name="delete_resident",
    ),
    path(
        "residents/filter/", FilterResidentListAPIView.as_view(), name="filter_resident"
    ),
    path("rooms/create/", RoomCreateAPIView.as_view(), name="add_room"),
    path("rooms/", RoomListAPIView.as_view(), name="view_rooms"),
    path("rooms/<int:room_id>", RoomDetailAPIView.as_view(), name="view_room"),
    path("rooms/update/<int:room_id>", RoomUpdateAPIView.as_view(), name="edit_room"),
    path("rooms/delete/<int:room_id>", RoomDeleteAPIView.as_view(), name="delete_room"),
    path("rooms/filter/", FilterRoomListAPIView.as_view(), name="filter_room"),
    path("student/create/", CreateStudentAPIView.as_view(), name="add_student"),
    path("student/login/", LoginAPIView.as_view(), name="login_student_in"),
    path("profile/", StudentProfileAPIView.as_view(), name="student-profile"),
    path("logout_basic_auth_user/", LogoutAPIView.as_view(), name="user_logout"),
    path("", home, name="homepage"),
    path("logout/", logout_view, name="logout"),
    path("google_login/", google_login, name="google_login"),
]
