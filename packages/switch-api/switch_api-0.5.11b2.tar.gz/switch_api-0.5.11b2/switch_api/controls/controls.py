# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""
A module for sending control request of sensors.
"""

import json
import logging
import os
import sys
import time
from typing import Dict, Union, Optional
import uuid
import pandas
import requests

from ._enums import ControlStatus
from ._constants import IOT_RESPONSE_ERROR, IOT_RESPONSE_SUCCESS, WS_DEFAULT_PORT, WS_MQTT_CONNECTION_TIMEOUT, WS_MQTT_DEFAULT_MAX_TIMEOUT
from ._mqtt import SwitchMQTT
from .._utils._utils import ApiInputs, _with_func_attrs, is_valid_uuid
from ..cache.cache import get_cache, set_cache

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s  %(name)s.%(funcName)s  %(levelname)s: %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')
consoleHandler.setFormatter(formatter)

global _control_api_endpoint
global _control_ws_host
global _control_ws_port
global _control_ws_username
global _control_ws_password
global _control_ws_max_timeout

_control_api_endpoint = ''
_control_ws_host = ''
_control_ws_port = WS_DEFAULT_PORT
_control_ws_username = ''
_control_ws_password = ''
_control_ws_max_timeout = WS_MQTT_DEFAULT_MAX_TIMEOUT

global _control_components

_control_components = {}


def set_control_variables(api_endpoint: str, ws_host: str, user_name: str, password: str,
                          ws_port: int = WS_DEFAULT_PORT, max_timeout: int = WS_MQTT_DEFAULT_MAX_TIMEOUT):
    """Set Control Variables

    Set Control Variables needed to enable control request to MQTT Broker when running locally.

    In Production, these are pulled from the deployment environment variables.

    Parameters
    ----------
    api_endpoint : str
        Platform IoT API Endpoint.
    host : str
        Host URL for MQTT connection. This needs to be datacenter specfic URL.
    port : int
        MQTT message broker port. Defaults to 443.
    user_name : str
        Username for MQTT connection
    password: str
        Password for MQTT connection
    max_timeout : int
        Max timeout set for the controls module. Defaults to 30 seconds.
    """
    global _control_api_endpoint
    global _control_ws_host
    global _control_ws_port
    global _control_ws_username
    global _control_ws_password
    global _control_ws_max_timeout

    # Check if endpoint is a valid URL
    if not api_endpoint.startswith('https://'):
        raise ValueError(
            "Invalid IoT API Endpoint. The IoT host should start with 'https://'.")

    # Check if host is a valid URL
    if not ws_host.startswith('wss://'):
        raise ValueError(
            "Invalid IoT Websocket MQTT Host. The IoT host should start with 'wss://'.")

    # Check if user_name and password are not empty
    if not user_name:
        raise ValueError("user_name cannot be empty.")
    if not password:
        raise ValueError("password cannot be empty.")

    # Check if max_timeout is greated than 0
    if max_timeout < 1:
        raise ValueError("max_timeout should be greater than 0.")

    # Set global variables
    _control_api_endpoint = api_endpoint
    _control_ws_host = ws_host
    _control_ws_port = ws_port
    _control_ws_username = user_name
    _control_ws_password = password
    _control_ws_max_timeout = max_timeout


def submit_control_continue(api_inputs: ApiInputs, data: pandas.DataFrame, information_columns: list = [], is_send_control: bool = True):
    global _control_components
    control_results = []

    # Validate Information Columns if existing
    missing_columns = [
        col for col in information_columns if col not in data.columns]

    if missing_columns:
        logger.error(
            f"These columns are not in the DataFrame: {missing_columns}")
        raise ValueError(
            f"These columns are not in the DataFrame: {missing_columns}")

    for name, value in _control_components.items():
        column_with_object_installation_id = value[0]
        column_with_object_property_id = value[1]
        column_with_label = value[2]
        column_with_value = value[3]
        column_with_continue = value[4]
        column_with_default_value = value[5]
        timeoutMinutes = value[6]
        priority = value[7]

        if column_with_object_property_id not in data.columns:
            logger.error(
                f"ObjectPropertyId column {column_with_object_property_id} not found in the DataFrame")
            raise ValueError(
                f"ObjectPropertyId column {column_with_object_property_id} not found in the DataFrame")
        elif column_with_label not in data.columns:
            logger.error(
                f"Label column {column_with_label} not found in the DataFrame")
            raise ValueError(
                f"Label column {column_with_label} not found in the DataFrame")
        elif column_with_value not in data.columns:
            logger.error(
                f"Value column {column_with_value} not found in the DataFrame")
            raise ValueError(
                f"Value column {column_with_value} not found in the DataFrame")
        elif column_with_object_installation_id not in data.columns:
            logger.error(
                f"InstallationId column {column_with_object_installation_id} not found in the DataFrame")
            raise ValueError(
                f"InstallationId column {column_with_object_installation_id} not found in the DataFrame")
        elif "TimestampLocal" not in data.columns:
            logger.error(
                f"TimestampLocal not found in the DataFrame")
            raise ValueError(
                f"TimestampLocal not found in the DataFrame")
        elif column_with_continue not in data.columns:
            logger.error(
                f"Continue column {column_with_continue} not found in the DataFrame")
            raise ValueError(
                f"Continue column {column_with_continue} not found in the DataFrame")
        elif column_with_default_value != None and column_with_default_value not in data.columns:
            logger.error(
                f"Default Value column {column_with_default_value} not found in the DataFrame")
            raise ValueError(
                f"Default Value column {column_with_default_value} not found in the DataFrame")

        data[column_with_value] = pandas.to_numeric(
            data[column_with_value], errors='coerce')

        grouped = data.groupby(column_with_object_installation_id)

        for installation_id, group in grouped:

            control_df = pandas.DataFrame()
            group["ControlName"] = name

            if column_with_default_value == None:
                control_df = pandas.DataFrame({
                    'ControlName': group['ControlName'],
                    'ObjectPropertyId': group[column_with_object_property_id],
                    'Label': group[column_with_label],
                    'Value': group[column_with_value],
                    'ContinueValue': group[column_with_continue],
                    'TTL': timeoutMinutes,
                    'Priority': priority
                })
            else:
                control_df = pandas.DataFrame({
                    'ControlName': group['ControlName'],
                    'ObjectPropertyId': group[column_with_object_property_id],
                    'Label': group[column_with_label],
                    'Value': group[column_with_value],
                    'ContinueValue': group[column_with_continue],
                    'DefaultControlValue': group[column_with_default_value],
                    'TTL': timeoutMinutes,
                    'Priority': priority
                })

            control_df = control_df.dropna(subset=['Value'])

            try:
                control_result_df = group.copy()

                if control_df.empty:
                    logger.warning(
                        "Control Dataframe is Empty. Continuing to next Control Component.")

                else:
                    control_result_df = __send_control(
                        api_inputs=api_inputs,
                        df=control_df,
                        installation_id=installation_id,
                        has_priority=True,
                        session_id=uuid.uuid4(),
                        timeout=300,
                        is_send_control=is_send_control
                    )

                if not is_send_control:
                    if control_df.empty:
                        control_result_df['ControlStatus'] = ControlStatus.NoControlRequired.value
                    else:
                        control_result_df['ControlStatus'] = ControlStatus.NotSentToService.value
                    control_result_df = control_result_df.rename(
                        columns={column_with_object_property_id: 'ObjectPropertyId', column_with_value: 'Value'})

                control_result_df['ControlName'] = name
                control_result_df['InstallationId'] = installation_id

                print(control_result_df.head())

                control_result_df = pandas.merge(group, control_result_df[[
                    'ObjectPropertyId', 'Value', 'ControlStatus']], left_on=column_with_object_property_id, right_on='ObjectPropertyId', how='right')

                print(control_result_df.head())

                new_order = ['ControlName', 'InstallationId',
                             'TimestampLocal', 'PivotKey', 'ControlStatus', 'InfoColumns']

                control_result_df['InfoColumns'] = control_result_df.apply(
                    lambda row: {col: row[col] for col in information_columns}, axis=1)

                # Reindex the DataFrame
                control_result_df = control_result_df.reindex(
                    columns=new_order)
                control_result_df.drop(control_result_df.columns.difference(
                    new_order), axis=1, inplace=True)

                control_result_df = control_result_df.rename(
                    columns={'TimestampLocal': 'Timestamp'})

                # Add Empty Column Space here after PivotKey column
                insert_position = control_result_df.columns.get_loc(
                    "PivotKey")
                control_result_df.insert(insert_position + 1, 'Blank', '')

                control_results.append(control_result_df)

            except Exception as e:
                logger.info(
                    f"An unexpected error occurred: {e}")

    _control_components = {}

    return pandas.concat(control_results, ignore_index=True)


@_with_func_attrs(df_required_columns=['ObjectPropertyId', 'Value', 'TTL'])
@_with_func_attrs(df_optional_columns=['DefaultControlValue', 'ControlName', 'ContinueValue'])
def __send_control(api_inputs: ApiInputs, installation_id: Union[uuid.UUID, str], df: pandas.DataFrame, has_priority: bool, session_id: uuid.UUID, is_send_control: bool = True, timeout: int = WS_MQTT_CONNECTION_TIMEOUT):
    """Submit control of sensor(s)

    Required fields are:

    - ObjectPropertyId
    - Value
    - TTL

    Optional fields are:
    - DefaultControlValue : if this column is present, after TTL, the sensor will turn into this value.
    - ControlContinue : if this column is present, this needs to verify if it's the first time controlling this or not.

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    df : pandas.DataFrame
        List of Sensors for control request.
    has_priority : bool
        Flag if dataframe passes contains has_priority column.
    session_id : uuid.UUID., Optional
        Session Id to reuse when communicating with IoT Endpoint and MQTT Broker
    timeout : int, Optional:
        Default value is 30 seconds. Value must be between 1 and max control timeout set in the control variables.
            When value is set to 0 it defaults to max timeout value.
            When value is above max timeout value it defaults to max timeout value.

    Returns
    -------
    tuple
        control_response  = is the list of sensors that were request to be controlled with status labelling if it was successful or not by the MQTTT message broker
    """
    global _control_api_endpoint
    global _control_ws_host
    global _control_ws_port
    global _control_ws_username
    global _control_ws_password
    global _control_ws_max_timeout

    default_control_value_column = 'DefaultControlValue'

    data_frame = df.copy()

    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using the API.")
        return 'Invalid api_inputs.', pandas.DataFrame()

    if not is_valid_uuid(installation_id):
        logger.error("Installation Id is not a valid UUID.")
        return 'Invalid installation_id.', pandas.DataFrame()

    if data_frame.empty:
        logger.error("Dataframe is empty.")
        return 'Empty dataframe.', pandas.DataFrame()

    if timeout < 0:
        logger.error(
            f"Invalid timeout value. Timeout should be between 0 and {_control_ws_max_timeout}. Setting to zero will default to max timeout.")
        return 'Invalid timeout.', pandas.DataFrame()

    if timeout > _control_ws_max_timeout:
        logger.critical(
            f'Timeout is greater than Max Timeout value. Setting timeout to Max Timeout Value instead.')
        timeout = _control_ws_max_timeout

    if timeout == 0:
        timeout = _control_ws_max_timeout

    if not is_valid_uuid(session_id):
        session_id = uuid.uuid4()

    required_columns = getattr(submit_control, 'df_required_columns')
    proposed_columns = data_frame.columns.tolist()

    if not set().issubset(data_frame.columns):
        logger.exception('Missing required column(s): %s', set(
            required_columns).difference(proposed_columns))
        return 'control.submit_control(): dataframe must contain the following columns: ' + ', '.join(
            required_columns), pandas.DataFrame()

    control_cache_key = f"{api_inputs.api_project_id}-submit-control-cache-test"

    control_cache_df = get_control_cache(
        api_inputs=api_inputs, key=control_cache_key, scope_id=api_inputs.api_project_id)

    if control_cache_df.empty:
        logger.error('Cache is empty.')
        control_cache_df = pandas.DataFrame(columns=['ObjectPropertyId'])

    # Check if Input Dataframe sensors is present in the Cache (Dictionary of Records)
    # Normalize casing to lowercase for comparison
    data_frame['NormalizedObjectPropertyId'] = data_frame['ObjectPropertyId'].str.lower()
    control_cache_df['NormalizedObjectPropertyId'] = control_cache_df['ObjectPropertyId'].str.lower()

    # Check if each row's ObjectPropertyId in data_frame is in control_cache_df
    data_frame['ExistsInControlCache'] = data_frame['NormalizedObjectPropertyId'].isin(
        control_cache_df['NormalizedObjectPropertyId'])

    # Drop the normalized columns - only used for checking
    data_frame.drop(columns=['NormalizedObjectPropertyId'], inplace=True)
    control_cache_df.drop(columns=['NormalizedObjectPropertyId'], inplace=True)

    # If Present, check if "ContinueValue" column value is present in Input Dataframe
    if 'ContinueValue' in data_frame.columns:
        data_frame['ContinueValuePresent'] = data_frame['ExistsInControlCache'] & data_frame['ContinueValue'].notnull()
        # Replace values in 'Value' column where 'ContinueValuePresent' is True with the value from 'ContinueValue'
        data_frame.loc[data_frame['ContinueValuePresent'],
                       'Value'] = data_frame['ContinueValue']
    else:
        data_frame['ContinueValuePresent'] = False

    df_matrix = data_frame.copy()

    control_columns_required = ['ObjectPropertyId', 'Value', 'TTL', 'Priority']
    data_frame.drop(data_frame.columns.difference(
        control_columns_required), axis=1, inplace=True)

    # We convert these columns to the required payload property names
    data_frame = data_frame.rename(columns={'ObjectPropertyId': 'id',
                                            'Value': 'v', 'TTL': 'dsecs'})

    if has_priority:
        if not 'Priority' in data_frame:
            logger.error(
                f"has_priority is set to True, but the dataframe does not have the column 'Priority'.")
            return 'Missing Priority column', pandas.DataFrame()
        else:
            data_frame = data_frame.rename(columns={'Priority': 'p'})

    json_payload = {
        "sensors": data_frame.to_dict(orient='records'),
        "email": api_inputs.email_address,
        "userid": api_inputs.user_id,
        "sessionId": str(session_id)
    }

    url = f"{_control_api_endpoint}/api/gateway/{str(installation_id)}/log-control-request"

    headers = api_inputs.api_headers.default

    logger.info("Sending Control Request to IoT API: POST %s", url)
    logger.info("Control Request Session Id: %s", str(session_id))
    logger.info("Control Request for User: %s=%s",
                api_inputs.email_address, api_inputs.user_id)

    if is_send_control:
        response = requests.post(url, json=json_payload, headers=headers)
        response_status = '{} {}'.format(response.status_code, response.reason)
        response_object = json.loads(response.text)

        if response.status_code != 200:
            logger.error("API Call was not successful. Response Status: %s. Reason: %s.",
                         response.status_code, response.reason)
            logger.error(response_object[IOT_RESPONSE_ERROR])
            return response_status, pandas.DataFrame()
        elif len(response.text) == 0:
            logger.error('No data returned for this API call. %s',
                         response.request.url)
            return response_status, pandas.DataFrame()

        if not response_object[IOT_RESPONSE_SUCCESS]:
            logger.error(response_object[IOT_RESPONSE_ERROR])
            return response_object[IOT_RESPONSE_SUCCESS], pandas.DataFrame()

        # Proceeds when the control request is successful
        logger.info('IoT API Control Request is Successful.')

    data_frame = df_matrix.copy()

    if default_control_value_column in data_frame.columns:
        control_columns_required.append(default_control_value_column)

    data_frame = data_frame.rename(columns={'ObjectPropertyId': 'sensorId',
                                            'Value': 'controlValue', 'TTL': 'duration', default_control_value_column: 'defaultControlValue'})

    if has_priority:
        if not 'Priority' in data_frame:
            logger.error(
                f"The dataframe does not have the column 'Priority'.")
        else:
            data_frame = data_frame.rename(columns={'Priority': 'priority'})

    switch_mqtt = SwitchMQTT(host_address=_control_ws_host, host_port=_control_ws_port,
                             username=_control_ws_username, password=_control_ws_password,
                             session_id=session_id, client_id=api_inputs.user_id, email=api_inputs.email_address,
                             project_id=api_inputs.api_project_id, installation_id=str(installation_id))

    def process_paged_request(df, page_size: int = 20):
        paged_results = pandas.DataFrame()
        total_rows = len(df)
        num_pages = (total_rows + page_size - 1) // page_size

        for page_num in range(num_pages):
            start_idx = page_num * page_size
            end_idx = min((page_num + 1) * page_size, total_rows)

            # Get the data for the current page
            page_data = df.iloc[start_idx:end_idx]

            result = send_control(page_data)
            paged_results = pandas.concat([paged_results, result])

        return paged_results

    def send_control(page_data):
        retry_count = 0
        max_retries = 3
        success_results = pandas.DataFrame()
        missing_results = pandas.DataFrame()

        dataframe_to_control = page_data.copy()

        while retry_count < max_retries:
            success_response, missing_response = switch_mqtt.send_control_request(
                sensors=dataframe_to_control.to_dict(orient='records'))

            if not isinstance(success_response, pandas.DataFrame):
                logger.error(success_response)
                retry_count += 1
                time.sleep(1)
                continue

            if not success_response.empty:
                logger.info("Sensors that were successful in control request:")
                logger.info(success_response.to_string(index=False))
                success_results = pandas.concat(
                    [success_results, success_response])

            if not missing_response.empty:
                logger.error(
                    "Sensors that aren't successful in control request.")
                logger.info(missing_response.to_string(index=False))
                missing_results = pandas.concat(
                    [missing_results, missing_response])

            if missing_response.empty:
                break

            # Discount the successful control requests from the ones going for a retry
            if not success_response.empty:
                dataframe_to_control = dataframe_to_control[~dataframe_to_control['sensorId'].isin(
                    success_response['sensorId'])]

            retry_count += 1
            if retry_count < max_retries:
                time.sleep(1)

        if missing_results.empty:
            success_results['status'] = True
            if retry_count > 1:
                success_results['writeStatus'] = 'Resent'
            else:
                success_results['writeStatus'] = 'Complete'
            control_result = success_results.copy()
        else:
            control_result = pandas.merge(page_data, missing_results, left_on='sensorId',
                                          right_on='sensorId', how='left', suffixes=('_df1', '_df2'))

            control_result['status'] = control_result['writeStatus'].isnull()

            columns_to_drop = ['controlValue_df2', 'duration_df2',
                               'priority_df2', 'defaultControlValue_df2']

            # Filter columns that exist in the dataframe
            existing_columns_to_drop = [
                col for col in columns_to_drop if col in control_result.columns]

            if existing_columns_to_drop:
                control_result.drop(
                    existing_columns_to_drop, axis=1, inplace=True)

            control_result['status'] = control_result['status'].fillna(True)

            control_result = control_result.rename(columns={
                'controlValue_df1': 'controlValue',
                'duration_df1': 'duration',
                'priority_df1': 'priority',
                'defaultControlValue_df1': 'defaultControlValue'
            })

        logger.info(control_result)
        return control_result

    if is_send_control:
        is_connected = switch_mqtt.connect(timeout=timeout)

        if not is_connected:
            logger.info("Could not connect to MQTT Broker.")
            return 'Could not connect to MQTT Broker.', pandas.DataFrame()

        control_results = process_paged_request(data_frame)
        switch_mqtt.disconnect()
    else:
        control_results = data_frame.copy()
        control_results['status'] = True
        control_results['writeStatus'] = "Resent"

    control_results = control_results.rename(
        columns={'sensorId': 'ObjectPropertyId', 'status': 'ControlStatus'})
    control_results['ControlStatus'] = control_results['ControlStatus'].apply(
        lambda x: ControlStatus.ControlSuccessful.value if x else ControlStatus.ControlFailed.value)
    control_results.loc[control_results['writeStatus'] ==
                        'Resent', 'ControlStatus'] = ControlStatus.ControlResent.value

    control_result_matrix = control_results.copy()
    control_result_matrix.drop(control_result_matrix.columns.difference(
        ['ObjectPropertyId']), axis=1, inplace=True)

    # Remove rows where ExistsInControlCache is True and ContinueValuePresent is False
    # These are candidate for stopping control / relinquish cache
    df_matrix = df_matrix[~((df_matrix['ExistsInControlCache'] == True) &
                            (df_matrix['ContinueValuePresent'] == False))]
    df_matrix.drop(
        columns=['Value', 'TTL', 'Priority', 'ContinueValue', 'ContinueValuePresent', 'ExistsInControlCache', 'Label', 'ControlName'], inplace=True)

    # Identify sensorId values in control_result_matrix that are not in df_matrix['ObjectPropertyId']
    to_update_in_cache = control_result_matrix[~control_result_matrix['ObjectPropertyId'].isin(
        df_matrix['ObjectPropertyId'])]

    print(to_update_in_cache.head())

    # Add missing rows to df_matrix for cache update
    df_matrix = pandas.concat(
        [df_matrix, to_update_in_cache], ignore_index=True)

    # change to dict of records for caching
    dict_of_records = df_matrix.to_dict(orient='records')
    set_control_cache(api_inputs=api_inputs, key=control_cache_key,
                      scope_id=api_inputs.api_project_id, data=dict_of_records)

    control_results.drop(
        columns=['ContinueValue', 'ContinueValuePresent', 'ExistsInControlCache', 'ControlName'], inplace=True)
    control_results = control_results.rename(
        columns={'controlValue': 'Value', 'duration': 'TTL', 'writeStatus': 'WriteStatus'})

    if has_priority:
        if not 'priority' in control_results:
            logger.error(
                f"The dataframe does not have the column 'Priority'.")
        else:
            control_results = control_results.rename(
                columns={'priority': 'Priority'})

    return control_results


@_with_func_attrs(df_required_columns=['ObjectPropertyId', 'Value', 'TTL'])
@_with_func_attrs(df_optional_columns=['DefaultControlValue'])
def submit_control(api_inputs: ApiInputs, installation_id: Union[uuid.UUID, str], df: pandas.DataFrame, has_priority: bool, session_id: uuid.UUID, timeout: int = WS_MQTT_CONNECTION_TIMEOUT):
    """Submit control of sensor(s)

    Required fields are:

    - ObjectPropertyId
    - Value
    - TTL
    - DefaultControlValue (Optional)

    Parameters
    ----------
    api_inputs : ApiInputs
        Object returned by initialize() function.
    df : pandas.DataFrame
        List of Sensors for control request.
    has_priority : bool
        Flag if dataframe passes contains has_priority column.
    session_id : uuid.UUID., Optional
        Session Id to reuse when communicating with IoT Endpoint and MQTT Broker
    timeout : int, Optional:
        Default value is 30 seconds. Value must be between 1 and max control timeout set in the control variables.
            When value is set to 0 it defaults to max timeout value.
            When value is above max timeout value it defaults to max timeout value.

    Returns
    -------
    tuple
        control_response  = is the list of sensors that were request to be controlled with status labelling if it was successful or not by the MQTTT message broker
    """
    global _control_api_endpoint
    global _control_ws_host
    global _control_ws_port
    global _control_ws_username
    global _control_ws_password
    global _control_ws_max_timeout

    default_control_value_column = 'DefaultControlValue'

    data_frame = df.copy()

    if api_inputs.api_base_url == '' or api_inputs.bearer_token == '':
        logger.error("You must call initialize() before using the API.")
        return 'Invalid api_inputs.', pandas.DataFrame()

    if not is_valid_uuid(installation_id):
        logger.error("Installation Id is not a valid UUID.")
        return 'Invalid installation_id.', pandas.DataFrame()

    if data_frame.empty:
        logger.error("Dataframe is empty.")
        return 'Empty dataframe.', pandas.DataFrame()

    if timeout < 0:
        logger.error(
            f"Invalid timeout value. Timeout should be between 0 and {_control_ws_max_timeout}. Setting to zero will default to max timeout.")
        return 'Invalid timeout.', pandas.DataFrame()

    if timeout > _control_ws_max_timeout:
        logger.critical(
            f'Timeout is greater than Max Timeout value. Setting timeout to Max Timeout Value instead.')
        timeout = _control_ws_max_timeout

    if timeout == 0:
        timeout = _control_ws_max_timeout

    if not is_valid_uuid(session_id):
        session_id = uuid.uuid4()

    required_columns = getattr(submit_control, 'df_required_columns')
    proposed_columns = data_frame.columns.tolist()

    if not set().issubset(data_frame.columns):
        logger.exception('Missing required column(s): %s', set(
            required_columns).difference(proposed_columns))
        return 'control.submit_control(): dataframe must contain the following columns: ' + ', '.join(
            required_columns), pandas.DataFrame()

    control_columns_required = ['ObjectPropertyId', 'Value', 'TTL', 'Priority']
    data_frame.drop(data_frame.columns.difference(
        control_columns_required), axis=1, inplace=True)

    # We convert these columns to the required payload property names
    data_frame = data_frame.rename(columns={'ObjectPropertyId': 'id',
                                            'Value': 'v', 'TTL': 'dsecs'})

    if has_priority:
        if not 'Priority' in data_frame:
            logger.error(
                f"has_priority is set to True, but the dataframe does not have the column 'Priority'.")
            return 'Missing Priority column', pandas.DataFrame()
        else:
            data_frame = data_frame.rename(columns={'Priority': 'p'})

    json_payload = {
        "sensors": data_frame.to_dict(orient='records'),
        "email": api_inputs.email_address,
        "userid": api_inputs.user_id,
        "sessionId": str(session_id)
    }

    url = f"{_control_api_endpoint}/api/gateway/{str(installation_id)}/log-control-request"

    headers = api_inputs.api_headers.default

    logger.info("Sending Control Request to IoT API: POST %s", url)
    logger.info("Control Request Session Id: %s", str(session_id))
    logger.info("Control Request for User: %s=%s",
                api_inputs.email_address, api_inputs.user_id)

    response = requests.post(url, json=json_payload, headers=headers)
    response_status = '{} {}'.format(response.status_code, response.reason)
    response_object = json.loads(response.text)

    if response.status_code != 200:
        logger.error("API Call was not successful. Response Status: %s. Reason: %s.",
                     response.status_code, response.reason)
        logger.error(response_object[IOT_RESPONSE_ERROR])
        return response_status, pandas.DataFrame()
    elif len(response.text) == 0:
        logger.error('No data returned for this API call. %s',
                     response.request.url)
        return response_status, pandas.DataFrame()

    if not response_object[IOT_RESPONSE_SUCCESS]:
        logger.error(response_object[IOT_RESPONSE_ERROR])
        return response_object[IOT_RESPONSE_SUCCESS], pandas.DataFrame()

    # Proceeds when the control request is successful
    logger.info('IoT API Control Request is Successful.')

    data_frame = df.copy()

    if default_control_value_column in data_frame.columns:
        control_columns_required.append(default_control_value_column)

    data_frame = data_frame.rename(columns={'ObjectPropertyId': 'sensorId',
                                            'Value': 'controlValue', 'TTL': 'duration', 'DefaultControlValue': 'defaultControlValue'})

    if has_priority:
        if not 'Priority' in data_frame:
            logger.error(
                f"The dataframe does not have the column 'Priority'.")
        else:
            data_frame = data_frame.rename(columns={'Priority': 'priority'})

    switch_mqtt = SwitchMQTT(host_address=_control_ws_host, host_port=_control_ws_port,
                             username=_control_ws_username, password=_control_ws_password,
                             session_id=session_id, client_id=api_inputs.user_id, email=api_inputs.email_address,
                             project_id=api_inputs.api_project_id, installation_id=str(installation_id))

    is_connected = switch_mqtt.connect(timeout=timeout)

    if not is_connected:
        logger.info("Could not connect to MQTT Broker.")
        return 'Could not connect to MQTT Broker.', pandas.DataFrame()

    def process_paged_request(df, page_size: int = 20):
        paged_results = pandas.DataFrame()
        total_rows = len(df)
        num_pages = (total_rows + page_size - 1) // page_size

        for page_num in range(num_pages):
            start_idx = page_num * page_size
            end_idx = min((page_num + 1) * page_size, total_rows)

            # Get the data for the current page
            page_data = df.iloc[start_idx:end_idx]

            result = send_control(page_data)
            paged_results = pandas.concat([paged_results, result])

        return paged_results

    def send_control(page_data):
        retry_count = 0
        max_retries = 3
        success_results = pandas.DataFrame()
        missing_results = pandas.DataFrame()

        dataframe_to_control = page_data.copy()

        while retry_count < max_retries:
            success_response, missing_response = switch_mqtt.send_control_request(
                sensors=dataframe_to_control.to_dict(orient='records'))

            if not isinstance(success_response, pandas.DataFrame):
                logger.error(success_response)
                retry_count += 1
                time.sleep(1)
                continue

            if not success_response.empty:
                logger.info("Sensors that were successful in control request:")
                logger.info(success_response.to_string(index=False))
                success_results = pandas.concat(
                    [success_results, success_response])

            if not missing_response.empty:
                logger.error(
                    "Sensors that aren't successful in control request.")
                logger.info(missing_response.to_string(index=False))
                missing_results = pandas.concat(
                    [missing_results, missing_response])

            if missing_response.empty:
                break

            # Discount the successful control requests from the ones going for a retry
            if not success_response.empty:
                dataframe_to_control = dataframe_to_control[~dataframe_to_control['sensorId'].isin(
                    success_response['sensorId'])]

            retry_count += 1
            if retry_count < max_retries:
                time.sleep(1)

        if missing_results.empty:
            success_results['status'] = True
            success_results['writeStatus'] = 'Complete'
            control_result = success_results.copy()
        else:
            control_result = pandas.merge(page_data, missing_results, left_on='sensorId',
                                          right_on='sensorId', how='left', suffixes=('_df1', '_df2'))

            control_result['status'] = control_result['writeStatus'].isnull()

            columns_to_drop = ['controlValue_df2', 'duration_df2',
                               'priority_df2', 'defaultControlValue_df2']

            # Filter columns that exist in the dataframe
            existing_columns_to_drop = [
                col for col in columns_to_drop if col in control_result.columns]

            if existing_columns_to_drop:
                control_result.drop(
                    existing_columns_to_drop, axis=1, inplace=True)

            control_result['status'] = control_result['status'].fillna(True)

            control_result = control_result.rename(columns={
                'controlValue_df1': 'controlValue',
                'duration_df1': 'duration',
                'priority_df1': 'priority',
                'defaultControlValue_df1': 'defaultControlValue'
            })

        logger.info(control_result)
        return control_result

    control_results = process_paged_request(data_frame)

    switch_mqtt.disconnect()

    return control_results


def get_control_cache(api_inputs: ApiInputs, key: str, scope_id: str) -> pandas.DataFrame:
    try:
        control_cache_res = get_cache(
            api_inputs=api_inputs, scope="Portfolio", key=key, scope_id=scope_id)

        if control_cache_res['success'] == True:
            cache_data = json.loads(control_cache_res['data'])
            df_from_records = pandas.DataFrame.from_records(
                cache_data)
            return df_from_records
        return pandas.DataFrame()
    except Exception as e:
        logger.error(
            f"An unexpected error occurred in getting Control cache: {e}")
        return pandas.DataFrame()


def set_control_cache(api_inputs: ApiInputs, key: str, scope_id: str, data: any):
    try:
        return set_cache(api_inputs=api_inputs, scope="Portfolio", key=key, val=data, scope_id=scope_id)
    except Exception as e:
        logger.error(
            f"An unexpected error occurred in setting Control cache: {e}")
        return pandas.DataFrame()


def add_control_component(name: str, column_with_object_installation_id: str, column_with_object_property_id: str, column_with_label: str, column_with_value: str, column_with_continue: str = None, column_with_default_value: str = None, timeoutMinutes: int = 0, priority: int = 8):

    global _control_components

    # Validate required parameters
    if not name:
        raise ValueError("The 'name' parameter cannot be None or empty.")
    if not column_with_object_installation_id:
        raise ValueError(
            "The 'column_with_object_installation_id' parameter cannot be None or empty.")
    if not column_with_object_property_id:
        raise ValueError(
            "The 'column_with_object_property_id' parameter cannot be None or empty.")
    if not column_with_label:
        raise ValueError(
            "The 'column_with_label' parameter cannot be None or empty.")
    if not column_with_value:
        raise ValueError(
            "The 'column_with_value' parameter cannot be None or empty.")

    # Optional parameters can be None, so only check if they are not None and empty
    if column_with_continue is not None and column_with_continue == "":
        raise ValueError(
            "The 'column_with_continue' parameter cannot be an empty string.")
    if column_with_default_value is not None and column_with_default_value == "":
        raise ValueError(
            "The 'column_with_default_value' parameter cannot be an empty string.")

    # Validate timeoutMinutes and priority
    if not isinstance(timeoutMinutes, int) or timeoutMinutes < 0:
        raise ValueError(
            "The 'timeoutMinutes' parameter must be a non-negative integer.")
    if not isinstance(priority, int) or priority < 0:
        raise ValueError(
            "The 'priority' parameter must be a non-negative integer.")

    _control_components[name] = (
        column_with_object_installation_id,
        column_with_object_property_id,
        column_with_label,
        column_with_value,
        column_with_continue,
        column_with_default_value,
        timeoutMinutes,
        priority)
