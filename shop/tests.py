from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from shop.models import Category,   Product
from rest_framework import status



class ShopAPITestCase(APITestCase):
    """
    Classe de test pour l'API de la boutique.
    """

    def setUp(self):
        """
        Configuration initiale des tests.
        """
        # Créez ici les objets nécessaires pour vos tests
        self.category = Category.objects.create(name='Test Category')

class TestProduct(ShopAPITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('product-list')
    def setUp(self):
        super().setUp()
        self.category1 = Category.objects.create(name="Catégorie 1")
        self.category2 = Category.objects.create(name="Catégorie 2")
        self.product1 = Product.objects.create(
            name="Produit A", description="desc A", active=True, category=self.category1
        )
        self.product2 = Product.objects.create(
            name="Produit B", description="desc B", active=True, category=self.category2
        )
        self.inactive_product = Product.objects.create(
            name="Inactif", description="...", active=False, category=self.category1
        )

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        product_names = [prod["name"] for prod in response.json()]
        assert "Produit A" in product_names
        assert "Produit B" in product_names
        assert "Inactif" not in product_names  # ⚠️ car il est `active=False`

    def test_filter_products_by_category(self):
        response = self.client.get(self.url, {"category_id": self.category1.id})
        self.assertEqual(response.status_code, 200)
        results = response.json()
        assert len(results) == 1
        assert results[0]["name"] == "Produit A"

    def test_product_detail(self):
        url_detail = reverse_lazy('product-detail', args=[self.product1.pk])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)
        assert response.json()["name"] == "Produit A"







class TestCategory(ShopAPITestCase):
    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    url = reverse_lazy('category-list')

    def format_datetime(self, value):
        # Cette méthode est un helper permettant de formater une date en chaine de caractères sous le même format que celui de l’api
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    

    def setUp(self):
        super().setUp()
        Category.objects.all().delete()

    def test_list(self):
        # Créons deux catégories dont une seule est active
        category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        # On réalise l’appel en GET en utilisant le client de la classe de test
        response = self.client.get(self.url)
        # Nous vérifions que le status code est bien 200
        # et que les valeurs retournées sont bien celles attendues
        self.assertEqual(response.status_code, 200)
        excepted = [
            {
                'id': category.pk,
                'name': category.name,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            }
        ]
        self.assertEqual(excepted, response.json())

    def test_create(self):
        # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
        self.assertFalse(Category.objects.exists())
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
        self.assertEqual(response.status_code, 405)
        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
        self.assertFalse(Category.objects.exists())


    

