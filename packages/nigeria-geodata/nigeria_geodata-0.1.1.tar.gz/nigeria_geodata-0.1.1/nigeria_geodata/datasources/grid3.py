"""

Grid3 data source implementation module.

Authors:

Date:

"""

from functools import cache
import json
from math import ceil
from typing import List, Optional, Union

from nigeria_geodata.async_core import AsyncBaseDataSource
from nigeria_geodata.config import Config
from nigeria_geodata.core import SyncBaseDataSource
from nigeria_geodata.datasources import DataSource
from nigeria_geodata.models.common import (
    EsriFeatureLayerBasicInfo,
    EsriFeatureServiceBasicInfo,
    EsriFeatureServiceDetailedInfo,
    Feature,
    FeatureCollection,
)
from nigeria_geodata.utils.api import make_request
from nigeria_geodata.utils.common import (
    geojson_to_esri_type,
)

from nigeria_geodata.utils.enums import NigeriaState
from nigeria_geodata.utils.validators import validate_geojson
import pandas as pd
from nigeria_geodata.utils.logging import logger


class EsriFeatureLayers:
    def __init__(
        self, feature_layers: List[EsriFeatureLayerBasicInfo], total_layers: int
    ) -> None:
        self.feature_layers = feature_layers
        self.total_layers = total_layers

    def __repr__(self) -> str:
        return f"<EsriFeatureLayers {[x for x in self.feature_layers ]}>"

    def first(self) -> EsriFeatureLayerBasicInfo:
        """Return the first layer in the feature layers"""
        # use the id to get the detailed information about it from the server.
        # why would a user need the first one, to download or query, if yes, what do we need that we don't already have?
        return EsriFeatureLayerBasicInfo(**self.feature_layers[0].__dict__)

    def __validate_index(self, id: int):
        """
        Validate that the provided index is within the available results.

        """
        assert (
            id <= self.total_layers + 1
        ), f"Provided index is out of range. Valid values are between 1 - {self.total_layers}"

    def get(self, id: int = None, name: str = None) -> EsriFeatureLayerBasicInfo:
        """Return the layer that match the id or name"""
        # use the id to get the detailed information about it from the server.
        # why would a user need the first one, to download or query, if yes, what do we need that we don't already have?
        if id:
            self.__validate_index(id)
            return EsriFeatureLayerBasicInfo(**self.feature_layers[id - 1])
        if name:
            return list(
                map(
                    lambda x: EsriFeatureLayerBasicInfo(**x.__dict__),
                    filter(
                        lambda x: name.lower() in str(x["name"]).lower(),
                        self.feature_layers,
                    ),
                )
            )
        return None


class EsriFeatureService:
    def __init__(self, feature_service: EsriFeatureServiceDetailedInfo) -> None:
        self.feature_service = feature_service

    @cache
    def get_max_features(self, service_url: str) -> int:
        params = {
            "where": "FID > 0",
            "groupByFieldsForStatistics": "",
            "orderByFields": "",
            "returnDistinctValues": "true",
            "outStatistics": [
                [
                    {
                        "statisticType": "count",
                        "onStatisticField": "FID",
                        "outStatisticFieldName": "COUNT",
                    }
                ]
            ],
            "f": "json",
        }
        res = make_request(service_url, params=params)
        return res["features"][0]["attributes"]["COUNT"]

    def filter(
        self,
        layer_id: int,  # a feature service can have many layers, allow them to pass the one they want here.
        state: Optional[str] = None,
        bbox: Optional[List[float]] = None,
        aoi_geojson: Optional[Union[Feature, FeatureCollection]] = None,
        dataframe: bool = True,
    ) -> pd.DataFrame:
        """
        Filter the service across multiple layers.
        """
        # todo confirm that the service support query?
        # get the total data in the layers
        # get the maximum offset in the info so as to make the request in a loop

        # only one parameter can be provided, so this check is to ensure that.
        params = sum([state is not None, bbox is not None, aoi_geojson is not None])

        if params != 1:
            raise ValueError(
                "Exactly one parameter (state, bbox, or aoi_geojson) must be provided."
            )

        # State validation
        # esri_bbox = None
        # default to the esriGeometryEnvelope which is like the bbox.
        # only change it when the user provide an aoi
        geometryType = "esriGeometryEnvelope"

        if state is not None:
            if isinstance(state, str):
                assert state in [
                    x.value for x in NigeriaState
                ], "The provided state is not a valid Nigeria State."

        # BBox validation
        if bbox is not None:
            if isinstance(bbox, list):
                if len(bbox) != 4 or not all(
                    isinstance(coord, (int, float)) for coord in bbox
                ):
                    raise ValueError(
                        "The provided bbox is invalid. It should be a list of four numeric values."
                    )
            # update esribbox

        # GeoJSON validation
        if aoi_geojson is not None:
            if isinstance(aoi_geojson, (Feature, FeatureCollection)):
                validate_geojson(aoi_geojson)
            elif isinstance(aoi_geojson, str):
                try:
                    obj = json.loads(aoi_geojson)
                    if obj.get("type") == "Feature":
                        feature = Feature(**obj)
                        validate_geojson(feature)
                    elif obj.get("type") == "FeatureCollection":
                        feature_collection = FeatureCollection(**obj)
                        validate_geojson(feature_collection)
                    else:
                        raise ValueError("Invalid GeoJSON string.")
                except (json.JSONDecodeError, ValueError) as e:
                    raise ValueError(f"Invalid GeoJSON string: {e}")
            else:
                raise ValueError(
                    "The provided GeoJSON must be a Feature, FeatureCollection, or a JSON string representing one of these."
                )

            # update geometry type
            geometryType = geojson_to_esri_type(aoi_geojson.geometry.type)

        # Layer_id validation
        if not isinstance(layer_id, int):
            raise ValueError(
                "Invalid layer_id provided. layer_id must be a valid integer."
            )

        valid_layer_ids = {idx["id"] for idx in self.feature_service.layers}
        if layer_id not in valid_layer_ids:
            raise ValueError(
                "Invalid layer_id provided. The provided layer_id is not available in this feature service."
            )

        # build the query
        params = {
            # get layer id from featureinfo ? because for now we're adding 1  to the query url
            "where": "FID > 0",  # this is required. We're assuming all data has `FID` here.
            "geometryType": geometryType,
            "f": "geojson",  # check the supported formats to know the one to user, if geojson is not supported, then use json and convert to geojson
        }
        req_url = f"{self.feature_service.featureServerURL}/{layer_id}/query"
        max_features = self.get_max_features(req_url)
        if max_features == 0:
            return []
        result_list = []
        resultOffset = 0
        max_request = ceil(max_features / self.feature_service.maxRecordCount)
        for _ in range(max_request):
            params["resultOffset"] = resultOffset
            features = make_request(req_url, params=params)["features"]
            result_list.extend(features)
            resultOffset += self.feature_service.maxRecordCount
        if dataframe:
            # geodataframe ?
            return pd.DataFrame(result_list)
        return result_list

    def layers(self, dataframe: bool = True) -> EsriFeatureLayers:
        """
        Return the available layers in the FeatureService.
        First - service returns many layers, default to the first, make false if otherwise, but in that case, the id or name of the layer will be required.
        """

        # return dataframe if the user provide the option to preview all data?

        return EsriFeatureLayers(
            self.feature_service.layers,
            total_layers=len(self.feature_service.layers) - 1,
        )

    def __repr__(self) -> str:
        return "<EsriFeatureService>"


class EsriRootFeatureServer:
    def __init__(
        self, feature_services: List[EsriFeatureServiceBasicInfo], total_services: int
    ) -> None:
        self.feature_services = feature_services
        self.total_services = total_services
        self.feature_server_id = 1

    def __validate_index(self, id: int):
        """
        Validate that the provided index is within the available results.

        """
        assert (
            id <= self.total_services
        ), f"Provided index is out of range. Valid values are between 1 - {self.total_services}"

    @cache
    def get(
        self, id: int, dataframe: bool = True
    ) -> Union[pd.DataFrame, EsriFeatureService]:
        """
        Connect to a FeatureServer and retrieve more information about it.

        Parameters:
            id (int): The ID of the feature service.
            dataframe (bool): If True, returns the information as a pandas DataFrame.
                              If False, returns an EsriFeatureService object.

        Returns:
            Union[pd.DataFrame, EsriFeatureService]: A DataFrame or an EsriFeatureService object.
        """
        self.__validate_index(id)

        query_params = {"f": "json"}
        # since one was added before, so we can remove it here to avoid list out of range error.
        feature_server = self.feature_services[id - 1]
        response = make_request(f"{feature_server.url}", query_params)
        feature_service = EsriFeatureServiceDetailedInfo(
            serviceDescription=response["serviceDescription"],
            serviceItemId=response["serviceItemId"],
            maxRecordCount=response["maxRecordCount"],
            supportedQueryFormats=response["supportedQueryFormats"],
            supportedExportFormats=response["supportedExportFormats"],
            capabilities=response["capabilities"],
            description=response["description"],
            copyrightText=response["copyrightText"],
            spatialReference=response["spatialReference"],
            fullExtent=response["fullExtent"],
            layers=response["layers"],
            tables=response["tables"],
            featureServerURL=feature_server.url,
        )
        if dataframe:
            data = feature_service.__dict__
            transformed_data = {"Key": list(data.keys()), "Value": list(data.values())}
            return pd.DataFrame(transformed_data)
        return EsriFeatureService(feature_service)

    def __repr__(self) -> str:
        return f"<EsriRootFeatureServer services={self.total_services}>"


class Grid3(SyncBaseDataSource):
    service_url: str = Config.get_service_url(DataSource.GRID3)
    service_info_url: str = Config.get_service_info_url(DataSource.GRID3)

    def _get_feature_services(self) -> List[EsriFeatureServiceBasicInfo]:
        """
        Retrieve the feature servers with Nigeria data from the ArcGIS Server root directory,
        """

        api_response = make_request(self.service_url)

        # based on review of the datasets, Nigeria is either represented as Nigeria or NGA
        # For now it works, but this has a potential for improvement.
        feature_services = list(
            map(
                lambda feature_service: EsriFeatureServiceBasicInfo(
                    feature_service["name"],
                    feature_service["url"],
                    feature_service["type"],
                ),
                filter(
                    lambda response_obj: "NGA" in str(response_obj["name"]).upper()
                    or "NIGERIA" in str(response_obj["name"]).upper(),
                    api_response.get("services", []),
                ),
            ),
        )
        return feature_services

    @cache
    def list_data(
        self, dataframe: bool = True
    ) -> Union[EsriRootFeatureServer, pd.DataFrame]:
        """List available datasets from the datasource"""
        feature_services = self._get_feature_services()
        total_services = len(feature_services) - 1
        logger.info(
            f"There is a total {total_services} feature services with Nigeria geodata."
        )
        if dataframe:
            data = {
                "ID": list(range(1, len(feature_services))),
                "Name": [feature_service.name for feature_service in feature_services],
            }
            return pd.DataFrame(data)
        return EsriRootFeatureServer(feature_services, total_services)

    def search(
        self, query: str, dataframe: bool = False
    ) -> Union[EsriRootFeatureServer, pd.DataFrame]:
        feature_servers = self._get_feature_services()
        # from the feature servers response do a string matching for the user query
        search_results = list(
            filter(
                lambda feature_server: query.upper()
                in str(feature_server.name).upper(),
                feature_servers,
            ),
        )

        if dataframe:
            data = {
                "ID": list(range(1, len(search_results))),
                "Name": [feature_service.name for feature_service in search_results],
            }
            return pd.DataFrame(data)
        return EsriRootFeatureServer(search_results, len(search_results))

    def __repr__(self) -> str:
        return "<Grid3>"


class AsyncGrid3(AsyncBaseDataSource):
    service_url: str = Config.get_service_url(DataSource.GRID3)

    async def list_data(self):
        # list available datasets in the data source
        # preview = true to preview on a static map as thumbnail, interactive = true to preview on interactive map e.g lon board
        ...

    def __repr__(self) -> str:
        return "<AsyncGrid3Data>"


if __name__ == "__main__":
    data_source = Grid3()

    # search for the specific dataset you need
    # it can return multiple results
    # suggest source e.g themes in documentation?
    # otherwise they might not see any result.
    search_results = data_source.search("health")
    # retrieve the specific one from the search result/data list using the id
    # todo - allow them to provide the name of the dataset as well, to make the code easy to read
    # e.g search_results.get('Nigeri_Health')
    service = search_results.get(1, False)
    # this is a query to the feature service
    # at this point, you can query the data with state, lga and bounding box, or geojson
    filtered_result = service.filter(layer_id=1, state="Lagos")
    # the result will be ResultSet that can be exported

    # all above can be piped into a single line of code
    # data = data_source.search("health").get(1).filter(state=Lagos)
    # # Front the service, you can also query specific layers of interest
    # # a service can have multiple layers, use .layers() to find out.
    # # default to the first layer, also support .first() if they want to be sure
    # layers = service.layers().get(id=1)
    # # or pass the id/name of the layer of interest, but use show=True above to list the layers to you can get the id and name
    # # i.e layers = service.layers(show=True)
    # layers = service.layers(1)
    # # should we all the user of .all() to filter all layers?
    # # you can filter based on state, lga, bounding box etc

    # all these will still be in memory until the use .fetch() ? before the actual data is retrived from esri to optimize speed
    print(filtered_result)
