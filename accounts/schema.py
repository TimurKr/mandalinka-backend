import graphene

from graphene_django.types import DjangoObjectType

from .models import User, Address


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'pronoun',
            'email',
            'phone',
            'newsletter',
            'terms_conditions',

            'is_active',

            'addresses',
        )


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        fields = (
            'id',
            'user',
            'primary',
            'name',
            'address',
            'note',
            'city',
            'district',
            'postal',
            'country',
            'coordinates',
        )


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.Int())

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user_by_id(self, info, id):
        return User.objects.get(id=id)

    addresses = graphene.List(AddressType)
    address_by_id = graphene.Field(AddressType, id=graphene.Int())

    def resolve_addresses(self, info, **kwargs):
        return Address.objects.all()

    def resolve_address_by_id(self, info, id):
        return Address.objects.get(id=id)
