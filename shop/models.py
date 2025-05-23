from django.db import models, transaction


class Category(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    @transaction.atomic
    def disable(self):
        if self.active is False:
        # Ne faisons rien si la catégorie est déjà désactivée
            return
        self.active = False
        self.save()
        self.products.update(active=False)

    @transaction.atomic
    def able(self):
        if self.active is True:
        # Ne faisons rien si la catégorie est déjà désactivée
            return
        self.active = True
        self.save()
        self.products.update(active=False)

    def __str__(self):
        return self.name


class Product(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)

    category = models.ForeignKey('shop.Category', on_delete=models.CASCADE, related_name='products')

    @transaction.atomic
    def disable(self):
        if self.active is False:
        # Ne faisons rien si la catégorie est déjà désactivée
            return
        self.active = False
        self.save()
        self.articles.update(active=False)

    @transaction.atomic
    def able(self):
        if self.active is True:
        # Ne faisons rien si la catégorie est déjà désactivée
            return
        self.active = True
        self.save()
        self.articles.update(active=False)

    def __str__(self):
        return self.name


class Article(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.name
