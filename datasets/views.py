import pandas as pd
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Dataset, ColumnMetadata
from .serializers import DatasetSerializer, ColumnMetadataSerializer


class DatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing datasets.
    Allows upload of CSV/Excel files and provides a summary of data.
    """
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return datasets for the logged-in user
        return Dataset.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Save dataset to DB
        dataset = serializer.save(user=self.request.user)

        try:
            # Try to load CSV/Excel
            file_path = dataset.uploaded_file.path
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")

            # Create metadata for each column
            for col in df.columns:
                ColumnMetadata.objects.create(
                    dataset=dataset,
                    name=col,
                    dtype=str(df[col].dtype),
                    unique_values=df[col].nunique(),
                    null_count=df[col].isnull().sum()
                )
        except Exception as e:
            print(f"[ERROR] Could not process file: {e}")

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """
        Return a statistical summary of the dataset using pandas.describe()
        """
        dataset = self.get_object()
        try:
            file_path = dataset.uploaded_file.path
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                return Response({"error": "Unsupported file format"}, status=400)

            summary = df.describe(include='all').fillna('').to_dict()
            return Response(summary)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ColumnMetadataViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only ViewSet for column metadata.
    """
    serializer_class = ColumnMetadataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only columns related to the user's datasets
        return ColumnMetadata.objects.filter(dataset__user=self.request.user)
