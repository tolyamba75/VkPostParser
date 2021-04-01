from django.conf import settings

from rest_framework.permissions import BasePermission
from base64 import b64encode
from collections import OrderedDict
from hashlib import sha256
from hmac import HMAC
from typing import Dict
from urllib.parse import urlencode


class APISigningPermission(BasePermission):
    secret_key = settings.VK_SECRET_KEY

    def has_permission(self, request, view):
        query = request.query_params
        if not query or 'sign' not in query:
            return False
        return query["sign"] == sign_vk_params(query, self.secret_key)


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        if 'vk_viewer_group_role' not in request.query_params:
            return False
        return request.query_params['vk_viewer_group_role'] in ['editor', 'admin']


class TaskPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.method == "GET":
                group_id = request.query_params['group_id']
            else:
                group_id = request.data['group_id']
            return request.query_params['vk_group_id'] == group_id
        except KeyError:
            return False


def sign(query: Dict, secret_key):
    hash_code = b64encode(
        HMAC(
            secret_key.encode(), urlencode(query, doseq=True).encode(), sha256
        ).digest()
    )
    return hash_code.decode("utf-8")[:-1].replace("+", "-").replace("/", "_")


def sign_vk_params(query: Dict, secret_key):
    vk_subset = OrderedDict(sorted(x for x in query.items() if x[0][:3] == "vk_"))
    return sign(vk_subset, secret_key)
