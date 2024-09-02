from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from air_pollution.models import Pollution
from air_pollution.serializers import PollutionStatsSerializer


class PollutionStatsView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, entity):
        # Fetching data for the specified entity using the custom manager's method
        pollution_stats = Pollution.objects.filter(entity=entity).with_statistics()

        if not pollution_stats:
            return Response({"error": "Entity not found"}, status=404)

        # Structuring the data using the custom serializer
        response_data = []
        for stat in pollution_stats:
            response_data.append(
                {
                    "entity": stat["entity"],
                    # "year": stat["year"],
                    "average": {
                        "nitrogen_oxide": stat["nitrogen_oxide_avg"],
                        "sulphur_dioxide": stat["sulphur_dioxide_avg"],
                        "carbon_monoxide": stat["carbon_monoxide_avg"],
                        "organic_carbon": stat["organic_carbon_avg"],
                        "nmvoc": stat["nmvoc_avg"],
                        "black_carbon": stat["black_carbon_avg"],
                        "ammonia": stat["ammonia_avg"],
                    },
                    # "median": {
                    #     "nitrogen_oxide": stat["nitrogen_oxide_median"],
                    #     "sulphur_dioxide": stat["sulphur_dioxide_median"],
                    #     "carbon_monoxide": stat["carbon_monoxide_median"],
                    #     "organic_carbon": stat["organic_carbon_median"],
                    #     "nmvoc": stat["nmvoc_median"],
                    #     "black_carbon": stat["black_carbon_median"],
                    #     "ammonia": stat["ammonia_median"],
                    # },
                    "std_dev": {
                        "nitrogen_oxide": stat["nitrogen_oxide_std_dev"],
                        "sulphur_dioxide": stat["sulphur_dioxide_std_dev"],
                        "carbon_monoxide": stat["carbon_monoxide_std_dev"],
                        "organic_carbon": stat["organic_carbon_std_dev"],
                        "nmvoc": stat["nmvoc_std_dev"],
                        "black_carbon": stat["black_carbon_std_dev"],
                        "ammonia": stat["ammonia_std_dev"],
                    },
                }
            )

        return Response(PollutionStatsSerializer(response_data, many=True).data)
