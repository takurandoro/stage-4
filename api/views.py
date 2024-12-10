from rest_framework import generics
from .models import Room, Resident
from .serializers import (
    ResidentSerializer,
    RoomSerializer,
    StudentSerializer,
)
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User

from .filters import *
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.


# create user with error handling and proper message
class CreateStudentAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Successfuly added",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            },
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        )


class LoginAPIView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    # login using the basic authentication
    authentication_classes = [BasicAuthentication, SessionAuthentication]

    def post(self, request):

        try:
            student = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Invalid email",
                }
            )
        if not student.check_password(request.data["password"]):
            return Response(
                {
                    "success": False,
                    "message": "Password incorrect",
                }
            )

        token, created = Token.objects.get_or_create(user=student)
        serializer = StudentSerializer(instance=student)
        return Response(
            {
                "success": True,
                "message": "Logged in Successfuly",
                "token": token.key,
                "student": serializer.data,
            }
        )


class LogoutAPIView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "logged out successfuly"}, status=status.HTTP_200_OK
        )


class StudentProfileAPIView(generics.GenericAPIView):
    serializer_class = StudentSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"success": False, "message": "Only authenticated user is allowed"}
            )
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResidentCreateAPIView(generics.CreateAPIView):

    serializer_class = ResidentSerializer

    def post(self, request, format=None):
        # if not request.user.is_authenticated:
        #     return Response({"success": False, "message": "Please login first"})
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Resident added Successfuly",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            },
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


# paginatioin
class ResidentListAPIView(generics.ListAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    # allow any user
    permission_classes = [AllowAny]

    # set limitation for retrieving data
    pagination_class = LimitOffsetPagination


class ResidentDetailAPIView(generics.RetrieveAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    lookup_url_kwarg = "resident_id"

    def get(self, request, resident_id):

        try:
            resident = Resident.objects.get(pk=resident_id)
            serializer = ResidentSerializer(resident)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return Response(
                {"success": False, "message": "Resident doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResidentUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    lookup_url_kwarg = "resident_id"

    def put(self, request, resident_id):
        if not request.user.is_authenticated:
            return Response(
                {"success": False, "message": "Please login first"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            resident = Resident.objects.get(pk=resident_id)
        except Resident.DoesNotExist:
            return Response(
                {"success": False, "message": "Resident doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        resident.name = request.data["name"]
        resident.size = request.data["size"]
        resident.save()
        return Response(
            {"success": True, "message": "Resident Successfully updated!"},
            status=status.HTTP_200_OK,
        )


class ResidentDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    lookup_url_kwarg = "resident_id"

    def delete(self, request, resident_id):
        if not request.user.is_superuser:
            return Response(
                {"success": False, "message": "You are not an admin"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            resident = Resident.objects.get(pk=resident_id)
        except Resident.DoesNotExist:
            return Response({"success": False, "message": "Resident doesn't exist"})
        resident.delete()
        return Response({"success": False, "message": "Resident Successfully Deleted!"})


# filter Resident fields
class FilterResidentListAPIView(generics.ListAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ResidentFilter


class RoomCreateAPIView(generics.CreateAPIView):

    serializer_class = RoomSerializer

    def post(self, request, format=None):
        # if not request.user.is_authenticated:
        #     return Response({"success": False, "message": "Please login first"})
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Room added Successfuly",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            },
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


# Caching concept
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    # allow any user
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer
        ser = serializer(rooms, many=True)
        return Response(ser.data)


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "room_id"

    def get(self, request, room_id):

        try:
            room = Room.objects.get(pk=room_id)
            serializer = RoomSerializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response(
                {"success": False, "message": "Room doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RoomUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "room_id"

    def put(self, request, room_id):
        if not request.user.is_authenticated:
            return Response(
                {"success": False, "message": "Please login first"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response(
                {"success": False, "message": "Room doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        resident = Resident.objects.get(pk=request.data["resident"])
        room.name = request.data["name"]
        room.floor = request.data["floor"]
        room.room_type = request.data["room_type"]
        room.resident = resident
        room.save()
        return Response(
            {"success": True, "message": "Room Successfully updated!"},
            status=status.HTTP_200_OK,
        )


class RoomDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "room_id"

    def delete(self, request, room_id):
        if not request.user.is_superuser:
            return Response(
                {"success": False, "message": "You are not an admin"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response({"success": False, "message": "Room doesn't exist"})
        room.delete()
        return Response({"success": False, "message": "Room Successfully Deleted!"})


# filter Room fields
class FilterRoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RoomFilter


# hangle google login system
def home(request):
    return render(request, "home.html")


def google_login(request):
    return render(request, "google.html")


def logout_view(request):
    logout(request)
    return redirect("/")


from rest_framework import generics
from .models import Room, Resident
from .serializers import (
    ResidentSerializer,
    RoomSerializer,
    StudentSerializer,
)
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from .filters import *
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.


# create user with error handling and proper message
class CreateStudentAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Successfuly added",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            },
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
        )


class LoginAPIView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    # login using the basic authentication
    authentication_classes = [BasicAuthentication, SessionAuthentication]

    def post(self, request):

        try:
            student = User.objects.get(username=request.data["username"])
        except User.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Invalid username",
                }
            )
        if not student.check_password(request.data["password"]):
            return Response(
                {
                    "success": False,
                    "message": "Password incorrect",
                }
            )

        token, created = Token.objects.get_or_create(user=student)
        serializer = StudentSerializer(instance=student)
        return Response(
            {
                "success": True,
                "message": "Logged in Successfuly",
                "token": token.key,
                "student": serializer.data,
            }
        )


class LogoutAPIView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "logged out successfuly"}, status=status.HTTP_200_OK
        )


class StudentProfileAPIView(generics.GenericAPIView):
    serializer_class = StudentSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"success": False, "message": "Only authenticated user is allowed"}
            )
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResidentCreateAPIView(generics.CreateAPIView):

    serializer_class = ResidentSerializer

    def post(self, request, format=None):
        # if not request.user.is_authenticated:
        #     return Response({"success": False, "message": "Please login first"})
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Resident added Successfuly",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            },
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


# paginatioin
class ResidentListAPIView(generics.ListAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    # allow any user
    permission_classes = [AllowAny]

    # set limitation for retrieving data
    pagination_class = LimitOffsetPagination


class ResidentDetailAPIView(generics.RetrieveAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    lookup_url_kwarg = "resident_id"

    def get(self, request, resident_id):

        try:
            resident = Resident.objects.get(pk=resident_id)
            serializer = ResidentSerializer(resident)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Resident.DoesNotExist:
            return Response(
                {"success": False, "message": "Resident doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ResidentUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    lookup_url_kwarg = "resident_id"

    def put(self, request, resident_id):
        if not request.user.is_authenticated:
            return Response(
                {"success": False, "message": "Please login first"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            resident = Resident.objects.get(pk=resident_id)
        except Resident.DoesNotExist:
            return Response(
                {"success": False, "message": "Resident doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        resident.name = request.data["name"]
        resident.size = request.data["size"]
        resident.save()
        return Response(
            {"success": True, "message": "Resident Successfully updated!"},
            status=status.HTTP_200_OK,
        )


class ResidentDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    lookup_url_kwarg = "resident_id"

    def delete(self, request, resident_id):
        if not request.user.is_superuser:
            return Response(
                {"success": False, "message": "You are not an admin"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            resident = Resident.objects.get(pk=resident_id)
        except Resident.DoesNotExist:
            return Response({"success": False, "message": "Resident doesn't exist"})
        resident.delete()
        return Response({"success": False, "message": "Resident Successfully Deleted!"})


# filter Resident fields
class FilterResidentListAPIView(generics.ListAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ResidentFilter


class RoomCreateAPIView(generics.CreateAPIView):

    serializer_class = RoomSerializer

    def post(self, request, format=None):
        # if not request.user.is_authenticated:
        #     return Response({"success": False, "message": "Please login first"})
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Room added Successfuly",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "success": False,
                "message": serializer.errors,
            },
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


# Caching concept
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    # allow any user
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer
        ser = serializer(rooms, many=True)
        return Response(ser.data)


class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "room_id"

    def get(self, request, room_id):

        try:
            room = Room.objects.get(pk=room_id)
            serializer = RoomSerializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response(
                {"success": False, "message": "Room doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RoomUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "room_id"

    def put(self, request, room_id):
        if not request.user.is_authenticated:
            return Response(
                {"success": False, "message": "Please login first"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response(
                {"success": False, "message": "Room doesn't exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        resident = Resident.objects.get(pk=request.data["resident"])
        room.name = request.data["name"]
        room.floor = request.data["floor"]
        room.room_type = request.data["room_type"]
        room.resident = resident
        room.save()
        return Response(
            {"success": True, "message": "Room Successfully updated!"},
            status=status.HTTP_200_OK,
        )


class RoomDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "room_id"

    def delete(self, request, room_id):
        if not request.user.is_superuser:
            return Response(
                {"success": False, "message": "You are not an admin"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            room = Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return Response({"success": False, "message": "Room doesn't exist"})
        room.delete()
        return Response({"success": False, "message": "Room Successfully Deleted!"})


# filter Room fields
class FilterRoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RoomFilter


# hangle google login system
def home(request):
    return render(request, "home.html")


def google_login(request):
    return render(request, "google.html")


def logout_view(request):
    logout(request)
    return redirect("/")
