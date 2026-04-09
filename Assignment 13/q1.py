import itertools

class Symbol:
    def __init__(self, name=None, is_composite=False):
        self.name = name
        self.is_composite = is_composite
        if is_composite:
            self.symbol_type = "composite"
        else:
            self.symbol_type = "primary"

    def get_value(self, env):
        return env.get(self.name, False)

    @staticmethod
    def logical_not(val):
        return not val

    @staticmethod
    def logical_and(val1, val2):
        return val1 and val2

    @staticmethod
    def logical_or(val1, val2):
        return val1 or val2

    @staticmethod
    def logical_implies(val1, val2):
        return (not val1) or val2

    @staticmethod
    def logical_iff(val1, val2):
        return val1 == val2


class PropositionEvaluator:
    def __init__(self):
        self.precedence = {'<->': 1, '->': 2, 'v': 3, '∨': 3, '^': 4, '∧': 4, '~': 5}
        self.composite_handler = Symbol(is_composite=True)

    def _tokenize(self, expression):
        tokens = []
        i = 0
        expression = expression.replace(' ', '')
        while i < len(expression):
            if expression[i:i+2] == '->':
                tokens.append('->')
                i += 2
            elif expression[i:i+3] == '<->':
                tokens.append('<->')
                i += 3
            elif expression[i] in ['v', '∨']:
                tokens.append(expression[i])
                i += 1
            elif expression[i].isalpha():
                tokens.append(expression[i])
                i += 1
            else:
                tokens.append(expression[i])
                i += 1
        return tokens

    def evaluate(self, expression, env):
        tokens = self._tokenize(expression)
        postfix = []
        ops = []
        
        for token in tokens:
            if token.isalpha() and token not in ['v', '∨']:
                postfix.append(Symbol(name=token, is_composite=False))
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops and ops[-1] != '(':
                    postfix.append(ops.pop())
                ops.pop()
            else:
                while ops and ops[-1] != '(' and self.precedence.get(ops[-1], 0) >= self.precedence.get(token, 0):
                    if token == '~' and ops[-1] == '~':
                        break
                    postfix.append(ops.pop())
                ops.append(token)
                
        while ops:
            postfix.append(ops.pop())
            
        stack = []
        
        # Here we evaluate using a stack
        for token in postfix:
            if isinstance(token, Symbol) and token.symbol_type == "primary":
                stack.append(token.get_value(env))
            elif token == '~':
                val = stack.pop()
                stack.append(self.composite_handler.logical_not(val))
            else:
                right = stack.pop()
                left = stack.pop()
                if token in ['^', '∧']:
                    stack.append(self.composite_handler.logical_and(left, right))
                elif token in ['v', '∨']:
                    stack.append(self.composite_handler.logical_or(left, right))
                elif token == '->':
                    stack.append(self.composite_handler.logical_implies(left, right))
                elif token == '<->':
                    stack.append(self.composite_handler.logical_iff(left, right))
                    
        return stack[0]

    def print_truth_table(self, expression):
        tokens = self._tokenize(expression)
        unique_vars = sorted(list(set([t for t in tokens if t.isalpha() and t not in ['v', '∨']])))
        
        header_elements = unique_vars + [expression]
        print("\t".join(header_elements))
        
        for values in itertools.product([False, True], repeat=len(unique_vars)):
            env = dict(zip(unique_vars, values))
            result = self.evaluate(expression, env)
            
            row_values = ['T' if v else 'F' for v in values]
            row_values.append('T' if result else 'F')
            print("\t".join(row_values))
        print("-" * 50)


if __name__ == "__main__":
    evaluator = PropositionEvaluator()
    propositions = [
        "~P->Q",
        "~P ^ ~Q",
        "~P v ~Q",
        "~P->~Q",
        "~P <-> ~Q",
        "(P v Q)^(~P->Q)",
        "((P v Q)->~R)",
        "(((P v Q)->~R) <-> ((~P^~Q)->~R))",
        "(((P->Q)^(Q->R))->(Q->R))",
        "(((P->(Q v R)) -> (~P^~Q^~R)))"
    ]
    
    for prop in propositions:
        evaluator.print_truth_table(prop)
