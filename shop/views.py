from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Category, Product,  Article
from shop.serializers import CategoryListSerializer, CategoryDetailSerializer
from shop.serializers import ProductSerializer, ArticleSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.db import transaction
from rest_framework.decorators import action

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

class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
 
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer
 
    def get_queryset(self):
        return Category.objects.all()
    
class CategoryViewset(ReadOnlyModelViewSet):

    serializer_class = CategoryListSerializer
    serializer_detail_class = CategoryDetailSerializer

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous avons défini notre action accessible sur la méthode POST seulement
        # elle concerne le détail car permet de désactiver une catégorie

        # Nous avons également mis en place une transaction atomique car plusieurs requêtes vont être exécutées
        # en cas d'erreur, nous retrouverions alors l'état précédent

        # Désactivons la catégorie
        category = self.get_object()
        category.active = False
        category.save()

        # Puis désactivons les produits de cette catégorie
        category.products.update(active=False)

        # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
        return Response()
    
    @transaction.atomic
    @action(detail=True, methods=['post'])
    def able(self, request, pk):
        category = self.get_object()
        category.active = True
        category.save()
        category.products.update(active=True)
        # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
        return Response()

    def get_queryset(self):
        if self.action in ['disable', 'able']:
            return Category.objects.all()
        return Category.objects.filter(active=True)
    
    def get_serializer_class(self):
    # Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == 'retrieve':
            return self.serializer_detail_class
        return super().get_serializer_class()

class ProductViewset(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer

    @transaction.atomic
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Nous avons défini notre action accessible sur la méthode POST seulement
        # elle concerne le détail car permet de désactiver une catégorie

        # Nous avons également mis en place une transaction atomique car plusieurs requêtes vont être exécutées
        # en cas d'erreur, nous retrouverions alors l'état précédent

        # Désactivons la catégorie
        product = self.get_object()
        product.active = False
        product.save()

        # Puis désactivons les produits de cette catégorie
        product.articles.update(active=False)

        # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
        return Response()
    
    @transaction.atomic
    @action(detail=True, methods=['post'])
    def able(self, request, pk):
        product = self.get_object()
        product.active = True
        product.save()
        product.articles.update(active=True)
        # Retournons enfin une réponse (status_code=200 par défaut) pour indiquer le succès de l'action
        return Response()

    def get_queryset(self):
        # Nous récupérons tous les produits dans une variable nommée queryset
            queryset = Product.objects.filter(active=True)
            # Vérifions la présence du paramètre ‘category_id’ dans l’url et si oui alors appliquons notre filtre
            
            category_id = self.request.GET.get('category_id')
            
            if category_id is not None:
                queryset = queryset.filter(category_id=category_id)
            if self.action in ['disable', 'able']:
                return Product.objects.all()
            return queryset
    


class AdminArticleViewset(ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()

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