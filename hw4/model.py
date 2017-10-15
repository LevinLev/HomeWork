import sys


class Scope:
    def __init__(self, parent=None):
        self.names = {}
        self.parent = parent

    def __getitem__(self, name):
        if name not in self.names:
            parent = self.parent
            while parent is not None:
                if name in parent.names:
                    return parent.names[name]
                parent = parent.parent
        else:
            return self.names[name]

    def __setitem__(self, name, obj):
        self.names[name] = obj


class Number:
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return hash(str(self.value)) % ((sys.maxsize + 1) * 2)

    def __eq__(self, other):
        if self.value == other.value:
            return Number(1)
        else:
            return Number(0)

    def __lt__(self, other):
        if self.value < other.value:
            return Number(1)
        else:
            return Number(0)

    def __gt__(self, other):
        if self.value > other.value:
            return Number(1)
        else:
            return Number(0)

    def __le__(self, other):
        if self.value <= other.value:
            return Number(1)
        else:
            return Number(0)

    def __gt__(self, other):
        if self.value >= other.value:
            return Number(1)
        else:
            return Number(0)

    def __ne__(self, other):
        if self.value != other.value:
            return Number(1)
        else:
            return Number(0)

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
        scope[self.name] = self.function
        return self.function


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if type(self.condition) == 'str':
            condition = scope(self.condition)
        else:
            condition = self.condition
        if condition.evaluate(scope) == Number(0):
            if self.if_false is None:
                return Number(0)
            else:
                for op in self.if_false[:-1]:
                    op.evaluate(scope)
                return self.if_false[-1].evaluate(scope)
        else:
            if self.if_true is None:
                return Number(0)
            else:
                for op in self.if_true[:-1]:
                    op.evaluate(scope)
                return self.if_true[-1].evaluate(scope)


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
        scope[self.name] = Number(input())
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
        for op in self.function.body[:-1]:
            op.evaluate(self.call_scope)
        return self.function.body[-1].evaluate(self.call_scope)


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

    def evaluate(self, scope):
        if type(self.lhs_expr) == 'str':
            self.lhs = scope[self.lhs_expr].evaluate(scope)
        else:
            self.lhs = self.lhs_expr.evaluate(scope)
        if type(self.rhs_expr) == 'str':
            self.rhs == scope[self.rhs_expr].evaluate(scope)
        else:
            self.rhs = self.rhs_expr.evaluate(scope)
        if self.op == '+':
            return self.lhs + self.rhs
        elif self.op == '-':
            return self.lhs - self.rhs
        elif self.op == '*':
            return self.lhs * self.rhs
        elif self.op == '/':
            return self.lhs // self.rhs
        elif self.op == '%':
            return self.lhs % self.rhs
        elif self.op == '==':
            return self.lhs == self.rhs
        elif self.op == '!=':
            return self.lhs != self.rhs
        elif self.op == '<=':
            return self.lhs <= self.rhs
        elif self.op == '<':
            return self.lhs < self.rhs
        elif self.op == '>=':
            return self.lhs >= self.rhs
        elif self.op == '>':
            return self.lhs > self.rhs
        elif self.op == '&&':
            return self.lhs and self.rhs
        elif self.op == '||':
            return self.lhs or self.rhs
        else:
            print("'", self.op, "': No such operation")


class UnaryOperation:
    def __init__(self, op, expr):
        self.expr = expr
        self.op = op

    def evaluate(self, scope):
        num = Number(0)
        if type(self.expr) == 'str':
            num = scope[self.expr].evaluate(scope)
        else:
            num = self.expr.evaluate(scope)
        if self.op == '-':
            return -num
        elif self.op == '!':
            if num == Number(0):
                return Number(1)
            else:
                return Number(0)
        else:
            print("'", self.op, "': No such operation")


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
