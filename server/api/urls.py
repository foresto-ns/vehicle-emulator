from django.urls import path

from api import viewsets
from api import views
from server.urls import router

router.register(r'vehicle', viewsets.VehicleViewSet)
router.register(r'command', viewsets.CommandViewSet)
router.register(r'trip', viewsets.TripViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('vehicle/<pk>', views.show_vehicle_info, name='vehicle_info'),
    path('create', views.create_vehicle, name='vehicle_create'),
    path('<pk>/set_options', views.set_options, name='set_options'),
    path('<pk>/set_rent', views.set_rent_status, name='set_rent'),
    path('<pk>/set_online', views.set_online, name='set_online'),
    path('<pk>/delete', views.VehicleDeleteView.as_view(), name='delete_vehicle'),


    path('api/options/<pk>', views.VehicleOptions.as_view()),
    path('api/trip/pause/<pk>', views.PauseTrip.as_view()),
    path('api/trip/continue/<pk>', views.ContinueTrip.as_view()),
    path('api/trip/finish/<pk>', views.FinishTrip.as_view()),
    path('api/vehicle/online/<pk>', views.SetOnlineStatus.as_view()),
    path('api/vehicle/rent/<pk>', views.SetRentStatus.as_view()),
]
