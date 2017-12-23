import sys


class PureCheckVisitor:
    def visit(self, prog):
        return prog.accept(self)

    def visit_number(self, number):
        return True

    def visit_read(self, read):
        return False

    def visit_write(self, write):
        return False

    def visit_ref(self, ref):
        return True

    def visit_function(self, function):
        for op in function.body:
            if op.visit() is False:
                return False
        return True

    def visit_func_def(self, func_def):
        return func_def.function.visit()

    def visit_func_call(self, func_call):
        return func_call.fun_expr.visit()

    def visit_bin_op(self, bin_op):
        return bin_op.lhs_expr.visit() and bin_op.rhs_expr.visit()

    def visit_un_op(self, un_op):
        return un_op.expr.visit()

    def visit_cond(self, cond):
        answ = cond.conditional.visit()
        for op in cond.if_true.visit():
            answ = answ and op.visit()
        if cond.if_true is not None:
            for op in cond.if_false:
                answ = answ and op.visit()
        return answ
