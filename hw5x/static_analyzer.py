import sys


class PureCheckVisitor:
    def visit(self, prog):
        return prog.accept(self)

    def visit_list(self, l):
        if l is None:
            return True
        for op in l:
            if not op.accept(self):
                return False
        return True

    def visit_number(self, number):
        return True

    def visit_read(self, read):
        return False

    def visit_write(self, write):
        return False

    def visit_ref(self, ref):
        return True

    def visit_function(self, function):
        return self.visit_list(function.body)

    def visit_func_def(self, func_def):
        return func_def.function.accept(self)

    def visit_func_call(self, func_call):
        answ = self.visit_list(func_call.args)
        return answ and func_call.fun_expr.accept(self)

    def visit_bin_op(self, bin_op):
        return bin_op.lhs_expr.accept(self) and bin_op.rhs_expr.accept(self)

    def visit_un_op(self, un_op):
        return un_op.expr.accept(self)

    def visit_cond(self, cond):
        answ = cond.condition.accept(self)
        answ = answ and self.visit_list(cond.if_true)
        answ = answ and self.visit_list(cond.if_false)
        return answ
