import pandas as pd
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Dataset, ColumnMetadata
from .serializers import DatasetSerializer, ColumnMetadataSerializer

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        dataset = serializer.save(user=self.request.user)
        df = pd.read_csv(dataset.uploaded_file.path)

        for col in df.columns:
            ColumnMetadata.objects.create(
                dataset=dataset,
                name=col,
                dtype=str(df[col].dtype),
                unique_values=df[col].nunique(),
                null_count=df[col].isnull().sum()
            )

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        dataset = self.get_object()
        df = pd.read_csv(dataset.uploaded_file.path)
        summary = df.describe(include='all').fillna('').to_dict()
        return Response(summary)
