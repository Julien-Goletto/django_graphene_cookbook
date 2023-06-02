from graphene import relay, ObjectType, String, Field
from graphql_relay import from_global_id
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
        name = String(required=True)
    
    def mutate_and_get_payload(root, info, **input):

        name = input["name"]

        existing_category = Category.objects.filter(name=name).first();
        if existing_category is not None:
            raise ValidationError('This category already exists.')

        category = Category(
            name = input["name"]
        )
        category.save()

        return CreateCategory(category=category)
    
class UpdateCategory(relay.ClientIDMutation):
    category = Field(CategoryNode)

    class Input:
        id = String()
        name = String()
        new_name = String(required=True)
    
    def mutate_and_get_payload(root, info, **input):

        id, name, new_name = input.values()

        if name is None and id is None:
            raise ValidationError('id or name has to be specified to target the category to mutate.')

        if id is None:
            category_to_update = Category.objects.filter(name=name).first()
        else :
            category_id = from_global_id(id).id
            category_to_update = Category.objects.filter(id=category_id).first()

        if category_to_update is None:
            raise ValidationError('The designated category does not exist.')

        category_to_update.name = new_name
        category_to_update.save()

        return UpdateCategory(category=category_to_update)
    
class DeleteCategory(relay.ClientIDMutation):
    delete_confirmation = String()

    class Input:
        id = String()
        name = String()
    
    def mutate_and_get_payload(root, info, **input):

        id, name = input.values()

        if name is None and id is None:
            raise ValidationError('id or name has to be specified to target the category to delete.')

        if id is None:
            category_to_delete = Category.objects.filter(name=name).first()
        else :
            category_to_delete = Category.objects.filter(id=id).first()

        if category_to_delete is None:
            raise ValidationError('The designated category does not exist.')

        category_to_delete.delete()
        delete_confirmation = "Targetted category has been deleted successfully"

        return DeleteCategory(delete_confirmation)

class Mutation(ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()