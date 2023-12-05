import kopf
import logging
from utils import initialize_kube, mysql_client_from_env

initialize_kube()
mysql_client = mysql_client_from_env()


@kopf.on.create("demo.com", "v1", "crd-op-writer")
def create_fn(spec, **kwargs):
    try:
        resource_namespace = kwargs["body"]["metadata"]["namespace"]
        resource_name = kwargs["body"]["metadata"]["name"]
        primary_id = f"{resource_namespace}/{resource_name}"

        table, name, age, country = (
            spec["table"],
            spec["name"],
            spec["age"],
            spec["country"],
        )

        mysql_client.insert_row(table, primary_id, name, age, country)

        message = (
            f"Successfully wrote data corresponding to id: {primary_id}, "
            f"name: {name}, age: {age}, country: {country}"
        )
        logging.info(message)
        return message
    except Exception as e:
        logging.error(f"Error during creation: {e}")
        return f"Error during creation: {e}"


@kopf.on.delete("demo.com", "v1", "crd-op-writer")
def delete_fn(spec, **kwargs):
    try:
        resource_namespace = kwargs["body"]["metadata"]["namespace"]
        resource_name = kwargs["body"]["metadata"]["name"]
        primary_id = f"{resource_namespace}/{resource_name}"
        table = spec["table"]

        if mysql_client.delete_row(table, primary_id):
            message = f"Successfully delete data corresponding to id: {primary_id}"
            logging.info(message)
        else:
            message = f"Failed delete data corresponding to id: {primary_id}"
            logging.error(message)

        return message
    except Exception as e:
        logging.error(f"Error during deletion: {e}")
        return f"Error during deletion: {e}"
