from typing import Any, Dict, List, NewType, Union


JsonType = NewType("JsonType", List[List[Union[str, int, float, bool, None, Dict[str, Any], List[Any]]]])
