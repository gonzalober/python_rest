from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)
        # return super().perform_create(serializer)


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # lookupfield='pk'
product_detail_view = ProductDetailAPIView.as_view()


@api_view(['GET', 'POST'])
def product_alt_view(req, pk=None, *args, **kwargs):
    method = req.method
    if method == "GET":
        if pk is not None:
            # get req->detail view
            # queryset = Product.objects.filter(pk=pk)
            # if not queryset.exist():
            # raise Http404 OR this:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    if method == "POST":
        # get req->detail view
        serializer = ProductSerializer(data=req.data)
        if serializer.is_valid(raise_exception=True):
            # title = serializer.validated_data.get('title')
            # content = serializer.validated_data.get('content') or None
            # if content is None:
            #     content = title
            # serializer.save(content=content)
            print(serializer.data)
            return Response(serializer.instance)
        return Response({"invalid": "not good data"}, status=400)
