from basicblock import ControlFlowGraph

def build_cfg(ast):
    assert ast[0] == 'script'
    _, script_name, statements = ast

    cfg = ControlFlowGraph()
    entry = cfg.new_block()
    build_from_statements(cfg, entry, statements)
    return cfg

def build_from_statements(cfg, block, stmts):

    for stmt in stmts:
        kind = stmt[0]

        if kind == 'declare':
            block.statements.append(stmt)

        elif kind == 'if':
            cond = stmt[1]
            then_stmts = stmt[2] # Could be none
            elseif_stmts = stmt[3] # Could be none
            else_stmts = stmt[4] # Could be none
            
            #then_block = cfg.new_block()
            after_block = cfg.new_block()

#            if elseif_stmts:
#                elseif_block = cfg.new_block()
#            else:
#                elseif_block = after_block # Fall through if no elseif

            if then_stmts and then_stmts != [None]:
                then_block = cfg.new_block()
            else:
                then_block = after_block # Fall through if no else

            if else_stmts:
                else_block = cfg.new_block()
            else:
                else_block = after_block # Fall through if no else


            current_fallback = else_block if else_stmts else after_block

            # Iterate in reverse to preserve order while chaining forward
            for cond_elseif, stmts2 in reversed(elseif_stmts or []):
                b = cfg.new_block()
                cfg.blocks.append(b)
                b.statements.append(('branch', cond_elseif, cfg.new_block().label, current_fallback.label))
                b.successors = [b.statements[-1][2], current_fallback.label]
                
                #body_block = next(b for b in cfg.blocks if b.label == b.statements[-1][2])
                body_block = next(
                    (b for b in cfg.blocks if b.statements and len(b.statements[-1]) > 2 and b.label == b.statements[-1][2]),
                    None
                )
                
                if body_block:
                    returned = build_from_statements(cfg, body_block, stmts2)
                    if returned:
                        returned.successors = [after_block.label]

                current_fallback = b
            
            block.statements.append(('branch', cond, then_block.label, current_fallback.label))
            block.successors = [then_block.label, current_fallback.label]

            if then_stmts and then_stmts != [None]:
              returned_then = build_from_statements(cfg, then_block, then_stmts)
              if returned_then:
                  returned_then.successors = [after_block.label]
                
            if else_stmts:
                returned_else = build_from_statements(cfg, else_block, else_stmts)
                if returned_else:
                    returned_else.successors = [after_block.label]

            block = after_block  # <-- REBIND to continue adding to the after-block

            continue  # resume from here

        elif kind == 'return':
            block.statements.append(stmt)
            block.successors = []  # end of flow
            return None

        elif block == None:
            print('hit none')
            return None

        else:
            block.statements.append(stmt)

    # If flow didn't return or branch, create a new block to continue
    next_block = cfg.new_block()
    block.successors = [next_block.label]
    return next_block