from .models import CustomUser
import django_filters


class UserFilter(django_filters.FilterSet):
    home = django_filters.CharFilter(field_name="home__name")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = CustomUser
        fields = ["home", "status"]
