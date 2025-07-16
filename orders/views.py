import io

import xlsxwriter
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import OrderSerializer
from .models import Order
from rest_framework import viewsets


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], url_path='change-status', permission_classes=[IsAdminUser])
    def change_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response({'detail': 'Status is required'}, status=400)

        if not order.is_transition_allowed(new_status):
            return Response({'detail': f'Status "{new_status}" not allowed from current status "{order.status}"'},
                            status=400)

        order.set_status(new_status)
        return Response({'detail': f'Status changed to {new_status}'}, status=200)

    @action(detail=False, methods=['get'], url_path='export/excel', permission_classes=[IsAdminUser])
    def export_excel(self, request):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Orders')

        # Header
        headers = ['Order ID', 'Username', 'Phone', 'Book', 'Quantity', 'Status', 'Paid', 'Date']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Data rows
        orders = Order.objects.select_related('user').prefetch_related('items__book')

        row = 1
        for order in orders:
            for item in order.items.all():
                worksheet.write(row, 0, order.id)
                worksheet.write(row, 1, order.user.username)
                worksheet.write(row, 2, order.phone_number)
                worksheet.write(row, 3, item.book.title)
                worksheet.write(row, 4, item.quantity)
                worksheet.write(row, 5, order.status)
                worksheet.write(row, 6, 'Yes' if order.is_paid else 'No')
                worksheet.write(row, 7, order.created_at.strftime('%Y-%m-%d %H:%M'))
                row += 1

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=orders.xlsx'
        return response

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
                if y < 50:
                    p.showPage()
                    y = height - 50
                    p.setFont("Helvetica", 10)

                line = f"#{order.id} | {order.user.username} | {order.phone_number} | " \
                       f"{item.book.title} x{item.quantity} | {order.status} | {'Paid' if order.is_paid else 'Not Paid'}"
                p.drawString(50, y, line)
                y -= 20

        p.save()
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orders.pdf"'
        return response
