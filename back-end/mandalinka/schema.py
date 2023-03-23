import graphene

from management.schema import Query as ManagementQuery
from utils.schema import Query as UtilsQuery
from accounts.schema import Query as AccountsQuery


class Query(
    UtilsQuery,
    AccountsQuery,
    ManagementQuery,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)
