from rest_framework import mixins, viewsets

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product instance Details View
    port -> create -> New Instance
    put -> Update
    patch -> partial update
    delete-> destroy
    '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class ProductGenericViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
        get -> list -> Queryset
        get -> retrieve -> Product instance Details View

      '''
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

# product_list_view = ProductGenericViewSet.as_view({'get': 'list'})
# product_detail_view = ProductGenericViewSet.as_view({'get': 'retrieve'})
