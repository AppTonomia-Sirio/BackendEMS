from .models import CustomUser
import django_filters


class UserFilter(django_filters.FilterSet):
    home = django_filters.CharFilter(field_name="home__name")
    active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = CustomUser
        fields = ["home", "active"]
