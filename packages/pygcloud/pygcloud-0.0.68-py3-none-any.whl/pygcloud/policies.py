"""
@author: jldupont
"""
from pygcloud.models import Policy


class PolicyServiceAccount(Policy):
    """
    Services should have a non-default Service Account
    """


class PolicyProjectLevelBindings(Policy):
    """
    Prohibit the usage of IAM bindings from outside
    of the service's project
    """


class PolicyIngress(Policy):
    """
    A service
    """
