class Scope:
    def __init__(self, parent=None):
        self.names = {}
        self.parent = parent

    def __getitem__(self, name):
        if name not in self.names:
            if self.parent:
                return self.parent.names[name]
        else:
            return self.names[name]

    def __setitem__(self, name, obj):
        self.names[name] = obj


def body_evaluate(body, scope):
    for op in body[:-1]:
        op.evaluate(scope)
    if body:
        return body[-1].evaluate(scope)


class Number:
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __add__(self, other):
        return Number(self.value + other.value)

    def __sub__(self, other):
        return Number(self.value - other.value)

    def __mul__(self, other):
        return Number(self.value * other.value)

    def __floordiv__(self, other):
        return Number(self.value // other.value)

    def __mod__(self, other):
        return Number(self.value % other.value)

    def __and__(self, other):
        return self.value and self.value

    def __or__(self, other):
        return self.value or self.value

    def __neg__(self):
        return Number(0) - self

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
        scope[self.name] = self.function
        return self.function


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        condition = self.condition.evaluate(scope)
        if condition == Number(0):
            if self.if_false:
                return body_evaluate(self.if_false, scope)
            else:
                return Number(0)
        else:
            if self.if_true:
                return body_evaluate(self.if_true, scope)
            else:
                return Number(0)

class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        answ = self.expr.evaluate(scope)
        print(answ.value)
        return answ


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))
        return scope[self.name]


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        self.function = self.fun_expr.evaluate(scope)
        self.func_args = []
        for op in self.args:
            self.func_args.append(op.evaluate(scope))
        self.call_scope = Scope(scope)
        for res, arg in list(zip(self.func_args, self.function.args)):
            self.call_scope[arg] = res
        return body_evaluate(self.function.body, self.call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.lhs_expr = lhs
        self.rhs_expr = rhs
        self.op = op
        self.lhs = Number(0)
        self.rhs = Number(0)
        self.opers = {}
        self.opers['+'] = lambda x, y: x + y
        self.opers['-'] = lambda x, y: x - y
        self.opers['*'] = lambda x, y: x * y
        self.opers['/'] = lambda x, y: x // y
        self.opers['%'] = lambda x, y: x % y
        self.opers['=='] = lambda x, y: Number(x == y)
        self.opers['!='] = lambda x, y: Number(x != y)
        self.opers['<='] = lambda x, y: Number(x <= y)
        self.opers['>='] = lambda x, y: Number(x >= y)
        self.opers['||'] = lambda x, y: Number(x or y)
        self.opers['&&'] = lambda x, y: Number(x and y)
        self.opers['<'] = lambda x, y: Number(x < y)
        self.opers['>'] = lambda x, y: Number(x > y)

    def evaluate(self, scope):
        self.lhs = self.lhs_expr.evaluate(scope)
        self.rhs = self.rhs_expr.evaluate(scope)
        return self.opers[self.op](self.lhs, self.rhs)


class UnaryOperation:
    def __init__(self, op, expr):
        self.expr = expr
        self.op = op
        self.opers = {}
        self.opers['!'] = lambda x: Number(not x)
        self.opers['-'] = lambda x: -x

    def evaluate(self, scope):
        num = Number(0)
        num = self.expr.evaluate(scope)
        return self.opers[self.op](num)


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
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)

def my_tests():
    scope = Scope()
    print("Write x:")
    read = Read('x')
    read.evaluate(scope)
    print("Write y:")
    read = Read('y')
    read.evaluate(scope)
    print("It should print max:")
    Conditional(BinaryOperation(Reference('y'), '>', Reference('x')),
                [Print(Reference('y'))],
                [Print(Reference('x'))]).evaluate(scope)

if __name__ == '__main__':
    example()
    my_tests()
