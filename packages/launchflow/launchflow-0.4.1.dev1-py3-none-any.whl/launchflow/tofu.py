from typing import Dict, Optional, Set

from launchflow.models.flow_state import EnvironmentState
from launchflow.resource import Resource, T


# TODO: move this into a lf.tofu submodule
# Considering moving all gcp / aws resource definitions to this tofu submodule, but
# still expose them at the lf.gcp / lf.aws submodule level
class TofuResource(Resource[T]):
    def __init__(
        self,
        name: str,
        replacement_arguments: Optional[Set[str]] = None,
        resource_id: Optional[str] = None,
        ignore_arguments: Optional[Set[str]] = None,
    ):
        super().__init__(name, replacement_arguments, resource_id, ignore_arguments)

    def __hash__(self) -> int:
        return super().__hash__()

    def import_tofu_resource(
        self, environment_state: EnvironmentState
    ) -> Dict[str, str]:
        """Returns a mapping from the resource name to the import string."""
        raise NotImplementedError(
            f"Importing is currently not support for resource type: {self.__class__.__name__}"
        )
