import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        # Distância de Manhattan: soma das distâncias de cada peça até sua posição goal
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = tile - 1  # tile 1 → índice 0, tile 2 → índice 1, ...
            distance += abs(i // 3 - goal_index // 3) + abs(i % 3 - goal_index % 3)
        return distance

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, depth=0)

        counter = 0
        heap = [(self.heuristic(initial), counter, initial)]
        visited = set()
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while heap:
            max_frontier_size = max(max_frontier_size, len(heap))
            _, _, node = heapq.heappop(heap)

            if node in visited:
                continue
            visited.add(node)

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            nodes_expanded += 1

            for neighbor in node.neighbors():
                if neighbor not in visited:
                    nodes_generated += 1
                    counter += 1
                    f = neighbor.cost + self.heuristic(neighbor)
                    heapq.heappush(heap, (f, counter, neighbor))

        return SearchResult(solution=None, nodes_expanded=nodes_expanded,
                            nodes_generated=nodes_generated, max_frontier_size=max_frontier_size)
