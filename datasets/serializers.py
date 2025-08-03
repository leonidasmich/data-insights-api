from rest_framework import serializers
from .models import Dataset, ColumnMetadata

class ColumnMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColumnMetadata
        fields = "__all__"
        

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = "__all__"
        read_only_fields = ['user', 'uploaded_at']