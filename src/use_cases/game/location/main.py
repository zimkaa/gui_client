from __future__ import annotations

from src.use_cases.game.location.implementation_logic import Node


class LocationNode(Node):
    def __init__(self, graph: dict[str, list[str]], value: str) -> None:
        self.graph = graph
        self.value = value
        self.parent = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LocationNode):
            return self.value == other.value
        return self.value == other

    def is_the_solution(self, final_state: str) -> bool:
        return self.value == final_state

    def extend_node(self) -> list[LocationNode]:
        children = [LocationNode(self.graph, child) for child in self.graph[self.value]]
        for child in children:
            child.parent = self  # type: ignore[assignment]
        return children

    def _find_path(self) -> list[str]:
        path: list[str] = []
        current_node = self
        while current_node.parent is not None:
            path.insert(0, current_node.value)
            current_node = current_node.parent
        path.insert(0, current_node.value)
        return path

    def sequence_actions(self) -> list[str]:
        path = self._find_path()
        path.pop(0)
        return path

    def __str__(self) -> str:
        total_path = self._find_path()
        path = ""
        for index in range(len(total_path)):
            if index == len(total_path) - 1:
                path += f"{total_path[index]} "
            else:
                path += f"{total_path[index]} -> "

        return path + f"\nPath length: {len(total_path)-1}"
