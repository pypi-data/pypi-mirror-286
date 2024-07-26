"""
Policer

@author: jldupont
"""
import logging
import sys
from typing import List, Union
from .models import Policy, PolicyViolation, PolicingResult, PolicingResults
from .models import service_groups, ServiceGroup, GCPService
from .constants import PolicerMode


warn = logging.warning
error = logging.error


class _Policer:

    def __init__(self):
        self._disabled: List[Policy] = []
        self._mode: PolicerMode = PolicerMode.RUN

    def disable(self, policy: Policy):
        assert isinstance(policy, Policy)
        self._disabled.append(policy)

    @property
    def mode(self):
        return self._mode

    def _eval_one(self, policy: Policy, service: GCPService) -> PolicingResult:

        if policy.allows(service):
            warn(f"Policy '{policy.name}' allows "
                 f"service '{service.name}'. Skipping.")
            return PolicingResult(
                service=service,
                policy=policy,
                allowed=True
            )

        passed = False
        raised = False
        violation: Union[PolicyViolation, None] = None

        try:
            policy.evaluate(service_groups, service)
            passed = True

        except PolicyViolation as e:

            violation = e
            passed = False

            if policy in self._disabled:
                warn(f"Disabled '{policy.name}' raised"
                     f" violation but ignoring: {e}")

        except Exception as e:

            passed = False
            raised = True

            if policy in self._disabled:
                warn(f"Disabled '{policy.name}' raised: {e}")
            else:
                error(f"Policy 'name' raised: {e}")

            if self.mode == PolicerMode.RUN:
                sys.exit(1)

        return PolicingResult(
            service=service,
            policy=policy,
            passed=passed,
            raised=raised,
            violation=violation
        )

    def _process_one(self, policy: Policy) -> List[PolicingResult]:
        """
        Go through all service groups so that each service
        is verified against the policy.

        The `eval` method is also given access to all
        service groups to account for more complex patterns.

        NOTE The head of the return list will contain the outcome.
        """

        group: ServiceGroup
        service: GCPService
        result: PolicingResult
        results: List[PolicingResult] = []

        for group in service_groups:
            for service in group:
                result = self._eval_one(policy, service)
                if not result.passed:
                    results.insert(0, result)
                else:
                    results.append(result)

        return results

    def police(self) -> PolicingResults:
        """
        In `DRY_RUN` mode, the method will return a `PolicingResults` instance.

        In `RUN` mode, if there is a violation, `sys.exit(1)` will be executed.
        """
        batch_result: List[PolicingResult]
        _all: List[Policy] = Policy.derived_classes

        results: List[PolicingResult] = []
        outcome = None

        policy: Policy

        for policy in _all:
            batch_result = self._process_one(policy)
            head_result = batch_result[0]
            if not head_result.passed:
                outcome = head_result
            results.extend(batch_result)

        return PolicingResults(
            outcome=outcome,
            results=results
        )


# Singleton instance
Policer = _Policer()
