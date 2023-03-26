import graphene

from management.graphql.schema import (
    Query as ManagementQuery,
    Mutation as ManagementMutation
)
from utils.schema import Query as UtilsQuery
from accounts.schema import Query as AccountsQuery


class Query(
    UtilsQuery,
    AccountsQuery,
    ManagementQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    ManagementMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
