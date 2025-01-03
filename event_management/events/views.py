from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from .models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.order_by('-pk').select_related('owner').prefetch_related('attendees')
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == ['create']:
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            response = serializer.create(serializer.validated_data)
        return Response(
            {
                "data": serializer.data,  
                "message": "Event created successfully",
                "status": True,
                "status_code": status.HTTP_201_CREATED,
            },
            status=status.HTTP_201_CREATED 
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = EventSerializer(queryset, many=True)
        return Response(
            {
                "data": serializer.data,
                "message": "All events retrieved successfully",
                "status": True,
                "status_code": status.HTTP_200_OK,
            },
        )
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
                {
                    "data": response.data,
                    "message": "Event retrieved successfully",
                    "status": True,
                    "status_code": status.HTTP_200_OK,
                },
            )
    
    def destroy(self, request, *args, **kwargs):
        resposne = super().destroy(request, *args, **kwargs)
        return Response(
                    {
                        "data": {},
                        "message": "Event delete successfully",
                        "status": True,
                        "status_code": status.HTTP_200_OK,
                    },
                )
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
                        {
                            "data": response.data,
                            "message": "Event update successfully",
                            "status": True,
                            "status_code": status.HTTP_200_OK,
                        },
                    )
    
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response(
                        {
                            "data": response.data,
                            "message": "Event update successfully",
                            "status": True,
                            "status_code": status.HTTP_200_OK,
                        },
                    )



