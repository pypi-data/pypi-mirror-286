"""
IAM related services

@author: jldupont
"""

import logging
from typing import Union
from pygcloud.models import GCPServiceSingletonImmutable, Result
from pygcloud.gcp.parsers import ProjectIAMBindings, IAMBinding
from pygcloud.gcp.models import ServiceAccountSpec


class ServiceAccountIAM(GCPServiceSingletonImmutable):
    """
    Add role to Service Account
    """

    LISTING_CAPABLE = False
    DEPENDS_ON_API = "iamcredentials.googleapis.com"
    REQUIRES_DESCRIBE_BEFORE_CREATE = True

    def __init__(self, target_binding: IAMBinding, project_id: str):
        """
        name: str = email of service account
                    (without the namespace prefix 'serviceAccount')
        """
        assert isinstance(target_binding, IAMBinding)
        assert isinstance(project_id, str)

        super().__init__(name=target_binding.email, ns="sa")
        self._project_id = project_id
        self._target_binding = target_binding
        self._bindings_obj = None

    @property
    def spec(self) -> ProjectIAMBindings:
        return self._bindings_obj

    @property
    def bindings(self) -> Union[ProjectIAMBindings, None]:
        return self._bindings_obj

    def params_describe(self):
        return ["projects", "get-iam-policy", self._project_id, "--format", "json"]

    def after_describe(self, result: Result) -> Result:
        """
        Cases:
        1. Service Account does not exist ==> nothing we can do
        2. Service Account exists with required role ==> nothing to do
        3. Service Account exists but missing required role ==> add
        """
        if not result.success:
            raise Exception(
                "Cannot access IAM bindings " f"for project: {result.message}"
            )

        try:
            self._bindings_obj = ProjectIAMBindings(result.message)

        except Exception as e:
            logging.error(e)
            raise Exception("Could not parse bindings from: " f"{result.message}")

        binding_existence = self._bindings_obj.check_for_target_binding(
            self._target_binding
        )

        self.already_exists = binding_existence

        if self.already_exists:
            ns = self._target_binding.ns
            email = self._target_binding.email
            role = self._target_binding.role

            logging.debug(
                "ServiceAccountIAM binding already exists: "
                f"{ns}:{email} for role '{role}'"
            )

        return result

    def params_create(self):
        """
        If there is already a binding for (name, role),
        then we just need to skip
        """
        ns = self._target_binding.ns
        email = self._target_binding.email
        role = self._target_binding.role

        return [
            "projects",
            "add-iam-policy-binding",
            self._project_id,
            "--member",
            f"{ns}:{email}",
            "--role",
            role,
            "--format",
            "json",
        ]


class ServiceAccount(GCPServiceSingletonImmutable):
    """
    https://cloud.google.com/sdk/gcloud/reference/iam/service-accounts
    """
    SPEC_CLASS = ServiceAccountSpec
    LISTING_CAPABLE = True
    DEPENDS_ON_API = "iam.googleapis.com"
    GROUP = ["iam", "service-accounts"]

    def __init__(self, name: str):
        super().__init__(name=name, ns="sa")

    def params_describe(self):
        return [
            "describe", self.name, "--format", "json"
        ]

    def params_create(self):
        return [
            "create", self.name, "--format", "json"
        ]


class ServiceAccountCapableMixin:

    @property
    def service_account(self):
        return getattr(self, "_service_account", None)

    @service_account.setter
    def service_account(self, sa: ServiceAccount):
        setattr(self, "_service_account", sa)
