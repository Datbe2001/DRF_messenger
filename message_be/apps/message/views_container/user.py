from message_be.apps.message.serializers import (
    UserSerializer
)

from message_be.apps.message.views_container import (
    Response,
    permissions, GenericAPIView
)


class UserDetailViewSet(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
