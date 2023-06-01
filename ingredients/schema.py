from graphene import relay, ObjectType, String, Field
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.core.exceptions import ValidationError

from ingredients.models import Category, Ingredient

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )


class Query(ObjectType):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)

class CreateCategory(relay.ClientIDMutation):
    category = Field(CategoryNode)

    class Input:
        name = String()
    
    def mutate_and_get_payload(root, info, **input):

        name = input["name"]
        if name is None:
            raise ValidationError('Name has to be defined.')

        existing_category = Category.objects.filter(name=name);
        if existing_category is not None:
            raise ValidationError('This category already exists.')

        category = Category(
            name = input["name"]
        )
        category.save()

        return CreateCategory(category=category)


class Mutation(ObjectType):
    create_category = CreateCategory.Field()