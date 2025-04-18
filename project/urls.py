from django.contrib import admin
from django.urls import path, include
#from shop.views import CategoryView
# from shop.views import ProductView
from rest_framework import routers

from shop.views import CategoryViewset
from shop.views import ProductViewset
from shop.views import ArticleViewset
from shop.views import AdminCategoryViewset
from shop.views import AdminArticleViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.SimpleRouter()
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('article', ArticleViewset, basename='article')
router.register('admin/category', AdminCategoryViewset, basename='admin-category')
router.register('admin/article', AdminArticleViewset, basename='admin-article')
 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    #path('api/category/', CategoryView.as_view()),
    #path('api/product/', ProductView.as_view()),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
