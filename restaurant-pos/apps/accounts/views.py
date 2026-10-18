from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import POSLoginSerializer, UsezrSerializer

class POSLoginView(TokenObtainPairView):
    serializer_class = POSLoginSerializer
    
class CurrentUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsezrSerializer
    
    def get_object(self):
        return self.request.user