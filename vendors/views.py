import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder
from django.db.models import Avg, ExpressionWrapper, F, DurationField
from django.utils import timezone
from .utils import update_performance_metrics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator


    
# Api To Create Vendor
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_vendor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vendor = Vendor.objects.create(
                name=data.get('name'),
                contact_details=data.get('contact_details'),
                address=data.get('address'),
                vendor_code=data.get('vendor_code')
            )
            return JsonResponse({'message': 'Vendor created successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# Api To Fetch all Vendor
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_vendors(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        paginator = Paginator(vendors, 10)  
        page_number = request.GET.get('page')
        vendors_page = paginator.get_page(page_number)
        vendor_data = [{'name': vendor.name, 'contact_details': vendor.contact_details, 'address': vendor.address,
                        'vendor_code': vendor.vendor_code} for vendor in vendors_page]        
        return JsonResponse({'vendors': vendor_data, 'total_pages': paginator.num_pages})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# Api To Fetch Single Vendor
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
        return JsonResponse({'name': vendor.name, 'contact_details': vendor.contact_details, 'address': vendor.address,
                             'vendor_code': vendor.vendor_code})
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)


# Api To Update Single Vendor
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            vendor.name = data.get('name', vendor.name)
            vendor.contact_details = data.get('contact_details', vendor.contact_details)
            vendor.address = data.get('address', vendor.address)
            vendor.vendor_code = data.get('vendor_code', vendor.vendor_code)
            vendor.save()
            return JsonResponse({'message': 'Vendor updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# Api To Delete Single Vendor
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor.delete()
        return JsonResponse({'message': 'Vendor deleted successfully'}, status=200)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Api To Create Purchase Order
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_purchase_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vendor_id = data.get('vendor_id')
            if not Vendor.objects.filter(pk=vendor_id).exists():
                return JsonResponse({'error': 'Vendor not found'}, status=404)

            purchase_order = PurchaseOrder.objects.create(
                vendor_id=vendor_id,
                po_number=data.get('po_number'),
                order_date=data.get('order_date'),
                delivery_date=data.get('delivery_date'),
                items=data.get('items'),
                quantity=data.get('quantity'),
                status=data.get('status'),
                quality_rating=data.get('quality_rating'),
                issue_date=data.get('issue_date'),
                acknowledgment_date=data.get('acknowledgment_date')
            )

            return JsonResponse({'message': 'Purchase Order created successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


# Api To Fetch All The Purchase Orders
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_purchase_orders(request):
    if request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        paginator = Paginator(purchase_orders, 10)  # Adjust the page size as needed
        page_number = request.GET.get('page')
        purchase_orders_page = paginator.get_page(page_number)
        
        po_data = [{'po_number': po.po_number, 'vendor_id': po.vendor_id, 'order_date': po.order_date,
                    'delivery_date': po.delivery_date, 'items': po.items, 'quantity': po.quantity,
                    'status': po.status, 'quality_rating': po.quality_rating, 'issue_date': po.issue_date,
                    'acknowledgment_date': po.acknowledgment_date} for po in purchase_orders_page]
        return JsonResponse({'purchase_orders': po_data, 'total_pages': paginator.num_pages})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    

# Api To Fetch Single Purchase Order
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        return JsonResponse({
            'po_number': purchase_order.po_number,
            'vendor_id': purchase_order.vendor_id,
            'order_date': purchase_order.order_date,
            'delivery_date': purchase_order.delivery_date,
            'items': purchase_order.items,
            'quantity': purchase_order.quantity,
            'status': purchase_order.status,
            'quality_rating': purchase_order.quality_rating,
            'issue_date': purchase_order.issue_date,
            'acknowledgment_date': purchase_order.acknowledgment_date
        })
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'Purchase Order not found'}, status=404)


# Api To Update Purchase Order
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'Purchase Order not found'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(purchase_order, key, value)
            purchase_order.save()

            return JsonResponse({'message': 'Purchase Order updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# Signal handler for purchase order updates
@receiver([post_save, post_delete], sender=PurchaseOrder)
def handle_purchase_order_change(sender, instance, **kwargs):
    update_performance_metrics(instance.vendor)


# Api To Delete Purchase Order
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        purchase_order.delete()
        return JsonResponse({'message': 'PO deleted successfully'}, status=200)
    except PurchaseOrder.DoesNotExist:
        return JsonResponse({'error': 'PO not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Api To Fetch Vendor Performance Metrics
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
        total_orders = vendor.purchaseorder_set.count()
        on_time_orders = vendor.purchaseorder_set.filter(status='completed',
                                                         delivery_date__lte=timezone.now()).count()
        on_time_delivery_rate = (on_time_orders / total_orders) * 100 if total_orders > 0 else 0

        quality_rating_avg = vendor.purchaseorder_set.aggregate(avg_quality=Avg('quality_rating'))[
            'avg_quality'] or 0

        response_times = vendor.purchaseorder_set.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
        ).aggregate(avg_response=Avg('response_time'))['avg_response']
        average_response_time = response_times.total_seconds() / total_orders if response_times else 0

        fulfilled_orders = vendor.purchaseorder_set.filter(status='completed').count()
        fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0

        performance_data = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate,
        }
        return JsonResponse(performance_data)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def acknowledge_purchase_order(request, po_id):
    print("Inside acknowledge_purchase_order view function")
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        print("Purchase Order not found")
        return JsonResponse({'error': 'Purchase Order not found'}, status=404)

    if request.method == 'POST':
        print("Request method is POST")
        try:
            data = json.loads(request.body)
            print("Request body:", data)
            acknowledgment_date = data.get('acknowledgment_date', timezone.now())
            print("Acknowledgment date:", acknowledgment_date)
            purchase_order.acknowledgment_date = acknowledgment_date
            purchase_order.save()

            update_performance_metrics(purchase_order.vendor)

            print("Purchase Order acknowledged successfully")
            return JsonResponse({'message': 'Purchase Order acknowledged successfully'})
        except json.JSONDecodeError:
            print("Invalid JSON data")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        print("Method not allowed")
        return JsonResponse({'error': 'Method not allowed'}, status=405)
