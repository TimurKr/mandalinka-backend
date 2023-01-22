from django.core.exceptions import ValidationError

def validate_positivity(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s is not positive'),
            params = {'value': value},
        )
