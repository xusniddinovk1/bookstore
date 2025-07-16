import io
import xlsxwriter
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .filters import OrderFilter
from .serializers import OrderSerializer
from .models import Order
from rest_framework import viewsets


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter
    ordering_fields = ['created_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], url_path='export/pdf', permission_classes=[IsAdminUser])
    def export_pdf(self, request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 50, "Buyurtmalar ro'yxati (PDF)")

        p.setFont("Helvetica", 10)
        y = height - 80

        orders = Order.objects.select_related('user').prefetch_related('items__book')

        for order in orders:
            for item in order.items.all():
                if y < 60:
                    p.showPage()
                    y = height - 50
                    p.setFont("Helvetica", 10)

                total_price = item.quantity * item.book.price
                line = (
                    f"#{order.id} | {order.user.username} | {item.book.title} x{item.quantity} | "
                    f"{order.status} | {'Paid' if order.is_paid else 'Not Paid'} | "
                    f"Total: {total_price} so'm"
                )
                p.drawString(50, y, line)
                y -= 20

        p.save()
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orders.pdf"'
        return response
