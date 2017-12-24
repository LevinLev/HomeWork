class PureCheckVisitor:
    def visit(self, prog):
        return prog.accept(self)

    def visit_list(self, l):
        for op in l or []:
            if not op.accept(self):
                return False
        return True

    def visit_number(self, number):
        return True

    def visit_read(self, read):
        return False

    def visit_print(self, printer):
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
        answ = self.visit_list(cond.if_true) and answ
        answ = self.visit_list(cond.if_false) and answ
        return answ


class NoReturnValueCheckVisitor:
    def visit(self, prog):
        return prog.accept(self)

    def visit_list(self, l):
        if not l:
            return True
        else:
            for op in l[:-1]:
                op.accept(self)
            return l[-1].accept(self)

    def visit_number(self, number):
        return False

    def visit_read(self, read):
        return False

    def visit_print(self, printer):
        printer.expr.accept(self)
        return False

    def visit_ref(self, ref):
        return False

    def visit_bin_op(self, bin_op):
        bin_op.lhs_expr.accept(self)
        bin_op.rhs_expr.accept(self)
        return False

    def visit_un_op(self, un_op):
        un_op.expr.accept(self)
        return False

    def visit_cond(self, cond):
        answ = cond.condition.accept(self)
        answ = self.visit_list(cond.if_true) or answ
        answ = self.visit_list(cond.if_false) or answ
        return answ

    def visit_function(self, function):
        return self.visit_list(function.body)

    def visit_func_def(self, func_def):
        if func_def.function.accept(self):
            print(func_def.name)
        return False

    def visit_func_call(self, func_call):
        answ = self.visit_list(func_call.args)
        answ = func_call.fun_expr.accept(self) or answ
        return answ
