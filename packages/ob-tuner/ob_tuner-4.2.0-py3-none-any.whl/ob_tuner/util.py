import datetime
import json
import os
import pathlib
import time
from logging.handlers import RotatingFileHandler
import boto3
import faker
import gradio as gr
import logging
from io import StringIO

import requests
from dotenv import load_dotenv, find_dotenv
from importlib.metadata import version
from boto3.dynamodb.conditions import Attr
# Use find_dotenv to locate the .env file
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path)

os.environ["INFRA_STACK_NAME"] = os.environ.get("INFRA_STACK_NAME", "LOCAL")
# Unfortunate... fix later
from openbrain.orm.model_client import Client

import openbrain.orm
import openbrain.util
from openbrain.orm.model_agent_config import AgentConfig
from openbrain.orm.model_common_base import InMemoryDb
from openbrain.util import config, Defaults
from openbrain.tools import Toolbox


# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Add a rotating log handler
formatter = logging.Formatter('%(filename)-20s:%(lineno)-4d %(levelname)-8s %(message)s')

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Add a stringio handler
log_stream = StringIO()
string_handler = logging.StreamHandler(log_stream)
string_handler.setLevel(logging.DEBUG)
string_handler.setFormatter(formatter)
logger.addHandler(string_handler)
ADMIN_USER = os.environ.get("ADMIN_USER")
if os.environ.get("OB_MODE", "LOCAL") == "LOCAL" and ADMIN_USER:
    logger.info(f"Creating admin user {ADMIN_USER}")
    try:
        ADMIN_LEADMO_LOCATION_ID = os.getenv("ADMIN_LEADMO_LOCATION_ID")
        ADMIN_LEADMO_API_KEY = os.getenv("ADMIN_LEADMO_API_KEY")
        ADMIN_LEADMO_CALENDAR_ID = os.getenv("ADMIN_LEADMO_CALENDAR_ID")
        admin_user = Client(email=ADMIN_USER, leadmo_api_key=ADMIN_LEADMO_API_KEY, leadmo_location_id=ADMIN_LEADMO_LOCATION_ID, leadmo_calendar_id=ADMIN_LEADMO_CALENDAR_ID)
        admin_user.save()
        admin_default_agent_config = AgentConfig(client_id=ADMIN_USER, profile_name=Defaults.DEFAULT_PROFILE_NAME.value)
        admin_default_agent_config.save()
    except Exception as e:
        admin_user = Client(email=ADMIN_USER)
        admin_user.save()
        logger.info(f"Created admin user {ADMIN_USER}")

INFRA_STACK_NAME = os.environ.get("INFRA_STACK_NAME")
OB_MODE = config.OB_MODE
CHAT_ENDPOINT = os.environ.get("OB_API_URL", "") + "/chat"
DEFAULT_ORIGIN = os.environ.get("DEFAULT_ORIGIN", "https://localhost:5173")
OB_PROVIDER_API_KEY = os.environ.get("OB_PROVIDER_API_KEY", "")
DEFAULT_CLIENT_ID: str = openbrain.util.Defaults.DEFAULT_CLIENT_ID.value
DEFAULT_PROFILE_NAME = Defaults.DEFAULT_PROFILE_NAME.value
PORTAL_URL = os.getenv("PORTAL_URL")
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
# CALLBACK_URL = os.getenv("CALLBACK_URL")
DEPLOYMENT_URL = os.getenv("DEPLOYMENT_URL")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GUEST_CLIENT_ID = "guest@openbra.in"
discovered_tools = Toolbox.discovered_tools
model_agent_config = openbrain.orm.model_agent_config
OB_TUNER_VERSION = version("ob-tuner")
CUSTOMER_NAME = os.getenv("CUSTOMER_NAME")


NOAUTH_DEMO_PAGE_STR = os.getenv("NOAUTH_DEMO_PAGE", "False")
LEADMO_INTEGRATION_STR = os.getenv("LEADMO_INTEGRATION", "False")
LLS_INTEGRATION_STR = os.getenv("LLS_INTEGRATION", "False")
NOAUTH_DEMO_PAGE = NOAUTH_DEMO_PAGE_STR.casefold() == "true"
LEADMO_INTEGRATION = LEADMO_INTEGRATION_STR.casefold() == "true"
LLS_INTEGRATION = LLS_INTEGRATION_STR.casefold() == "true"

logger.info(f"************************************ GRADIO CONFIG ************************************")
logger.info(f"DEFAULT_ORIGIN: {DEFAULT_ORIGIN}")
logger.info("OB_API_URL: " + os.environ.get("OB_API_URL", ""))
logger.info(f"({type(NOAUTH_DEMO_PAGE)}): {NOAUTH_DEMO_PAGE=}")
logger.info(f"({type(LEADMO_INTEGRATION)}): {LEADMO_INTEGRATION=}")
logger.info(f"({type(LLS_INTEGRATION)}): {LLS_INTEGRATION=}")
logger.info(f"{CUSTOMER_NAME=}")
logger.info(f"{LEADMO_INTEGRATION=}")
logger.info(f"{NOAUTH_DEMO_PAGE=}")
logger.info(f"{LLS_INTEGRATION=}")
logger.info(f"{OB_TUNER_VERSION=}")

logger.info(f"************************************ AUTH ************************************")
logger.info(f'COGNITO_DOMAIN: {COGNITO_DOMAIN}')
logger.info(f'CLIENT_ID: {CLIENT_ID}')
# logger.info(f'CALLBACK_URL: {CALLBACK_URL}')
logger.info(f'{PORTAL_URL=}')
logger.info(f'DEPLOYMENT_URL: {DEPLOYMENT_URL}')
logger.info("DEFAULT_ORIGIN: " + os.environ.get("DEFAULT_ORIGIN", "https://localhost:5173"))

logger.info(f"************************************ OPENBRAIN CONFIG ************************************")
logger.info(f"OB_MODE: {OB_MODE}")
logger.info(f"SESSION_TABLE_NAME: {config.SESSION_TABLE_NAME}")
logger.info(f"AGENT_CONFIG_TABLE_NAME: {config.AGENT_CONFIG_TABLE_NAME}")
logger.info(f"ACTION_TABLE_NAME: {config.ACTION_TABLE_NAME}")
logger.info(f"{INFRA_STACK_NAME=}")

logger.info(f"************************************ SECRETS ************************************")
OBFUSCATED_CLIENT_SECRET = CLIENT_SECRET[:2] + "*" * (len(CLIENT_SECRET) - 2)
OBFUSCATED_OB_PROVIDER_API_KEY = os.environ.get("GRADIO_OB_PROVIDER_API_KEY", "")[:2] + "*" * (len(os.environ.get("GRADIO_OB_PROVIDER_API_KEY", "")) - 2)
logger.info(f'CLIENT_SECRET: {OBFUSCATED_CLIENT_SECRET}')
logger.info("OB_PROVIDER_API_KEY: " + OBFUSCATED_OB_PROVIDER_API_KEY)

string_handler.flush()
tool_names = [tool.name for tool in Toolbox.discovered_tools if not tool.name.startswith("leadmo_")]
leadmo_tool_names = [tool.name for tool in Toolbox.discovered_tools if tool.name.startswith("leadmo_")]

tool_names.sort()
leadmo_tool_names.sort()
TOOL_NAMES = tool_names + leadmo_tool_names if LEADMO_INTEGRATION else tool_names
logger.info(f"Tool names: {TOOL_NAMES}")

REGISTERED_CLIENT_IDS = {
    "WoxomAI": [DEFAULT_CLIENT_ID, "woxom", "leadmo"],
    "OpenBra.in": [DEFAULT_CLIENT_ID, 'openbrain'],
    "OBTest": [DEFAULT_CLIENT_ID, 'openbrain', 'woxom', 'leadmo'],
}
REGISTERED_THEMES = {
    "WoxomAI": ["light", "dark"],
    "OpenBra.in": ["light", "dark"],
    "OBTest": ["light", "dark"],
}



def get_debug_text(_debug_text=None) -> str:
    try:
        ret = log_stream.getvalue()
    except Exception as e:
        ret = e.__str__()

    if _debug_text:
        _debug_text = ret

    return ret


def get_aws_xray_trace_summaries(id=None):
    """Get x-ray logs from AWS"""
    client = boto3.client("xray")
    this_year = datetime.datetime.now().year
    this_month = datetime.datetime.now().month
    this_day = datetime.datetime.now().day
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).day

    if id:
        response = client.get_trace_summaries(
            StartTime=datetime.datetime(this_year, this_month, yesterday),
            EndTime=datetime.datetime(this_year, this_month, this_day),
            Sampling=False,
            FilterExpression=f"traceId = {id}",
        )
    else:
        response = client.get_trace_summaries(
            StartTime=datetime.datetime(this_year, this_month, yesterday),
            EndTime=datetime.datetime(this_year, this_month, this_day),
            Sampling=False,
        )

    return response


def is_settings_set():
    return True


def get_tool_description(tool_name):
    for tool in Toolbox.discovered_tools:
        if tool_name == tool.name:
            tool_instance = tool.tool()
            tool_description = tool_instance.description
            fields = tool_instance.args_schema.model_fields
            args_string = ""
            if not fields:
                args_string = "'No args'"
            for field in fields:
                field_str = fields[field].__str__()
                args_string += f"{field}: {field_str}\n"
            tool_description = f"""#### Description
{tool_description}

#### Args
```python
{args_string}
```"""
            return tool_description


def get_available_tool_descriptions():
    tool_descriptions = []

    for tool in Toolbox.discovered_tools:
        tool_name = tool.name
        tool_instance = tool.tool()
        tool_description = tool_instance.description
        fields = tool_instance.args_schema.model_fields
        args_string = ""
        if not fields:
            args_string = "'No args'"
        for field in fields:
            field_str = fields[field].__str__()
            args_string += f"{field}: {field_str}\n"
        tool_description = f"""
## Tool: {tool_name}

#### Description
{tool_description}

#### Args
```python
{args_string}
```
---"""

        tool_descriptions.append(tool_description)

    tool_descriptions_string = "\n".join(tool_descriptions)
    return tool_descriptions_string


def get_available_profile_names(_client_id) -> list:
    logger.info(f"Getting available profile names for {_client_id}")
    # logger.warning("get_available_profile_names() is not implemented")
    # Get AgentConfig table

    if OB_MODE == Defaults.OB_MODE_LOCAL.value:
        try:
            logger.info(f"Checking InMemoryDb for available profile names...")
            lst = list(InMemoryDb.instance[config.AGENT_CONFIG_TABLE_NAME][_client_id].keys())
            return lst
        except Exception:
            logger.warning(f"Not found, initializing default profile name...")
            _client_id = _client_id or GUEST_CLIENT_ID
            default_config = AgentConfig(client_id=_client_id, profile_name=DEFAULT_PROFILE_NAME)
            logger.info(f"Saving default profile name: {default_config}")
            default_config.save()
            logger.info(f"Saved default profile name: {default_config}")
            lst = list(InMemoryDb.instance['agent_config_table'][_client_id].keys())
            logger.info(f"Available profile names: {lst}")
            return lst
    else:
        table = boto3.resource("dynamodb").Table(config.AGENT_CONFIG_TABLE_NAME)
        # get all items in the table
        try:
            items = table.scan()["Items"]
            available_profile_names = [item["profile_name"] for item in items if item["client_id"] == _client_id]
            # response = table.query(
            #     KeyConditionExpression=boto3.dynamodb.conditions.Key('client_id').eq(_client_id)
            # )
            # available_profile_names = [profile["profile_name"] for profile in response]

        except Exception as e:
            logger.error(f"Error getting available profile names: {e}")
            available_profile_names = []

        return available_profile_names


def update_available_profile_names(client_id):
    if not client_id:
        return gr.Dropdown(choices=[DEFAULT_PROFILE_NAME], value=DEFAULT_PROFILE_NAME)

    available_profile_names = get_available_profile_names(client_id)
    # available_profile_names = [profile["profile_name"] for profile in available_profiles]
    try:
        selected_profile = DEFAULT_PROFILE_NAME
    except IndexError:
        default_config = AgentConfig(client_id=client_id, profile_name=DEFAULT_PROFILE_NAME)
        default_config.save()
        selected_profile = DEFAULT_PROFILE_NAME
        available_profile_names = [DEFAULT_PROFILE_NAME]
    return gr.Dropdown(choices=available_profile_names, value=selected_profile)


def get_llm_choices(llm_types=None):
    """Get the available LLM choices based on the selected types"""
    if not llm_types:
        llm_types = ["function"]
    available_llms = []
    known_llm_types = openbrain.orm.model_agent_config.EXECUTOR_MODEL_TYPES
    for llm_type in llm_types:
        if llm_type == "function":
            available_llms += openbrain.orm.model_agent_config.FUNCTION_LANGUAGE_MODELS
        elif llm_type == "chat":
            available_llms += openbrain.orm.model_agent_config.CHAT_LANGUAGE_MODELS
        elif llm_type == "completion":
            available_llms += openbrain.orm.model_agent_config.COMPLETION_LANGUAGE_MODELS
        else:
            logger.error(f"Unknown LLM type: {llm_type}, must be one of {known_llm_types}")
            continue
    return gr.Dropdown(choices=available_llms)


def greet(request: gr.Request):
    try:
        return f"Welcome to Gradio, {request.username}"
    except Exception:
        return "OH NO!"


def initialize_username(request: gr.Request):
    _username = request.username or GUEST_CLIENT_ID
    logger.info(f"Initializing username: {_username}")
    registered_client_ids = get_registered_client_ids()
    # Copying the dict so we don't update it
    registered_client_ids_copy = registered_client_ids.copy()
    registered_client_ids_copy.append(_username)
    client_id_dropdown = gr.Dropdown(choices=registered_client_ids_copy, value=_username)

    try:
        AgentConfig.get(client_id=_username, profile_name=DEFAULT_PROFILE_NAME)
    except Exception as e:
        logger.info(f"No default AgentConfig found for {_username}, creating default agent config for {_username}")
        new_default_agent_config = AgentConfig(client_id=_username, profile_name=DEFAULT_PROFILE_NAME)
        new_default_agent_config.save()
    return [_username, client_id_dropdown]
    # return [_username]

def update_client_id(_username, _session_state):
    _username = _session_state["username"]
    _username_from_session_state = _session_state["username"]

    if _username != _username_from_session_state:
        _session_state["username"] = _username
        logger.info(f"Updating session state (MISMATCH): {_username=}")

    logger.info(f"Updating client_id: {_username=}")
    logger.info(f"Updating client_id: {DEFAULT_CLIENT_ID=}")
    registered_client_ids = get_registered_client_ids()
    registered_client_ids_copy = registered_client_ids.copy()
    registered_client_ids_copy.append(_username)

    return gr.Dropdown(choices=registered_client_ids_copy, value=_username)

# def get_session_username(_session_state=None):
#     username = _session_state["username"]
#     _choices = [DEFAULT_CLIENT_ID, username]
#     return gr.Dropdown(choices=_choices, value=username)


def get_help_text() -> str:
    current_dir = pathlib.Path(__file__).parent
    help_text_path = current_dir / "resources" / "help_text.md"
    with open(help_text_path, "r", encoding="utf8") as file:
        # Read line in UTF-8 format
        help_text = file.readlines()
    return ''.join(help_text)

def get_registered_client_ids(customer_name=CUSTOMER_NAME):
    registered_client_ids = REGISTERED_CLIENT_IDS.get(customer_name, [DEFAULT_CLIENT_ID])
    return registered_client_ids








# EXAMPLE_CONTEXT = """
# {
#     "locationId": "LEADMOMENTUMLOCATIONID",
#     "calendarId": "LEADMOMENTUMCALENDARID",
#     "contactId": "CONTACTID",
#     "random_word": "spatula",
#     "firstName": "Cary",
#     "lastName": "Nutzington",
#     "name": "Cary Nutzington",
#     "dateOfBirth": "1970-04-01",
#     "phone": "+16198675309",
#     "email": "example@email.com",
#     "address1": "1234 5th St N",
#     "city": "San Diego",
#     "state": "CA",
#     "country": "US",
#     "postalCode": "92108",
#     "companyName": "Augmenting Integrations",
#     "website": "openbra.in",
#     "medications": "tylonol"
# }
# """.strip()

EXAMPLE_CONTEXT = {
    "locationId": "LEADMOMENTUMLOCATIONID",
    "calendarId": "LEADMOMENTUMCALENDARID",
    "contactId": "CONTACTID",
    "random_word": "spatula",
}
def set_client_id(_username):
    registered_client_ids = get_registered_client_ids()
    # Copying the dict so we don't update it
    registered_client_ids_copy = registered_client_ids.copy()
    registered_client_ids_copy.append(_username)
    client_id = gr.Dropdown(
        label="Client ID",
        filterable=True,
        info="Develop your own AI agents or use a community agent.",
        choices=registered_client_ids_copy,
        value=_username,
        elem_id="client_id",
        elem_classes=["agent_config"],
    )

    return client_id


def fetch_user_from_leadmo(context, username, leadmo_api_key, leadmo_location_id, leadmo_calendar_id, first_name, last_name, date_of_birth, phone, address1, address2, city, state, country, postal_code, website):
    """Fetch user from Lead Momentum. If that fails, create a new user."""
    user = Client.get(email=username)

    try:
        leadmo_api_key = user.leadmo_api_key
    except Exception as e:
        gr.Error(f"Please save your Lead Momentum Location ID and API key to your profile.")
        return context

    # First try to fetch with the phone number, and if that fails, try with the email address
    LEADMO_API_V1_CONTACTS_URL = 'https://rest.gohighlevel.com/v1/contacts/lookup'

    url_encoded_phone = phone.replace("+", "%2B")
    url_encoded_email = username.replace("@", "%40")

    phone_url = LEADMO_API_V1_CONTACTS_URL + f'?phone={url_encoded_phone}'
    email_url = LEADMO_API_V1_CONTACTS_URL + f'?email={url_encoded_email}'
    response = None

    headers = {
        "Content-Type": "application/json",
        "Origin": DEFAULT_ORIGIN,
        "Authorization": f'Bearer {leadmo_api_key}'
    }
    response = requests.get(url=phone_url, headers=headers)
    if not (200 <= response.status_code < 300):
        logger.error(f"Failed to fetch user from Lead Momentum with phone number.")
        response = None

    if not response:
        response = requests.get(url=email_url, headers=headers)
    if not (200 <= response.status_code < 300):
        logger.error(f"Failed to fetch user from Lead Momentum with email address.")
        response = None

    if not response:
    # Create a contact
        url = LEADMO_API_V1_CONTACTS_URL
        headers = {
            "Content-Type": "application/json",
            "Origin": DEFAULT_ORIGIN,
            "Authorization ": f'Bearer {leadmo_api_key}'
        }

        data = {
            "email": username,
            "phone": phone,
            "firstName": first_name,
            "lastName": last_name,
            "name": f"{first_name} {last_name}",
            "dateOfBirth": date_of_birth,
            "address1": address1,
            "city": city,
            "state": state,
            "country": country,
            "postalCode": postal_code,
            "companyName": "Augmenting Integrations",
            "website": website,
            "tags": ["woxom_ai"]
        }

        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        logger.info(f"Successfully created user in Lead Momentum.")

    if not (200 <= response.status_code < 300):
        logger.error(f"Failed to create user in Lead Momentum.")
        return context


    context = response.json()["contacts"][0]
    context = {
        "locationId": leadmo_location_id,
        "calendarId": leadmo_calendar_id,
        "contactId": context.get("id", ""),
        "firstName": context.get("firstName", ""),
        "lastName": context.get("lastName", ""),
        "name": context.get("name", ""),
        "dateOfBirth": context.get("dateOfBirth", ""),
        "phone": context.get("phone", ""),
        "email": context.get("email", ""),
        "address1": context.get("address1", ""),
        "city": context.get("city", ""),
        "state": context.get("state", ""),
        "country": context.get("country", ""),
        "postalCode": context.get("postalCode", ""),
        "companyName": context.get("companyName", ""),
        "website": context.get("website", ""),
    }
    return context    # context2, leadmo_contact_id_phone, leadmo_location_id, lls_api_key


# username.change(fill_context, inputs=[context, username], outputs=user_leadmo_details + user_personal_details)
def fill_context(username, leadmo_api_key, leadmo_location_id, leadmo_calendar_id, first_name, last_name, date_of_birth, phone, address1, address2, city, state, country, postal_code, website):
    """Fill the context with the user's details from Lead Momentum"""
    random_word = faker.Faker().word()
    context = {
        "locationId": leadmo_location_id,
        "calendarId": leadmo_calendar_id,
        "contactId": "",
        "firstName": first_name,
        "lastName": last_name,
        "name": f"{first_name} {last_name}",
        "dateOfBirth": date_of_birth,
        "phone": phone,
        "email": username,
        "address1": address1,
        "address2": address2,
        "city": city,
        "state": state,
        "country": country,
        "postalCode": postal_code,
        "website": website,
        "random_word": random_word
    }
    return context

def fill_context_from_username(username):
    try:
        user = Client.get(email=username)
        context = {
            "locationId": user.leadmo_location_id,
            "calendarId": user.leadmo_calendar_id,
            "contactId": "",
            "firstName": user.first_name,
            "lastName": user.last_name,
            "name": f"{user.first_name} {user.last_name}",
            "dateOfBirth": user.date_of_birth,
            "phone": user.phone,
            "email": username,
            "address1": user.address1,
            "address2": user.address2,
            "city": user.city,
            "state": user.state,
            "country": user.country,
            "postalCode": user.postal_code,
            "website": user.website,
        }
    except Exception as e:
        logger.warning(e)
        context = {
            "locationId": "UNKNOWN",
            "email": username,
        }
    return context


def alert_on_actions(_session_state):
    """Alert on actions"""
    for i in range(3):
        time.sleep(4)
        logger.info(f"Checking for actions({i})...")

        try:
            _session_id = _session_state["session_id"]
            logger.info("Checking for actions: Found session_id")
        except TypeError:
            logger.warning("No session ID found")

        try:
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table(config.ACTION_TABLE_NAME)
            response = table.scan(
                FilterExpression=Attr('session_id').eq(_session_id)
            )
            logger.info(f"Checking for actions: {_session_id}")

            ret: dict = response.get("Items", {})
            logger.info(f"found ({len(ret)}) actions")
            for item in ret:
                event = item.get("event", "")
                response = item.get("response", "")
                logger.info(f"Event: {event}")
                logger.info(f"Response: {response}")
                if item["action_id"] in _session_state.get("events"):
                    continue
                _session_state.get("events").append(item["action_id"])
                gr.Info(f"Event: {event}\nResponse: {response}")
        except Exception as e:
            logger.error(f"Error checking for actions: {e}")
            pass

    return _session_state

