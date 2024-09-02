from django.db import models
from django.db.models import Avg, StdDev
from tailslide import Median


class PollutionQuerySet(models.QuerySet):
    def with_statistics(self):
        return self.values("entity").annotate(
            nitrogen_oxide_avg=Avg("nitrogen_oxide"),
            # nitrogen_oxide_median=Median("nitrogen_oxide"),
            nitrogen_oxide_std_dev=StdDev("nitrogen_oxide"),
            sulphur_dioxide_avg=Avg("sulphur_dioxide"),
            # sulphur_dioxide_median=Median("sulphur_dioxide"),
            sulphur_dioxide_std_dev=StdDev("sulphur_dioxide"),
            carbon_monoxide_avg=Avg("carbon_monoxide"),
            # carbon_monoxide_median=Median("carbon_monoxide"),
            carbon_monoxide_std_dev=StdDev("carbon_monoxide"),
            organic_carbon_avg=Avg("organic_carbon"),
            # organic_carbon_median=Median("organic_carbon"),
            organic_carbon_std_dev=StdDev("organic_carbon"),
            nmvoc_avg=Avg("non_methane_volatile_organic_compounds"),
            # nmvoc_median=Median("non_methane_volatile_organic_compounds"),
            nmvoc_std_dev=StdDev("non_methane_volatile_organic_compounds"),
            black_carbon_avg=Avg("black_carbon"),
            # black_carbon_median=Median("black_carbon"),
            black_carbon_std_dev=StdDev("black_carbon"),
            ammonia_avg=Avg("ammonia"),
            # ammonia_median=Median("ammonia"),
            ammonia_std_dev=StdDev("ammonia"),
        )


class PollutionManager(models.Manager):
    def get_queryset(self):
        return PollutionQuerySet(self.model, using=self._db)

    def with_statistics(self):
        return self.get_queryset().with_statistics()
