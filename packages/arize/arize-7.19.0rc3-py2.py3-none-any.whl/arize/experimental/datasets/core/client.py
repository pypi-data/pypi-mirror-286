import json
import time
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd
import pyarrow as pa
from google.protobuf import json_format, message
from pyarrow import flight

from .. import requests_pb2 as request_pb
from ..experiments.evaluators.base import Evaluators
from ..experiments.functions import run_experiment
from ..experiments.types import ExperimentTask
from ..utils.constants import (
    ARIZE_PROFILE,
    DEFAULT_ARIZE_FLIGHT_HOST,
    DEFAULT_ARIZE_FLIGHT_PORT,
    DEFAULT_CONFIG_PATH,
    DEFAULT_PROFILE_NAME,
    DEFAULT_TRANSPORT_SCHEME,
    FLIGHT_ACTION_KEY,
    OPEN_INFERENCE_JSON_STR_TYPES,
)
from ..validation.validator import Validator
from .session import Session


@dataclass
class ArizeDatasetsClient:
    """
    ArizeDatasetsClient is a client for interacting with the Arize Datasets API.

    Args:
        api_key (str, optional): Arize provided personal API key associated with your user profile,
            located on the API Explorer page. API key is required to initiate a new client, it can
            be passed in explicitly, or set up as an environment variable or in profile file.
        arize_profile (str, optional): profile name for ArizeExportClient credentials and endpoint.
            Defaults to '{DEFAULT_PROFILE_NAME}'.
        arize_config_path (str, optional): path to the config file that stores ArizeExportClient
            credentials and endpoint. Defaults to '~/.arize'.
        host (str, optional): URI endpoint host to send your export request to Arize AI. Defaults to
            "{DEFAULT_ARIZE_FLIGHT_HOST}".
        port (int, optional): URI endpoint port to send your export request to Arize AI. Defaults to
            {DEFAULT_ARIZE_FLIGHT_PORT}.
        scheme (str, optional): Transport scheme to use for the connection. Defaults to
            "{DEFAULT_TRANSPORT_SCHEME}".

    Attributes:
        session (Session): The session object used for making API requests.

    """

    api_key: Optional[str] = None
    arize_profile: str = ARIZE_PROFILE or DEFAULT_PROFILE_NAME
    arize_config_path: str = DEFAULT_CONFIG_PATH
    host: str = DEFAULT_ARIZE_FLIGHT_HOST
    port: int = DEFAULT_ARIZE_FLIGHT_PORT
    scheme: str = DEFAULT_TRANSPORT_SCHEME

    def __post_init__(self) -> None:
        """
        Initializes the Arize Dataset Client.
        """
        self.__session = Session(
            self.api_key,
            self.arize_profile,
            self.arize_config_path,
            self.host,
            self.port,
            self.scheme,
        )

    @property
    def session(self) -> Session:
        return self.__session

    def run_experiment(
        self,
        space_id: str,
        experiment_name: str,
        task: ExperimentTask,
        dataset_id: str = "",
        dataset_name: str = "",
        evaluators: Optional[Evaluators] = None,
    ) -> Optional[str]:

        if not (dataset_id or dataset_name):
            raise ValueError("Either dataset_id or dataset_name must be provided")

        dataset = self.get_dataset(
            space_id=space_id, dataset_id=dataset_id, dataset_name=dataset_name
        )
        if dataset is None or dataset.empty:
            raise RuntimeError("Dataset is empty or does not exist")

        exp_df = run_experiment(
            dataset=dataset,
            task=task,
            evaluators=evaluators,
            experiment_name=experiment_name,
        )

        pa_schema = pa.Schema.from_pandas(exp_df)
        new_schema = pa.schema([field for field in pa_schema])
        tbl = pa.Table.from_pandas(exp_df, schema=new_schema)
        request = request_pb.DoPutRequest(
            create_experiment=request_pb.CreateExperimentRequest(
                space_id=space_id,
                dataset_id=dataset_id,
                experiment_name=experiment_name,
            )
        )

        descriptor = self._descriptor_for_request(request)
        flight_client = self.session.connect()

        try:
            writer, metadata_reader = flight_client.do_put(
                descriptor, tbl.schema, self.session.call_options
            )
            with writer:
                writer.write_table(tbl, max_chunksize=10_000)
                writer.done_writing()
                response = metadata_reader.read()
                if response is not None:
                    res = request_pb.CreateDatasetResponse()
                    res.ParseFromString(response.to_pybytes())
                    return str(res.dataset_id)
        except Exception as e:
            raise RuntimeError("Failed to create dataset") from e
        finally:
            flight_client.close()

    def create_dataset(
        self,
        space_id: str,
        dataset_name: str,
        dataset_type: request_pb.DatasetType,
        data: pd.DataFrame,
        convert_dict_to_json: bool = True,
    ) -> Optional[str]:
        """
        Create a new dataset.

        Args:
            space_id (str): The ID of the space where the dataset will be created.
            dataset_name (str): The name of the dataset.
            dataset_type (DatasetType): The type of the dataset.
            data (pd.DataFrame): The data to be included in the dataset.

        Returns:
            str: The ID of the created dataset, or None if the creation failed.
        """
        ## Validate and convert to arrow table
        df = self._set_default_columns_for_dataset(data)
        if convert_dict_to_json:
            df = self._convert_default_columns_to_json_str(df)
        validation_errors = Validator.validate(df)
        if validation_errors:
            raise RuntimeError([e.error_message() for e in validation_errors])

        pa_schema = pa.Schema.from_pandas(df)
        new_schema = pa.schema([field for field in pa_schema])
        tbl = pa.Table.from_pandas(df, schema=new_schema)

        request = request_pb.DoPutRequest(
            create_dataset=request_pb.CreateDatasetRequest(
                space_id=space_id,
                dataset_name=dataset_name,
                dataset_type=dataset_type,
            )
        )
        descriptor = self._descriptor_for_request(request)
        flight_client = self.session.connect()

        try:
            writer, metadata_reader = flight_client.do_put(
                descriptor, tbl.schema, self.session.call_options
            )
            with writer:
                writer.write_table(tbl, max_chunksize=10_000)
                writer.done_writing()
                response = metadata_reader.read()
                if response is not None:
                    res = request_pb.CreateDatasetResponse()
                    res.ParseFromString(response.to_pybytes())
                    return str(res.dataset_id)
        except Exception as e:
            raise RuntimeError("Failed to create dataset") from e
        finally:
            flight_client.close()

    def update_dataset(self, space_id: str, dataset_id: str, data: pd.DataFrame) -> Optional[str]:
        """
        Update an existing dataset by creating a new version.

        Args:
            space_id (str): The ID of the space where the dataset is located.
            dataset_id (str): The ID of the dataset to update.
            data (pd.DataFrame): The updated data to be included in the dataset.

        Returns:
            str: The ID of the updated dataset, or None if the update failed.
        """
        df = self._set_default_columns_for_dataset(data)
        validation_errors = Validator.validate(df)
        if validation_errors:
            raise RuntimeError([e.error_message() for e in validation_errors])
        pa_schema = pa.Schema.from_pandas(df)
        new_schema = pa.schema([field for field in pa_schema])
        tbl = pa.Table.from_pandas(df, schema=new_schema)

        request = request_pb.DoPutRequest(
            update_dataset=request_pb.UpdateDatasetRequest(
                space_id=space_id,
                dataset_id=dataset_id,
            )
        )
        descriptor = self._descriptor_for_request(request)
        flight_client = self.session.connect()
        try:
            writer, metadata_reader = flight_client.do_put(
                descriptor, tbl.schema, self.session.call_options
            )
            with writer:
                writer.write_table(tbl, max_chunksize=10_000)
                writer.done_writing()
                response = metadata_reader.read()
                if response is not None:
                    res = request_pb.UpdateDatasetResponse()
                    res.ParseFromString(response.to_pybytes())
                    return str(res.dataset_id)
        except Exception as e:
            raise RuntimeError("Failed to update dataset") from e
        finally:
            flight_client.close()

    def get_dataset(
        self,
        space_id: str,
        dataset_id: str = "",
        dataset_name: str = "",
        dataset_version: str = "",
        convert_json_str_to_dict: bool = True,
    ) -> pd.DataFrame | None:
        """
        Get the data of a dataset.

        Args:
            space_id (str): The ID of the space where the dataset is located.
            dataset_id (str): The ID of the dataset to get.
            dataset_version (str, optional): The version name of the dataset to get.
            Defaults to "" and grabs the latest version by created_at.

        Returns:
            pd.DataFrame: The data of the dataset.
        """
        if dataset_id:
            request = request_pb.DoGetRequest(
                get_dataset=request_pb.GetDatasetRequest(
                    space_id=space_id, dataset_version=dataset_version, dataset_id=dataset_id
                )
            )
        elif dataset_name:
            request = request_pb.DoGetRequest(
                get_dataset=request_pb.GetDatasetRequest(
                    space_id=space_id, dataset_version=dataset_version, dataset_name=dataset_name
                )
            )
        else:
            raise ValueError("Either dataset_id or dataset_name must be provided")

        flight_client = self.session.connect()
        ticket = self._ticket_for_request(request)
        try:
            reader = flight_client.do_get(ticket, self.session.call_options)
            df = reader.read_all().to_pandas()
            if convert_json_str_to_dict:
                df = self._convert_json_str_to_dict(df)
            return df
        except Exception as e:
            raise RuntimeError("Failed to get dataset") from e
        finally:
            flight_client.close()

    def get_dataset_versions(self, space_id: str, dataset_id: str) -> List[Dict[str, Any]]:
        """
        Get the versions of a dataset.

        Args:
            space_id (str): The ID of the space where the dataset is located.
            dataset_id (str): The ID of the dataset to get versions for.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the versions of the dataset.
        """
        request = request_pb.DoActionRequest(
            get_dataset_versions=request_pb.GetDatasetVersionsRequest(
                space_id=space_id, dataset_id=dataset_id
            )
        )
        action = self._action_for_request(FLIGHT_ACTION_KEY.GET_DATASET_VERSION, request)
        flight_client = self.session.connect()
        try:
            res = flight_client.do_action(action, self.session.call_options)
            # Close the client here to drain the response stream
            flight_client.close()
            res = next(res, None)
            if not res:
                return []
            resp_pb = request_pb.GetDatasetVersionsResponse()
            resp_pb.ParseFromString(res.body.to_pybytes())
            out = []
            for v in resp_pb.versions:
                out.append(
                    {
                        "dataset_version": v.version_name,
                        "created_at": v.created_at.ToJsonString(),
                        "updated_at": v.updated_at.ToJsonString(),
                    }
                )
            return out
        except Exception as e:
            raise RuntimeError("Failed to get dataset versions") from e

    def list_datasets(self, space_id: str) -> List[Dict[str, Any]]:
        """
        List all datasets in a space.

        Args:
            space_id (str): The ID of the space to list datasets for.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the datasets in the space.
        """
        request = request_pb.DoActionRequest(
            list_datasets=request_pb.ListDatasetsRequest(space_id=space_id)
        )
        action = self._action_for_request(FLIGHT_ACTION_KEY.LIST_DATASETS, request)
        flight_client = self.session.connect()
        try:
            res = flight_client.do_action(action, self.session.call_options)
            # Close the client here to drain the response stream
            flight_client.close()
            res = next(res, None)
            if not res:
                return []
            resp_pb = request_pb.ListDatasetsResponse()
            resp_pb.ParseFromString(res.body.to_pybytes())

            out = []
            for dataset in resp_pb.datasets:
                out.append(
                    {
                        "dataset_id": dataset.dataset_id,
                        "dataset_name": dataset.dataset_name,
                        "dataset_type": request_pb.DatasetType.Name(dataset.dataset_type),
                        "created_at": dataset.created_at.ToJsonString(),
                        "updated_at": dataset.updated_at.ToJsonString(),
                    }
                )
            return out
        except Exception as e:
            raise RuntimeError("Failed to get all datasets") from e

    def delete_dataset(self, space_id: str, dataset_id: str) -> bool:
        """
        Delete a dataset.

        Args:
            space_id (str): The ID of the space where the dataset is located.
            dataset_id (str): The ID of the dataset to delete.

        Returns:
            bool: True if the dataset was successfully deleted, False otherwise.
        """
        request = request_pb.DoActionRequest(
            delete_dataset=request_pb.DeleteDatasetRequest(space_id=space_id, dataset_id=dataset_id)
        )
        action = self._action_for_request(FLIGHT_ACTION_KEY.DELETE_DATASET, request)
        flight_client = self.session.connect()
        try:
            res = flight_client.do_action(action, self.session.call_options)
            # Close the client here to drain the response stream
            flight_client.close()
            res = next(res, None)
            if not res:
                return False
            resp_pb = request_pb.DeleteDatasetResponse()
            resp_pb.ParseFromString(res.body.to_pybytes())
            return resp_pb.success
        except Exception as e:
            raise RuntimeError("Failed to delete dataset") from e

    def _descriptor_for_request(self, request: message) -> flight.FlightDescriptor:
        data = json_format.MessageToJson(request).encode("utf-8")
        return flight.FlightDescriptor.for_command(data)

    def _ticket_for_request(self, request: message) -> flight.Ticket:
        data = json_format.MessageToJson(request).encode("utf-8")
        return flight.Ticket(data)

    def _action_for_request(self, action_key: FLIGHT_ACTION_KEY, request: message) -> flight.Action:
        req_bytes = json_format.MessageToJson(request).encode("utf-8")
        return flight.Action(action_key.value, req_bytes)

    @staticmethod
    def _set_default_columns_for_dataset(df: pd.DataFrame) -> pd.DataFrame:
        current_time = int(time.time() * 1000)
        if "created_at" in df.columns:
            if df["created_at"].isnull().values.any():
                df["created_at"].fillna(current_time, inplace=True)
        else:
            df["created_at"] = current_time

        if "updated_at" in df.columns:
            if df["updated_at"].isnull().values.any():
                df["updated_at"].fillna(current_time, inplace=True)
        else:
            df["updated_at"] = current_time

        if "id" in df.columns:
            if df["id"].isnull().values.any():
                df["id"] = df["id"].apply(lambda x: str(uuid.uuid4()) if pd.isnull(x) else x)
        else:
            df["id"] = [str(uuid.uuid4()) for _ in range(len(df))]

        return df

    @staticmethod
    def _convert_default_columns_to_json_str(df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            if col in OPEN_INFERENCE_JSON_STR_TYPES:
                try:
                    df[col] = df[col].apply(lambda x: json.dumps(x))
                    print(f"converted {col} to json str")
                except Exception:
                    continue
        return df

    @staticmethod
    def _convert_json_str_to_dict(df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            if col in OPEN_INFERENCE_JSON_STR_TYPES:
                try:
                    df[col] = df[col].apply(lambda x: json.loads(x))
                    print(f"converted {col} to dict")
                except Exception:
                    continue
        return df
