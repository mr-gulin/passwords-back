from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        return {"token": attrs["token"]}
