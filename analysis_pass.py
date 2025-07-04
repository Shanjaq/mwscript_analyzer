class ScriptAnalysisResult(object):
    def __init__(self, script_name):
        self.script_name = script_name
        self.max_path_cost = 0
        self.total_blocks = 0
        self.avg_path_cost = 0.0
        self.path_profiles = []  # Optional: list of path costs for histogramming
        self.flagged = False     # Future: heuristics for slow scripts

    def __repr__(self):
        return ("Script: %s\n"
                "  Max Path Cost: %d\n"
                "  Avg Path Cost: %.2f\n"
                "  Blocks: %d\n" % (
                    self.script_name,
                    self.max_path_cost,
                    self.avg_path_cost,
                    self.total_blocks
                ))


def evaluate_cfg_cost(cfg, ast):
    from collections import deque
    cost_table = {
        'set': 1,
        'journal': 2,
        'return': 0,
        'activate': 2,
        'say': 2,
        'aitravel': 2,
        'call': 2,
        'branch': 1,
        'declare': 0
    }

    # First, compute each block's cost
    for block in cfg.blocks:
        block.cost = sum(cost_table.get(stmt[0], 1) for stmt in block.statements)

    # Traverse paths and record total costs
    def walk_iterative(cfg, entry_block, max_paths=1000, max_depth=50, max_cost=100):
        stack = [(entry_block, 0, [])]  # (block, current_cost, visited)

        visited_paths = []
        seen = set()

        while stack and len(visited_paths) < max_paths:
            block, cost, visited = stack.pop()

            key = (block.label, tuple(visited))
            if key in seen:
                continue
            seen.add(key)

            if block.label in visited:
                continue  # avoid cycles

            new_visited = visited + [block.label]
            new_cost = cost + block.cost

            if len(new_visited) > max_depth or new_cost > max_cost:
                visited_paths.append(new_cost)  # Consider it truncated but record
                continue

            if not block.successors:
                visited_paths.append(new_cost)
                continue

            for succ in block.successors:
                next_block = next(b for b in cfg.blocks if b.label == succ)
                stack.append((next_block, new_cost, new_visited))

        return visited_paths


    result = ScriptAnalysisResult(ast[1])
    paths = walk_iterative(cfg, cfg.blocks[0], max_paths=32000, max_depth=120, max_cost=150)
    result.total_blocks = len(cfg.blocks)
    result.max_path_cost = max(paths or [0])
    result.avg_path_cost = float(sum(paths)) / len(paths) if paths else 0.0
    result.path_profiles = paths

    return result
