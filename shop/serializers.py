from rest_framework.serializers import ModelSerializer
from shop.models import Category, Product, Article
from rest_framework import serializers
import requests




class ProductSerializer(serializers.ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'articles']

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data
    
    def call_external_api(self, method, url):
    # l'appel doit être le plus petit possible car appliquer un mock va réduire la couverture de tests
    # C'est cette méthode qui va être monkey patchée
        return requests.request(method, url)
 
    @property
    def ecoscore(self):
        # Nous réalisons l'appel à open food fact
        response = self.call_external_api('GET', 'https://world.openfoodfacts.org/api/v0/product/3229820787015.json')
        if response.status_code == 200:
        # et ne renvoyons l'écoscore que si la réponse est valide
            return response.json()['product']['ecoscore_grade']
        
        
class ProductListSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Product
        fields = ['id', 'date_created', 'date_updated', 'name', 'category', 'ecoscore']

class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name', 'description'] 

    def validate_name(self, value):
        # Nous vérifions que la catégorie existe
        if Category.objects.filter(name=value).exists():
        # En cas d'erreur, DRF nous met à disposition l'exception ValidationError
            raise serializers.ValidationError('Category already exists')
        return value
    
    def validate(self, data):
        # Effectuons le contrôle sur la présence du nom dans la description
        if data['name'] not in data['description']:
        # Levons une ValidationError si ça n'est pas le cas
            raise serializers.ValidationError('Name must be in description')
        return data

class CategoryDetailSerializer(serializers.ModelSerializer):

    products = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'date_created', 'date_updated', 'name','products']

    def get_products(self, instance):
        # Le paramètre 'instance' est l'instance de la catégorie consultée.
        # Dans le cas d'une liste, cette méthode est appelée autant de fois qu'il y a
        # d'entités dans la liste

        # On applique le filtre sur notre queryset pour n'avoir que les produits actifs
        queryset = instance.products.filter(active=True)
        # Le serializer est créé avec le queryset défini et toujours défini en tant que many=True
        serializer = ProductSerializer(queryset, many=True)
        # la propriété '.data' est le rendu de notre serializer que nous retournons ici
        return serializer.data

class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'id',
            'date_created',
            'date_updated',
            'name',
            'price',
            'product'
        ]

    
    def validate(self, data):

        if data['price'] < 1:
            raise serializers.ValidationError('Price must be greater than 1€')
        # Vérification de l'état actif du produit associé
        product = data.get('product')
        if product and not product.active:
            raise serializers.ValidationError('The associated product must be active')
        return data
        

