class Scope:
    def __init__(self, parent=None):
        self.names = {}
        self.parent = parent

    def __getitem__(self, name):
        if name not in self.names:
            return self.parent[name]
        else:
            return self.names[name]

    def __setitem__(self, name, obj):
        self.names[name] = obj


def body_evaluate(body, scope):
    result = Number(0)
    for op in body or []:
        result = op.evaluate(scope)
    return result


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
        if self.condition.evaluate(scope) == Number(0):
            return body_evaluate(self.if_false, scope)
        else:
            return body_evaluate(self.if_true, scope)


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
        function = self.fun_expr.evaluate(scope)
        func_args = [op.evaluate(scope) for op in self.args]
        call_scope = Scope(scope)
        for arg_value, arg_name in zip(func_args, function.args):
            call_scope[arg_name] = arg_value
        return body_evaluate(function.body, call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    OPS = {
      '+': lambda x, y: x + y,
      '-': lambda x, y: x - y,
      '*': lambda x, y: x * y,
      '%': lambda x, y: x % y,
      '/': lambda x, y: x // y,
      '<': lambda x, y: Number(int(x < y)),
      '>': lambda x, y: Number(int(x > y)),
      '==': lambda x, y: Number(int(x == y)),
      '!=': lambda x, y: Number(int(x != y)),
      '<=': lambda x, y: Number(int(x <= y)),
      '>=': lambda x, y: Number(int(x >= y)),
      '||': lambda x, y: Number(x.value or y.value),
      '&&': lambda x, y: Number(x.value and y.value)
            }

    def __init__(self, lhs, op, rhs):
        self.lhs_expr = lhs
        self.rhs_expr = rhs
        self.op = op

    def evaluate(self, scope):
        lhs = self.lhs_expr.evaluate(scope)
        rhs = self.rhs_expr.evaluate(scope)
        return self.OPS[self.op](lhs, rhs)


class UnaryOperation:
    OPS = {
      '!': lambda x: Number(int(x == Number(0))),
      '-': lambda x: -x
            }

    def __init__(self, op, expr):
        self.expr = expr
        self.op = op

    def evaluate(self, scope):
        num = self.expr.evaluate(scope)
        return self.OPS[self.op](num)


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
    print("It should print 0 (8 times):")
    Print(BinaryOperation(Number(1), '&&', Number(0))).evaluate(scope)
    Print(BinaryOperation(Number(0), '||', Number(0))).evaluate(scope)
    Print(BinaryOperation(Number(1), '-', Number(1))).evaluate(scope)
    Print(BinaryOperation(Number(-1), '+', Number(1))).evaluate(scope)
    Print(BinaryOperation(Number(0), '/', Number(10))).evaluate(scope)
    Print(BinaryOperation(Number(1), '==', Number(0))).evaluate(scope)
    Print(UnaryOperation('!', Number(12))).evaluate(scope)
    Print(UnaryOperation('-', Number(0))).evaluate(scope)


def scope_test():
    scope1 = Scope()
    scope1[1] = 'a'
    scope2 = Scope(scope1)
    scope2[2] = 'b'
    scope3 = Scope(scope2)
    scope3[3] = 'c'
    scope4 = Scope(scope3)
    scope4[4] = 'd'
    print("It should print 'abcd'")
    print(scope4[1])
    print(scope4[2])
    print(scope4[3])
    print(scope4[4])


if __name__ == '__main__':
    example()
    my_tests()
    scope_test()
