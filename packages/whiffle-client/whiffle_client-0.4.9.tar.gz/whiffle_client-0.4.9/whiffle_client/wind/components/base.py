import inspect
import json
from dataclasses import asdict, dataclass


@dataclass
class BaseComponent:
    @classmethod
    def from_dict(cls, env):
        instance = cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )
        instance._readonly_attrs_names = []
        for k, v in env.items():
            if k not in inspect.signature(cls).parameters:
                setattr(instance, k, v)
                instance._readonly_attrs_names.append(k)

        return instance

    def _get_api_params(self):
        return asdict(self)

    def __str__(self) -> str:
        data = json.dumps(
            asdict(self)
            | {k: getattr(self, k) for k in getattr(self, "_readonly_attrs_names", {})},
            indent=4,
        )
        return f"{self.__class__}:\n{data}"

    def __repr__(self) -> str:
        return json.dumps(
            asdict(self)
            | {k: getattr(self, k) for k in getattr(self, "_readonly_attrs_names", {})}
        )
