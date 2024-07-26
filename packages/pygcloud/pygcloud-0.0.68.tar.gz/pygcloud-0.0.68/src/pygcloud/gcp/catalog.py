"""
Catalog facility for the supported GCP services

@author: jldupont
"""

from typing import List
from functools import cache
from pygcloud.gcp.services import *  # NOQA
from pygcloud.gcp.models import ServiceDescription
from pygcloud.models import ServiceNode, GCPService


@cache
def map():
    return {classe.__name__: classe for classe in ServiceNode.__all_classes__}


def lookup(class_name: str):
    return map().get(class_name, None)


@cache
def get_listable_services():
    return [classe for classe in ServiceNode.__all_classes__ if classe.LISTING_CAPABLE]


def get_service_classes_from_services_list(
    liste: List[ServiceDescription],
) -> List[GCPService]:
    """
    From the list of enabled services in the target project,
    make up list of GCPService classes
    """
    services: List[GCPService] = get_listable_services()

    apis: List[str] = []
    item: ServiceDescription

    for item in liste:
        apis.append(item.api)

    enabled: List[GCPService] = []

    for service in services:
        if service.DEPENDS_ON_API in apis:
            enabled.append(service)

    return enabled
