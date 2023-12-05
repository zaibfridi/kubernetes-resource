from kubernetes import config
from clients.mysql import MysqlClient
import os


def mysql_client_from_env():
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")

    client = MysqlClient(
        db=MYSQL_DB, username=MYSQL_USERNAME, password=MYSQL_PASSWORD, host=MYSQL_HOST
    )
    client.connect_if_not_connected()
    return client


def initialize_kube():
    DEV = os.getenv("DEV")
    if DEV:
        print("Loading from local kube config")
        home = os.path.expanduser("~")
        kube_config_path = os.getenv("KUBE_CONFIG", home + "/.kube/config")
        config.load_kube_config(config_file=kube_config_path)
    else:
        print("Loading In-cluster config")
        config.load_incluster_config()
