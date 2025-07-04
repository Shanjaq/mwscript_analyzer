class BasicBlock(object):
    def __init__(self, label):
        self.label = label
        self.statements = []
        self.successors = []
        #self.cost = 0  # Sum of statement costs

    def __repr__(self):
        lines = ["%s:" % self.label]
        for stmt in self.statements:
            lines.append("  %s" % repr(stmt))
        lines.append("  -> %s" % self.successors)
        return "\n".join(lines)


class ControlFlowGraph(object):
    def __init__(self):
        self.blocks = []
        self.counter = 0

    def new_block(self):
        label = "L%d" % self.counter
        self.counter += 1
        block = BasicBlock(label)
        self.blocks.append(block)
        return block
