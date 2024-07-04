from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from typing import Self


class Node(ABC):
    @abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_the_solution(self, final_state: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def extend_node(self) -> list[Self]:
        raise NotImplementedError

    @abstractmethod
    def sequence_actions(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class BFS:
    def __init__(self, start: Node, final: str) -> None:
        self.start_state = start
        self.final_state = final
        self.frontier = [self.start_state]
        self.checked_nodes: list[Node | None] = []
        self.number_of_steps = 0
        # self.path = []  # noqa: ERA001

    def insert_to_frontier(self, node: Node) -> None:
        self.frontier.append(node)

    def remove_from_frontier(self) -> Node | None:
        first_node = self.frontier.pop(0)
        self.checked_nodes.append(first_node)
        return first_node

    def frontier_is_empty(self) -> bool:
        if len(self.frontier) == 0:
            return True
        return False

    def search(self) -> list[str] | None:
        while True:
            self.number_of_steps += 1
            if self.frontier_is_empty():
                return None

            selected_node = self.remove_from_frontier()

            assert selected_node is not None
            if selected_node.is_the_solution(self.final_state):
                return selected_node.sequence_actions()

            new_nodes = selected_node.extend_node()
            if len(new_nodes) > 0:
                for new_node in new_nodes:
                    if new_node not in self.frontier and new_node not in self.checked_nodes:
                        self.insert_to_frontier(new_node)
