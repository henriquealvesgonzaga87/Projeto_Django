from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from ..permissions import IsOwner

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer

from tag.models import Tag


class RecipeApiV2Pagination(PageNumberPagination):
    page_size = 5


class RecipeApiV2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeApiV2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly,]
    http_method_names = ["get", "options", "head", "patch", "post", "delete"]

    def get_serializer_class(self):
        return super().get_serializer_class()
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        query_set = super().get_queryset()
        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            query_set = query_set.filter(category_id=category_id)

        return query_set
    
    def get_object(self):
        pk = self.kwargs.get('pk', '')
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        self.check_object_permissions(request=self.request, obj=obj)

        return obj
    
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsOwner(),]
        
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def partial_update(self, request, *args, **kwargs):
        recipe = self.get_object()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={"request": request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,)
    

@api_view(http_method_names=['get'])
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(instance=tag, many=False, context={'request':request},)
    return Response(serializer.data)


# class RecipeAPIV2List(ListCreateAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeApiV2Pagination


# class RecipeAPIV2Detail(RetrieveUpdateDestroyAPIView):
#     queryset = Recipe.objects.get_published()
#     serializer_class = RecipeSerializer
#     pagination_class = RecipeApiV2Pagination


# class RecipeAPIV2List(APIView):
#     def get(self, request):
#         recipes = Recipe.objects.get_published()[:10]
#         serializer = RecipeSerializer(instance=recipes, many=True, context={'request':request},)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = RecipeSerializer(data=request.data, context={'request':request},)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    

# class RecipeAPIV2Detail(APIView):
#     def get_recipe(self, pk):
#         recipe = get_object_or_404(
#         Recipe.objects.get_published(),
#         pk=pk
#     )
#         return recipe

#     def get(self, request, pk):
#         recipe = self.get_recipe(pk=pk)
#         serializer = RecipeSerializer(instance=recipe, many=False, context={'request':request},)
#         return Response(serializer.data)
    
#     def patch(self, request, pk):
#         recipe = self.get_recipe(pk=pk)
#         serializer = RecipeSerializer(
#             instance=recipe, 
#             data=request.data,
#             many=False, 
#             context={'request':request},
#             partial=True,
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             serializer.data,
#         )
    
#     def delete(self, request, pk):
#         recipe = self.get_recipe(pk=pk)
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# @api_view(http_method_names=['get', 'post'])
# def recipe_api_list(request):
#     if request.method == 'GET':
#         recipes = Recipe.objects.get_published()[:10]
#         serializer = RecipeSerializer(instance=recipes, many=True, context={'request':request},)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = RecipeSerializer(data=request.data, context={'request':request},)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(
            # author_id=1,
            # category_id=1,
            # tags=[1, 2]
        # )
        # return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(
        #         data=serializer.validated_data, 
        #         status=status.HTTP_201_CREATED,
        #     )
        # return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(http_method_names=['get', 'patch', 'delete'])
# def recipe_api_detail(request, pk):
#     recipe = get_object_or_404(
#         Recipe.objects.get_published(),
#         pk=pk
#     )
#     if request.method == 'GET':
#         serializer = RecipeSerializer(instance=recipe, many=False, context={'request':request},)
#         return Response(serializer.data)
    
#     elif request.method == 'PATCH':
#         serializer = RecipeSerializer(
#             instance=recipe, 
#             data=request.data,
#             many=False, 
#             context={'request':request},
#             partial=True,
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(
#             serializer.data,
#         )

#     elif request.method == 'DELETE':
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()

    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         "Detail": "Not found"
    #     }, status=status.HTTP_404_NOT_FOUND)
    