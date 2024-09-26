from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer

from tag.models import Tag


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(instance=recipes, many=True, context={'request':request},)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data, context={'request':request},)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            # author_id=1,
            # category_id=1,
            # tags=[1, 2]
        )
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(
        #         data=serializer.validated_data, 
        #         status=status.HTTP_201_CREATED,
        #     )
        # return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['get', 'patch', 'delete'])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.get_published(),
        pk=pk
    )
    if request.method == 'GET':
        serializer = RecipeSerializer(instance=recipe, many=False, context={'request':request},)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = RecipeSerializer(
            instance=recipe, 
            data=request.data,
            many=False, 
            context={'request':request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
        )

    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()

    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         "Detail": "Not found"
    #     }, status=status.HTTP_404_NOT_FOUND)

@api_view(http_method_names=['get'])
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(instance=tag, many=False, context={'request':request},)
    return Response(serializer.data)
    