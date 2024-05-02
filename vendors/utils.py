from django.db.models import Avg ,ExpressionWrapper, F, DurationField
from django.utils import timezone

def update_performance_metrics(vendor):
    total_orders = vendor.purchaseorder_set.count()
    on_time_orders = vendor.purchaseorder_set.filter(status='completed', delivery_date__lte=timezone.now()).count()
    on_time_delivery_rate = (on_time_orders / total_orders) * 100 if total_orders > 0 else 0

    quality_rating_avg = vendor.purchaseorder_set.aggregate(avg_quality=Avg('quality_rating'))['avg_quality'] or 0

    response_times = vendor.purchaseorder_set.exclude(acknowledgment_date__isnull=True).annotate(
        response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
    ).aggregate(avg_response=Avg('response_time'))['avg_response']
    average_response_time = response_times.total_seconds() / total_orders if response_times else 0

    fulfilled_orders = vendor.purchaseorder_set.filter(status='completed').count()
    fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0

    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = average_response_time
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
