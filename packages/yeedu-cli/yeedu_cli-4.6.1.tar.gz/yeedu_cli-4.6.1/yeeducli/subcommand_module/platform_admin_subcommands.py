from yeeducli.openapi.iam.platform_admin import PlatformAdmin
from yeeducli.utility.json_utils import *
from yeeducli.utility.logger_utils import Logger
import sys
import json

logger = Logger.get_logger(__name__, True)


# Platform Admin
# Tenant
def create_tenant(args):
    try:
        trim_json_data = trim_namespace_json(args)
        json_data = change_output(remove_output(args))

        response_json, status_code = PlatformAdmin.add_tenant(
            json_data
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def list_tenants(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = PlatformAdmin.list_tenants(
            json_data.get('page_number'),
            json_data.get('limit')
        )

        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def get_tenant(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = PlatformAdmin.get_tenant_by_id_or_name(
            json_data.get('tenant_id'),
            json_data.get('tenant_name')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def delete_tenant(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))

        response_json, status_code = PlatformAdmin.delete_tenant_by_id_or_name(
            trim_json_data.get('tenant_id'),
            trim_json_data.get('tenant_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def edit_tenant(args):
    try:
        trim_json_data = change_output(trim_namespace_json(args))
        json_data = process_null_values(remove_output(args))

        if json_data.get("tenant_id"):
            del json_data["tenant_id"]
        if json_data.get("tenant_name"):
            del json_data["tenant_name"]

        response_json, status_code = PlatformAdmin.edit_tenant_by_id_or_name(
            json.dumps(json_data),
            trim_json_data.get('tenant_id'),
            trim_json_data.get('tenant_name')
        )
        confirm_output(response_json, status_code, trim_json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


def search_tenants(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = PlatformAdmin.search_tenants(
            json_data.get('tenant_name'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)


# List User Tenants
def list_user_tenants(args):
    try:
        json_data = change_output(trim_namespace_json(args))

        response_json, status_code = PlatformAdmin.list_user_tenants(
            json_data.get('user_id'),
            json_data.get('page_number'),
            json_data.get('limit')
        )
        confirm_output(response_json, status_code, json_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(-1)
