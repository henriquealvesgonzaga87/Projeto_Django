from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from recipes import views


app_name = "recipes"

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(prefix='recipes/api/v2', viewset=views.RecipeApiV2ViewSet, basename="recipes-api")

urlpatterns = [
    path("", views.RecipeListViewHome.as_view(), name="home"),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/tags/<slug:slug>', views.RecipeListViewTag.as_view(), name='tag'),
    path("recipes/category/<int:category_id>/", views.RecipeListViewCategory.as_view(), name="category"),
    path("recipes/<int:pk>/", views.RecipeDetail.as_view(), name="recipe"),
    path("recipes/api/v1", views.RecipeListViewHomeApi.as_view(), name="recipe_api_v1"),
    path("recipes/api/v1/<int:pk>", views.RecipeDetailApi.as_view(), name="recipe_api_v1_detail"),
    path("recipes/theory/", views.theory, name="theory"),
    # path("recipes/api/v2/", views.RecipeApiV2ViewSet.as_view({
    #     "get": "list",
    #     "post": "create",
    # }), name="recipe_api_v2"),
    # path("recipes/api/v2/<int:pk>", views.RecipeApiV2ViewSet.as_view({
    #     "get": "retrieve",
    #     "patch": "partial_update",
    #     "delete": "destroy",
    # }), name="recipe_api_v2_detail"),
    
    # api URLS
    path("recipes/api/v2/tag/<int:pk>", views.tag_api_detail, name="recipes_api_v2_tag"),
    path('recipes/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('recipes/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('recipes/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(recipe_api_v2_router.urls))
]

# urlpatterns += recipe_api_v2_router.urls
