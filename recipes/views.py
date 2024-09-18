from django.http import Http404
from django.db.models import Q
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict

from recipes.models import Recipe
from utils.pagination import make_pagination

import os

PER_PAGE = int(os.environ.get('PER_PAGE', default=6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    ordering = ["-id"]
    template_name = "recipes/pages/home.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            is_published = True
        )

        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        page_object, pagination_range = make_pagination(self.request, context.get("recipes"), PER_PAGE)

        context.update({"recipes": page_object, "pagination_range": pagination_range})

        return context
    

class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = "recipes/pages/home.html"

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()["recipes"]
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            category__id=self.kwargs.get("category_id")
        )
        if not queryset:
            raise Http404()

        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            'title': f"{context.get('recipes')[0].category.name} - Category | "
        })

        return context


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )

        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        context.update({
            'page_title': f"Search for '{search_term}' | ",
            'search_term': search_term,
            'additional_url_query': f"&q={search_term}"
        })

        return context
    

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/pages/recipe-view.html"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        queryset = queryset.filter(is_published=True)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            "is_detail_page": True
        })

        return context
    

class RecipeDetailApi(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()["recipe"]
        recipe_dict = model_to_dict(recipe)

        recipe_dict["created_at"] = str(recipe.created_at)
        recipe_dict["updated_at"] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict["is_published"]
        del recipe_dict["preparation_steps_is_html"]

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
