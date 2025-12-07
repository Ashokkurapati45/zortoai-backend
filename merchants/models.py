# merchants/models.py
import secrets
import hashlib
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_raw_key():
    return secrets.token_urlsafe(32)

def hash_key(raw):
    return hashlib.sha256(raw.encode()).hexdigest()

class Merchant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="merchants")
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class APIKey(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="api_keys")
    name = models.CharField(max_length=120, blank=True, null=True)
    hashed_key = models.CharField(max_length=64, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)

    @classmethod
    def create_key(cls, merchant, name=None):
        raw = generate_raw_key()
        hashed = hash_key(raw)
        obj = cls.objects.create(merchant=merchant, name=name, hashed_key=hashed)
        return obj, raw
