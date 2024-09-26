from collections import defaultdict
from rest_framework import serializers
from django.contrib.auth.models import User
from tag.models import Tag
from . models import Recipe
from authors.validators import AuthorRecipeValidator


# class TagSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField(max_length=255)
#     slug = serializers.SlugField()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

# class RecipeSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     description = serializers.CharField(max_length=165)
#     public = serializers.BooleanField(source="is_published", read_only=True)
#     preparation = serializers.SerializerMethodField(method_name='any_method_name', ready_only=True)
#     # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     category = serializers.StringRelatedField()
#     author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
#     tag_objects = TagSerializer(many=True, source='tags')
#     tag_links = serializers.HyperlinkedRelatedField(
#         many=True, 
#         source='tags', 
#         queryset=Tag.objects.all(),
#         view_name="recipes:recipe_api_v2_tag"
#     )

#     def any_method_name(self, recipe):
#         return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover'
        ]

    public = serializers.BooleanField(
        source='is_published',
        read_only=True,
    )
    preparation = serializers.SerializerMethodField(
        method_name='any_method_name',
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True, source='tags',
        read_only=True,
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipes_api_v2_tag',
        read_only=True,
    )

    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
    
    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs["servings"] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs["preparation_time"] = self.instance.preparation_time

        super_validate =  super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs, 
            ErrorClass=serializers.ValidationError
        )

        return super_validate
        
        # title = attrs.get('title')
        # description = attrs.get('description')

        # if description == title:
        #     raise serializers.ValidationError({
        #         "title": ["The title can't be equal to the description"],
        #         "description": ["The description can't be equal to the title"]
        #     })

        
        # super_validate =  super().validate(attrs)

        # cleaned_data = attrs
        # _my_errors = defaultdict(list)
        
        # title = cleaned_data.get('title')
        # description = cleaned_data.get('description')

        # if description == title:
        #     _my_errors['description'].append("The description can't be equal to the title")
        #     _my_errors['title'].append("The title can't be equal to the description")

        # if _my_errors:
        #     raise serializers.ValidationError(_my_errors)

        # return super_validate
    
    # def validate_title(self, value):
    #     title = value

    #     if len(title) < 5:
    #         raise serializers.ValidationError("Must have at least 5 chars")
        
    #     return title

    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
