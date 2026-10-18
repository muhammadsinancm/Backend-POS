from rest_framework.response import Response
from rest_framework.views import APIView
from apps.common.permission import IsOwnerOrReadOnly

class MenuPermissionTestView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    
    def get(self, reqeust):
        return Response({
            "message": "You can view the menu."
        })
    
    def post(self, request):
        return Response({
            "message": "You can modify menu data."
        })