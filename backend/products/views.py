from re import A
from rest_framework import generics, mixins
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


class ProductListAPIView(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


product_list_view = ProductListAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookupfield = 'pk'

    def perform_update(self, serialiser):
        instance = serialiser.save()
        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookupfield = 'pk'

    def perform_delete(self, instance):
        super().perform_delete(instance)


product_delete_view = ProductDeleteAPIView.as_view()

# mixins and generics views


class ProductMixinView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, req, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(req, *args, **kwargs)
        return self.list(req, *args, **kwargs)

    def post(self, req, *args, **kwargs):
        return self.create(req, *args, **kwargs)

    # def perform_create(self, serializer):
    #     # serializer.save(user=self.request.user)
    #     title = serializer.validated_data.get('title')
    #     content = serializer.validated_data.get('content') or None
    #     if content is None:
    #         content = "Hola desde mi single view"
    #     serializer.save(content=content)


product_mixin_view = ProductMixinView.as_view()

# function based version


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
