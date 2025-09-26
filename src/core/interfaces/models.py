from abc import ABC
from dataclasses import asdict, is_dataclass
from typing import Optional, Set, Dict, Any


class AbstractModel(ABC):
    """
    Base model, from which any domain model should be inherited.
    """

    async def to_dict(
            self,
            exclude: Optional[Set[str]] = None,
            include: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        if is_dataclass(self):
            data: Dict[str, Any] = asdict(self)
        else:
            data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

        if exclude:
            for key in exclude:
                data.pop(key, None)

        if include:
            data.update(dict(include))

        return data
