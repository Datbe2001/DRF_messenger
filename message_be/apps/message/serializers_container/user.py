from message_be.apps.message.models import User

from message_be.apps.message.serializers_container import (serializers)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
