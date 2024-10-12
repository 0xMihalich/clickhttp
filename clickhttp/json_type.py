from typing import Any, Dict, List, TypeAlias, Union


JsonType: TypeAlias = List[
    List[
        Union[str,
              int,
              float,
              bool,
              None,
              Dict[str, Any,],
              List[Any]
        ],
    ]
]
