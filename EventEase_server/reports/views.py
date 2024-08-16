from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from accounts.permissions import IsAdminUser,IsOwner,IsOwnerOrAdminUser,IsServiceOwnerOrAdmin, DefaultOrIsAdminUser
from reviews.models import Review
from services.models import Service
from .serializers import ReportReviewSerializer,ReportServiceSerializer
from .models import ReportReview,ReportService


class ReportReviewAPIView(APIView):

    def post(self, request, service_pk, review_pk,report_pk= None):
        reporter = request.user
        review = get_object_or_404(Review, pk=review_pk)
        if ReportReview.objects.filter(reporter = reporter, review = review, is_solved = False).exists():
            return Response({'message':'you already have an unsolved report on this review'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReportReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, service_pk, review_pk,report_pk=None):
        if request.user.is_superuser:
            review_reports = ReportReview.objects.filter(review_id=review_pk)
        else :
            review_reports = ReportReview.objects.filter(review_id=review_pk, reporter = request.user)
        serializer = ReportReviewSerializer(review_reports, many=True)
        return Response(serializer.data)

    def delete(self, request, service_pk, review_pk,report_pk):
        review_report = get_object_or_404(ReportReview, id = report_pk )
        self.check_object_permissions(request, review_report)
        review_report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [DefaultOrIsAdminUser()]
        elif self.request.method == 'DELETE':
            return [IsOwnerOrAdminUser()] 
    

class SolveReportReviewAPIView(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, service_pk, review_pk,report_pk):
        report = get_object_or_404(ReportReview,id =report_pk )
        report.is_solved = True
        report.solved_by = request.user
        report.save()
        return Response(status=status.HTTP_200_OK)
    

class ReportServiceAPIView(APIView):
    
    def post(self, request, service_pk, report_pk=None):
        reporter = request.user
        service = get_object_or_404(Service, pk=service_pk)
        if ReportService.objects.filter(reporter=reporter, service=service, is_solved=False).exists():
            return Response({'message': 'You already have an unsolved report on this service'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReportServiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user, service=service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, service_pk, report_pk=None):
        if request.user.is_superuser:
            service_reports = ReportService.objects.filter(service_id=service_pk)
        else:
            service_reports = ReportService.objects.filter(service_id=service_pk, reporter=request.user)
        serializer = ReportServiceSerializer(service_reports, many=True)
        return Response(serializer.data)

    def delete(self, request, service_pk, report_pk):
        service_report = get_object_or_404(ReportService, id=report_pk)
        self.check_object_permissions(request, service_report)
        service_report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [DefaultOrIsAdminUser()]
        elif self.request.method == 'DELETE':
            return [IsOwnerOrAdminUser()]


class SolveReportServiceAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request, service_pk, report_pk):
        report = get_object_or_404(ReportService, id=report_pk)
        report.is_solved = True
        report.solved_by = request.user
        report.save()
        return Response(status=status.HTTP_200_OK)
    

class ListAllReviewsReports(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = ReportReview.objects.all()
    serializer_class = ReportReviewSerializer


class ListAllServicesReports(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = ReportService.objects.all()
    serializer_class = ReportServiceSerializer
