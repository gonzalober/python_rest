from email import header
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer
# auth


@api_view(['POST'])
def api_home(req, *args, **kwargs):
    """
    drf api view
    """
    serializer = ProductSerializer(data=req.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        print(instance)
        return Response(serializer.instance)
    return Response({"invalid": "not good data"}, status=400)

    # instance = Product.objects.all().order_by("?").first()
    # data = {}
    # if instance:
    #     # data = model_to_dict(model_data, fields=[
    #     #                      'id', 'title', 'content', 'price', 'sale_price'])
    #     data = ProductSerializer(instance).data
    # data['id'] = model_data.id
    # data['title'] = model_data.title
    # data['content'] = model_data.content
    # data['price'] = model_data.price
    # model instance (model_data)
    # turn into Pyhton dict
    #     data = model_to_dict(model_data, fields=['id', 'title', 'content'])
    #     # json serialisation
    #     json_data_str = json.dumps(data)
    # return (HttpResponse(json_data_str, headers={"content-type": "application/json"}))
