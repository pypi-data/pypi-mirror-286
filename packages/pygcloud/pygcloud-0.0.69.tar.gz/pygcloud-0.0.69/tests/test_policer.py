"""
@author: jldupont
"""
import pytest
from pygcloud.models import Policy
from pygcloud.policies import PolicyServiceAccount


class MockPolicy(Policy):
    ...


@pytest.fixture
def mock_policy():
    return MockPolicy


def test_policy_derived_classes(mock_policy):

    assert isinstance(Policy.derived_classes, list), \
        print(Policy.derived_classes)

    assert PolicyServiceAccount in Policy.derived_classes
    assert Policy not in Policy.derived_classes


def test_policy_allowed(mock_policy, mock_service):

    mock_policy.allow(mock_service, "some reason")

    assert mock_policy.allows(mock_service)
