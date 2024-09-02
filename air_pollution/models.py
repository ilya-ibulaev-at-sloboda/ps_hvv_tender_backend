from django.db import models


class Pollution(models.Model):
    """
    Entity,
    Code,
    Year,
    Nitrogen oxide (NOx),
    Sulphur dioxide (SO₂) emissions,
    Carbon monoxide (CO) emissions,
    Organic carbon (OC) emissions,
    Non-methane volatile organic compounds (NMVOC) emissions,
    Black carbon (BC) emissions,
    Ammonia (NH₃) emissions,
    """

    entity = models.CharField(max_length=255)
    iso = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField()
    nitrogen_oxide = models.FloatField(help_text="Nitrogen oxide (NOx)")
    sulphur_dioxide = models.FloatField(help_text="Sulphur dioxide (SO₂) emissions")
    carbon_monoxide = models.FloatField(help_text="Carbon monoxide (CO) emissions")
    organic_carbon = models.FloatField(help_text="Organic carbon (OC) emissions")
    non_methane_volatile_organic_compounds = models.FloatField(
        help_text="Non-methane volatile organic compounds (NMVOC) emissions"
    )
    black_carbon = models.FloatField(help_text="Black carbon (BC) emissions")
    ammonia = models.FloatField(help_text="Ammonia (NH₃) emissions")

    class Meta:
        indexes = [
            models.Index(fields=["entity"]),
            models.Index(fields=["year"]),
            models.Index(fields=["entity", "year"]),
        ]
        ordering = ["entity", "year"]
        unique_together = ["entity", "year"]

    def __str__(self):
        return self.entity
