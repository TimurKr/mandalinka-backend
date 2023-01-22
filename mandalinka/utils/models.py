from django.db import models
from django.utils import timezone

# Create your models here.

class TimeStampedMixin(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Vytvorené"
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Upravené"
    )

    class Meta:
        abstract = True


class StatusMixin(models.Model):
    """
    An abstract base class model that provides a ``status`` field.
    TimeStamps the time of last status change. 
    By default it has 3 options: 'active', 'inactive' and 'deleted'.
    The 'deleted' option is used for soft-deletion.
    The 'inactive' option is the default.
    Also provides methods to check and change the status.
    """

    status_id = models.AutoField(primary_key=True)

    class Statuses:
        """Internal for a status representation"""
        ACTIVE = 'active'
        INACTIVE = 'inactive'
        DELETED = 'deleted'
        options = (
            (ACTIVE, ACTIVE),
            (INACTIVE, INACTIVE),
            (DELETED, DELETED)
        )

    _status = models.CharField(
        max_length=8,
        choices=Statuses.options, default=Statuses.INACTIVE,
        editable=False
    )

    status_changed = models.DateTimeField(
        verbose_name="Zmena statusu", editable=False
    )

    class Meta:
        abstract = True

    @property
    def status(self) -> str:
        return self._status

    @property
    def active(self) -> bool:
        """Returns True if the status is 'active'"""
        return self.status == self.Statuses.ACTIVE

    @property
    def inactive(self) -> bool:
        """Returns True if the status is 'inactive'"""
        return self.status == self.Statuses.INACTIVE
    
    @property
    def deleted(self) -> bool:
        """Returns True if the status is 'deleted'"""
        return self.status == self.Statuses.DELETED
    
    def activate(self) -> None:
        """
        Sets the status to 'active'
        Overwrite this method and call it at the end for custom activation logic.
        """
        if self.active:
            return
        self.status_changed = timezone.now()
        self.status = self.Statuses.ACTIVE
        self.save()
    
    def deactivate(self) -> None:
        """
        Sets the status to 'inactive'
        Overwrite this method and call it at the end for custom deactivation logic.
        """
        if self.inactive:
            return
        self.status_changed = timezone.now()
        self.status = self.Statuses.INACTIVE
        self.save()
    
    def soft_delete(self) -> None:
        """
        Sets the status to 'deleted'
        Overwrite this method and call it at the end for custom soft-deletion logic.
        """
        if self.deleted:
            return
        self.status_changed = timezone.now()
        self.status = self.Statuses.DELETED
        self.save()
        


class Unit(models.Model):
    """
    Model for representing units of measurement.
    Includes methods to convert to and from base unit.
    """
    name = models.CharField(
        unique=True,
        max_length=64,
    )

    sign = models.CharField(
        unique=True,
        max_length=6,
    )

    base_unit = models.ForeignKey('self',
        blank=True, null=True,
        on_delete=models.RESTRICT,
        related_name='sub_units'
    )

    conversion_rate = models.DecimalField(
        max_digits=13, decimal_places=6,
        verbose_name="Konštanta na premenu na base_unit"
    )


    class Systems:
        """Internal for a system representation"""
        METRIC = 'METRIC'
        IMPERIAL = 'IMPERIAL'
        options = (
            (METRIC, METRIC),
            (IMPERIAL, IMPERIAL)
        )

    system = models.CharField(
        max_length=8,
        choices=Systems.options, default=Systems.METRIC
    )


    class Proprties:
        """Internal for a property representation"""
        LENGTH = 'LENGTH'
        MASS = 'MASS'
        VOLUME = 'VOLUME'
        options = (
            (LENGTH, LENGTH),
            (MASS, MASS),
            (VOLUME, VOLUME)
        )
    
    property = models.CharField(
        max_length=8,
        choices=Proprties.options, default=Proprties.MASS
    )


    def __str__(self) -> str:
        """Returns the sign of the unit"""
        return self.sign


    def in_base(self, amount: float, as_string: bool = False):
        """Converts given amount to base unit
        
        :param amount: Amount to convert
        :type amount: float
        :param as_string: If True, returns the value as a string, else returns the value as a float
        :type as_string: bool
        :return: Converted value
        :rtype: float or str
        """
        value = amount * float(self.conversion_rate)
        if as_string:
            return f'{value} {self.base}'
        else:
            return value


    def from_base(self, amount: float, as_string: bool = False):
        """Converts given amount from base unit to this unit
        
        :param amount: Amount to convert
        :type amount: float
        :param as_string: If True, returns the value as a string, else returns the value as a float
        :type as_string: bool
        :return: Converted value
        :rtype: float or str
        """
        value = amount / float(self.conversion_rate)
        if as_string:
            return f'{value} {self.base}'
        else:
            return value

