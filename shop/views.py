from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Category, Product,  Article
from shop.serializers import CategorySerializer, ProductSerializer, ArticleSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

# class CategoryView(APIView):

#     def get(self, *args, **kwargs):
#         queryset = Category.objects.all()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data)


# class ProductView(APIView):

#     def get(self, *args, **kwargs):
#         queryset = Product.objects.all()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)
    
class CategoryViewset(ReadOnlyModelViewSet):

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)
    

class ProductViewset(ModelViewSet):

    serializer_class = ProductSerializer

    def get_queryset(self):
        # Nous récupérons tous les produits dans une variable nommée queryset
            queryset = Product.objects.filter(active=True)
            # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
            category_id = self.request.GET.get('category_id')
            if category_id is not None:
                queryset = queryset.filter(category_id=category_id)
            return queryset
    

class ArticleViewset(ModelViewSet):
    
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = Article.objects.all()
        active_param = self.request.query_params.get('active')
        if active_param is not None:
            if active_param.lower() == 'true':
                queryset = queryset.filter(active=True)
            elif active_param.lower() == 'false':
                queryset = queryset.filter(active=False)
        return queryset