from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import BusinessAccount

class FindBusinessAccounts(APIView):
    def get(self, request):
        try:
            # Get parameters from the request
            latitude = float(request.GET.get('latitude'))
            longitude = float(request.GET.get('longitude'))
            max_range = float(request.GET.get('max_range'))
            cuisine_name = request.GET.get('cuisine_name')

            # Create a Point object for the current location
            current_location = Point(longitude, latitude, srid=4326)

            # Define a bounding box for the search area
            search_area = current_location.buffer(D(km=max_range))

            # Perform the query to find business accounts within the specified range and with the given cuisine
            business_accounts = BusinessAccount.objects.filter(
                Q(location__within=search_area),
                Q(cuisines__name=cuisine_name)
            )

            # Serialize the results
            data = [{
                'business_name': business.business_name,
                'street_name': business.street_name,
                'locality': business.locality,
                # Include other fields you want to return
            } for business in business_accounts]

            return JsonResponse({'business_accounts': data})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
