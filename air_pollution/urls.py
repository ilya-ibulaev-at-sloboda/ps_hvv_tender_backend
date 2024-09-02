from django.urls import path

from air_pollution.api import PollutionStatsView

app_name = "air_pollution"

urlpatterns = [
    path(
        "entity/<str:entity>/",
        PollutionStatsView.as_view(),
        name="stats-by-entity",
    ),
]
