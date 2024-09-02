from rest_framework import serializers


class ParamsNestedSerializer(serializers.Serializer):
    """
    Nested serializer for each pollution parameter
    """

    nitrogen_oxide = serializers.FloatField()
    sulphur_dioxide = serializers.FloatField()
    carbon_monoxide = serializers.FloatField()
    organic_carbon = serializers.FloatField()
    nmvoc = serializers.FloatField()
    black_carbon = serializers.FloatField()
    ammonia = serializers.FloatField()


class PollutionStatsSerializer(serializers.Serializer):
    """
    Main serializer for pollution statistics
    """

    entity = serializers.CharField()
    average = ParamsNestedSerializer()
    # median = ParamsNestedSerializer()
    std_dev = ParamsNestedSerializer()
