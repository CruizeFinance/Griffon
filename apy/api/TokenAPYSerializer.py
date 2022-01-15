from rest_framework import serializers


class TokenAPYSerializer(serializers.Serializer):
    token_ticker = serializers.CharField(required=False, default="USDC")
    reward_token_ticker = serializers.CharField(required=False, default="WETH")
