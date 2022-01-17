from rest_framework import serializers


class TokenAPYSerializer(serializers.Serializer):
    token_ticker = serializers.CharField(required=True)
    reward_token_ticker = serializers.CharField(required=True)
