from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, Vendor, PurchaseOrder , HistoricalPerformance

"""
This function defines a signal receiver that automatically creates a UserProfile object whenever a new User is created.
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# trigger historical performance metric updates in real-time in historical performance model when related PurchaseOrder data is modified
@receiver(post_save, sender=PurchaseOrder)
def update_historical_performance(sender, instance, created, **kwargs):
    if not created:
        # Update historical performance metrics
        vendor = instance.vendor
        historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=instance.issue_date)
        historical_performance.on_time_delivery_rate = vendor.on_time_delivery_rate
        historical_performance.quality_rating_avg = vendor.quality_rating_avg
        historical_performance.average_response_time = vendor.average_response_time
        historical_performance.fulfillment_rate = vendor.fulfillment_rate
        historical_performance.save()