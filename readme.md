# Setting up a GraphQL API based on django architecture

## Just a casual exploration of GraphQL use on a django based API
Testing django capabilities and DevX on creating a simple graphQL API with core features, then elaborate progressivly with advanced concepts and mechanics. Let's get going

## Copypastas startovers

### GraphQL

Graphical approach, allowing to explore data as a network full of data nodes and creativly fill your payload whith exactly what you need.
In opposition to classic Restful APIs where every single route has to be handmade, driving crazy poor little back-end devs.

### Graphene

Graphene is "just" a lib that brings all necessary tools to create a GraphQL API. 
In a similar way Rest Framework does for Restful APIs.
Advanced notion : the approach is code-first, in opposition to Apolo I used previously in a JavaScript environment. We do not define schemas first but a descriptive approach (yes, I have to dig deeper and maybe recall in a better way what I experienced with Apollo but eh... that was an eon ago).

A specific integration for Django is delivered with graphene_django

### Relay

Relay is an additionnal library that brings more built-in data-manipulating features (such as filters).

## Branches

- main : uses Relay advanced querying features to write more complex queries
- basic_implementation : simple boilerplate using graphene_django on its own

## Queries to test with main branch

```graphql
  query {
  allIngredients {
    edges {
      node {
        id,
        name
      }
    }
  }
}
```
```graphql
query {
  allCategories {
    edges {
      node {
        name,
        ingredients {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}
```
```graphql
query {
  allIngredients(name_Icontains: "e", category_Name: "Meat") {
    edges {
      node {
        name
      }
    }
  }
}
```

```graphql
mutation{
  createCategory(input:{name: "Cereals"}){
    category{
      id
      name
    }
  }
}
```

```graphql
mutation{
  updateCategory(input:{id: null, name:"Cereals", newName: "Vegetables"}){
    category{
      name
      id
    }
  }
}
```

```graphql
mutation{
  deleteCategory(input: {name: "Vegetables", id: null}){
    deleteConfirmation
  }
}
```

## Ressources

- [Graphene-django documentation](https://docs.graphene-python.org/en/latest/)
- [Relay Documentation](https://relay.dev/docs/)
- [First basic offical tutorial with graphene only](https://docs.graphene-python.org/en/latest/relay/)
- [Advanced tutorial, using graphene + relay](https://docs.graphene-python.org/projects/django/en/latest/tutorial-relay/)