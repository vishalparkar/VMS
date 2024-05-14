from django.db import models
from django.db.models import Avg, Count, F, ExpressionWrapper, fields
from django.utils import timezone
from django.utils.timezone import now

class Vendor(models.Model):
    """
    This model captures the details of each purchase order and is used to calculate various performance metrics.
    """
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)

    # Performance metrics (fields will be updated dynamically)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    def update_performance_metrics(self):
        completed_orders = self.purchase_orders.filter(status='completed')
        self.on_time_delivery_rate = completed_orders.filter(delivery_date__lte=F('order_date')).count() / completed_orders.count() * 100
        self.quality_rating_avg = completed_orders.aggregate(average=Avg('quality_rating'))['average']
        response_times = completed_orders.annotate(response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=fields.DurationField())).aggregate(average=Avg('response_time'))
        self.average_response_time = response_times['average'].total_seconds() / 3600  # Convert to hours
        self.fulfillment_rate = completed_orders.filter(quality_rating__gte=3).count() / completed_orders.count() * 100
        self.save()

class PurchaseOrder(models.Model):
    """
    This model captures the details of each purchase order and is used to calculate various performance metrics.
    """
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_choices=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)  # Optional rating for completed orders
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'completed':
            self.vendor.update_performance_metrics()

class HistoricalPerformance(models.Model):
    """
    This model optionally stores historical data on vendor performance, enabling trend analysis.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} Performance ({self.date})"