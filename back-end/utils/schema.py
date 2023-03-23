import graphene

from graphene_django.types import DjangoObjectType

from .models import Unit


class TimeStampTypeMixin:
    created = graphene.DateTime()
    modified = graphene.DateTime()

    def resolve_created_at(self, info, **kwargs):
        return self.created

    def resolve_updated_at(self, info, **kwargs):
        return self.modified


class StatusTypeMixin:
    status = graphene.String()
    is_active = graphene.Boolean()
    is_inactive = graphene.Boolean()
    is_deleted = graphene.Boolean()

    def resolve_status(self, info, **kwargs):
        return self.status

    def resolve_is_active(self, info, **kwargs):
        return self.is_active

    def resolve_is_inactive(self, info, **kwargs):
        return self.is_inactive

    def resolve_is_deleted(self, info, **kwargs):
        return self.is_deleted


class UnitType(DjangoObjectType):
    class Meta:
        model = Unit
        fields = (
            'id',
            'name',
            'sign',
            'base_unit',
            'conversion_rate',
            'system',
            'property',
        )


class Query(graphene.ObjectType):
    units = graphene.List(UnitType)
    unit_by_id = graphene.Field(UnitType, id=graphene.Int())

    def resolve_units(self, info, **kwargs):
        return Unit.objects.all()

    def resolve_unit_by_id(self, info, id):
        return Unit.objects.get(id=id)
