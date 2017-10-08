class Scope:
    def __init__(self, parent = None):
        self.names = {}
        self.parent = parent
    def __getitem__(self, name):
        if name not in self.names:
            if name in self.parent.names:
                return self.parent.names[name]
        else:
            return self.names[name]
    def __setitem__(self, name, obj):
        if self.parent == None:
            self.names[name] = obj
        elif name not in self.parent.names:
            self.names[name] = obj
        else:
            self.parent.names[name] = obj

class Number:
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        if self.value == self.value:
            return True
        else:
            return False
    def __lt__(self, other):
        if self.value < other.value:
            return True
        else:
            return False
    def __add__(self, other):
        return Number(self.value + other.value)
    def __mul__(self, other):
        return Number(self.value - other.value)
    def __floordiv__(self, other):
        return Number(self.value // other.value)
    def __mod__(self, other):
        return Number(self.value % other.value)
    def __and__(self, other):
        if self.value == 0:
            lhs = 0
        else:
            lhs = 1
        if other.value == 0:
            rhs = 0
        else:
            rhs = 1
        return Number(lhs & rhs)
    def __or__(self, other):
        if self.value == 0:
            lhs = 0
        else:
            lhs = 1
        if other.value == 0:
            rhs = 0
        else:
            rhs = 1
        return Number(lhs | rhs)
    def __neg__(self):
        return Number(-self.value)
    def evaluate(self, scope):
        return self

class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body
    def evaluate(self, scope):
        return self

class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function
    def evaluate(self, scope):
        scope[name] = function

class Conditional:
    def __init__(self, condition, if_true, if_false = None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false
    def evaluate(self, scope):
        if condition.evaluate(scope) == Number(0):
            for op in self.if_false[:-1]:
                op.evaluate(scope)
            if self.if_false != None:
                return self.if_false[-1].evaluate(scope)
        else:
            for op in self.if_true[:-1]:
                op.evaluate(scope)
            if self.if_true != None:
                return self.if_true[-1].evaluate(scope)

class Print:
    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, scope):
        print(Number(expr.evaluate()).value)
        return Number(expr.evaluate()).value

class Read:
    def _init__(self, name):
        self.name = name
    def evaluate(self, scope):
        scope[name] = Number(input())
        return scope[name]

class FunctionCall: 
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args
    def evaluate(self, scope):
        self.function = scope[self.fun_expr]
        self.func_args =[]
        for op in self.args:
            self.func_args.append(op.evaluate(scope))
        self.call_scope = Scope(scope)
        for res in self.func_args:
            self.call_scope[self.function.args] = res
        for op in self.function.body[:-1]:
            self.op.evaluate(self.call_scope)
        return self.function.body[-1].evaluate(self.call_scope)
        
class Reference:
    def __init__(self, name):
        self.name = name
    def evaluate(self, scope):
        return scope[self.name]

class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
    def evaluate(self, scope):
        if type(lhs) == 'str':
            self.lhs = scope[lhs]
        elif type(lhs) == 'Number':
            self.lhs = lhs
        else:
            self.lhs = lhs.evaluate(scope)
        if type(rhs) == 'str':
            self.rhs == scope[rhs]
        elif type(rhs) == 'Number':
            els.rhs = rhs
        else:
            self.num = rhs.evaluate(scope)
        if op == '+':
            return lhs + rhs
        elif op == '-':
            return lhs - rhs
        elif op == '*':
            return lhs * rhs
        elif op == '/':
            return lhs / rhs
        elif op == '%':
            return lhs % rhs
        elif op == '==':
            return lhs == rhs
        elif op == '!=':
            return lhs != rhs
        elif op == '||':
            return lhs | rhs
        else:
            return lhs & rhs
        
class UnaryOperation:
    def __init__(self, op, expr):
        self.expr = expr
        self.op = op
    def evaluate(self, score):
        if type(self.expr) == 'str':
            self.expr = scope[expr]
        elif type(self.expr) == 'Number':
            self.expr = self.expr
        else:
            self.expr = self.expr.evaluate(score)
        if self.op == '-':
            return -self.expr
        elif self.expr.value == 0:
            return Number(1)
        else:
            return Number(0)
        
def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end = ' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope) 

#def my_tests():
    

if __name__ == '__main__':
    example()
    #my_tests()
        
