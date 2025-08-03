from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    uploaded_file = models.FileField(upload_to="datasets/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ColumnMetadata(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="columns")
    name = models.CharField(max_length=150)
    dtype = models.CharField(max_length=50)
    unique_values = models.IntegerField()
    null_count = models.IntegerField()
