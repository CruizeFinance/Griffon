from django.conf.urls import url

from apy.api.views import TokenAPYViewset

urlpatterns = [
    url("", TokenAPYViewset.as_view({"get": "list"}), name="token_apy"),
]
