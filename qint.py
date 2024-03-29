from qclasses import *
import os
import sys
import runpy


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        print("Interpreter Error")
        print(self.parser.lexer.text.splitlines()[node.token.line])
        print(" " * node.token.col + "^")
        print(
            f'No visit_{type(node).__name__} method, error on position {str(node.token.line + 1)}:{str(node.token.col)}')
        sys.exit(1)


class Interpreter(NodeVisitor):
    def __init__(self, parser, variables, sourcefile):
        self.parser = parser
        self.Variables = variables
        self.sourcefile = sourcefile

    def visit_BinOp(self, node):
        a = self.visit(node.left)
        b = self.visit(node.right)
        if isinstance(a, VarVal):
            a = a.value
        if isinstance(a, VarVal):
            b = a.value

        ops = {
            Tokens.PLUS: lambda a, b: a + b,
            Tokens.MINUS: lambda a, b: a - b,
            Tokens.MULTIPLY: lambda a, b: a * b,
            Tokens.DIVIDE: lambda a, b: a / b,
            Tokens.LESS_THAN: lambda a, b: a < b,
            Tokens.GREATER_THAN: lambda a, b: a > b,
            Tokens.EQUAL: lambda a, b: a == b,
            Tokens.LESS_EQUAL: lambda a, b: a <= b,
            Tokens.GREATER_EQUAL: lambda a, b: a >= b,
            Tokens.NOT_EQUAL: lambda a, b: a != b,
            Tokens.AND: lambda a, b: a and b,
            Tokens.OR: lambda a, b: a or b,
            Tokens.POWER: lambda a, b: a ** b,
            Tokens.PERCENT: lambda a, b: a % b,
            Tokens.TIN_OP: lambda a, b: b if a is None else a
        }

        return ops.get(node.op.type, lambda a, b: None)(a, b)

    def visit_Num(self, node):
        return node.value

    def visit_Float(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        match node.op.type:
            case Tokens.PLUS:
                val = self.visit(node.expr)
                if isinstance(val, VarVal):
                    val = val.value
                return +val
            case Tokens.MINUS:
                val = self.visit(node.expr)
                if isinstance(val, VarVal):
                    val = val.value
                return -val
            case Tokens.TIN_OP:
                val = self.visit(node.expr)
                if isinstance(val, VarVal):
                    val = val.value
                ret = None
                for v in val:
                    if v is not None:
                        ret = v
                        break
                return ret

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        if node.left.token.type == Tokens.LISTITEM:
            llist = self.Variables.getVar(node.left.token.value)
            llist.value[self.visit(node.left.item)] = self.visit(node.right)
            self.Variables.setVar(llist)
        else:
            var_name = node.left.value
            var_val = self.visit(node.right)
            var = VarVal(var_name, var_val)
            self.Variables.setVar(var)

    def visit_Var(self, node):
        var_name = node.value
        val = self.Variables.getVar(var_name)
        if val is None:
            print("Interpreter Error")
            if self.parser is not None:
                print(self.parser.lexer.text.splitlines()[node.token.line])
                print(" " * node.token.col + "^")
            print(
                f'Variable not found, error on position {str(node.token.line + 1)}:{str(node.token.col)}')
            sys.exit(1)
        else:
            return val.value

    def visit_AssignOp(self, node):
        ops = {
            Tokens.ADD: lambda a, b: a + b,
            Tokens.SUB: lambda a, b: a - b,
            Tokens.AMUL: lambda a, b: a * b,
            Tokens.ADIV: lambda a, b: a / b,
            Tokens.AMOD: lambda a, b: a % b,
        }
        if node.left.token.type == Tokens.LISTITEM:
            llist = self.Variables.getVar(node.left.value)
            llist.value[self.visit(node.left.item)] = ops[node.token.type](
                self.visit(node.left.item), self.visit(node.right))
            self.Variables.setVar(llist)
        else:
            var_old = self.Variables.getVar(node.left.value).value
            var_new = self.visit(node.right)
            var = VarVal(node.left.value, ops[node.token.type](var_old, var_new))
            self.Variables.setVar(var)

    def visit_FncDec(self, node):
        self.Variables.setVar(VarVal(node.name, node))

    def visit_InlineFunc(self, node):
        return node

    def visit_FncCall(self, node):
        var = self.Variables.getVar(node.name)
        if var is None:
            print("Interpreter Error")
            print(self.parser.lexer.text.splitlines()[node.token.line])
            print(" " * node.token.col + "^")
            print(
                f'Function {node.name} not found, error on position {str(node.token.line)}:{str(node.token.col)}')
            sys.exit(1)
        else:
            if isinstance(var, PythonFunc):
                var = PythonFuncCall(node.token, var.func, node.args)
                return self.visit(var)
        if not len(node.args) == len(var.value.args):
            print("Interpreter Error")
            print(self.parser.lexer.text.splitlines()[node.token.line])
            print(" " * node.token.col + "^")
            print(
                f'Expected {str(len(node.args))} args, got {str(len(var.value.args))}, error on position {str(node.token.line)}:{str(node.token.col)}')
            sys.exit(1)

        newvars = Vars()
        i = 0
        for arg in node.args:
            toadd = self.visit(arg)
            nvar = VarVal(var.value.args[i].value, toadd)
            newvars.setVar(nvar)
            i += 1

        # local variables
        actualvariables = self.Variables
        self.Variables = newvars
        if os.name == "nt":
            toinclude = runpy.run_path("C:\\qolang\\libs\\std.py")
        elif os.name == "posix":
            toinclude = runpy.run_path("/usr/lib/qo/std.py")

        for fn, fs in toinclude["qolang_export"].items():
            if callable(toinclude[fn]):
                added = PythonFunc(node.token, fs, toinclude[fn])
            else:
                added = VarVal(fs, toinclude[fn])
            self.Variables.setVar(added)
        self.Variables.setVar(actualvariables.getVar("__main__"))
        self.Variables.setVar(actualvariables.getVar("__qcf__"))

        for node in var.value.node.children:
            if isinstance(node, Return):
                returned = self.visit(node)
                self.Variables = actualvariables
                return returned
            else:
                self.visit(node)

        self.Variables = actualvariables

    def visit_PythonFuncCall(self, node):
        args = []
        i = 0
        for arg in node.args:
            toadd = self.visit(arg)
            if isinstance(toadd, VarVal):
                toadd = toadd.value
            args += [toadd]
            i += 1

        ret = None
        self.Variables, ret = node.func(self.Variables, args)
        return ret

    def visit_String(self, node):
        return node.value

    def visit_Boolean(self, node):
        return node.value

    def visit_Pointer(self, node):
        return node.value

    def visit_If_St(self, node):
        if self.visit(node.condition).value if hasattr(self.visit(node.condition), "value") else self.visit(node.condition):
            for statement in node.consequences:
                self.visit(statement)
        else:
            for statement in node.alternatives:
                self.visit(statement)

    def visit_For_St(self, node):
        self.visit(node.initial)
        while self.visit(node.condition):
            for statement in node.statements:
                self.visit(statement)
            self.visit(node.everyiter)

    def visit_While_St(self, node):
        while self.visit(node.condition):
            for statement in node.statements:
                self.visit(statement)

    def visit_Times_St(self, node):
        for i in range(self.visit(node.times)):
            if node._as is not None:
                self.Variables.setVar(VarVal(node._as, i))
            for statement in node.statements:
                self.visit(statement)

    def visit_Fstring(self, node):
        result = ''
        for nod in node.nodes:
            match nod.type:
                case Tokens.STRING:
                    result += nod.value
                case Tokens.ID:
                    result += str(self.visit(Var(nod)))
        return result

    def visit_Return(self, node):
        return self.visit(node.value)

    def visit_List(self, node):
        return [self.visit(nnode) for nnode in node.values]

    def visit_ListItem(self, node):
        if node.attributes.slice is None:
            return self.visit(node.left)[self.visit(node.item)]
        elif node.attributes.steps is None:
            start = self.visit(node.attributes.slice[0])
            stop = self.visit(node.attributes.slice[1])
            if stop is None:
                return [val for val in self.visit(node.left)[start:]]
            else:
                return [val for val in self.visit(node.left)[start:stop]]
        else:
            start = self.visit(node.attributes.slice[0])
            stop = self.visit(node.attributes.slice[1])
            steps = self.visit(node.attributes.steps)
            if stop is None:
                return [val for val in self.visit(node.left)[start::steps]]
            else:
                return [val for val in self.visit(node.left)[start:stop:steps]]

    def visit_Foreach_St(self, node):
        for item in self.visit(node.llist):
            self.Variables.setVar(VarVal(node.pointer, item))
            for statement in node.statements:
                self.visit(statement)

    def visit_None_Type(self, node):
        return None

    def visit_Include(self, node):
        import qo
        sourcedir = os.path.dirname(os.path.realpath(self.sourcefile))

        libpath = ""
        if os.name == "nt":
            libpath = "C:\\qolang\\libs\\"
        elif os.name == "posix":
            libpath = "/usr/lib/qo/"

        incfile = node.incfile.replace('.', os.sep)
        outvar = node._as

        if os.path.isfile(os.path.join(sourcedir, incfile + ".qo")):
            qo.run([sys.argv[0], os.path.join(sourcedir, incfile + ".qo")])
            exported = qo.Variables.getVar("__export__")
            if exported is not None:
                for variable in exported.value:
                    self.Variables.setExistingAttr(
                        outvar, qo.Variables.getVar(variable))
        elif os.path.isfile(os.path.join(sourcedir, incfile + ".py")):
            toinclude = runpy.run_path(
                os.path.join(sourcedir, incfile + ".py"))
            for fn, fs in toinclude["qolang_export"].items():
                if callable(toinclude[fn]) and (toinclude[fn].qo_callable if hasattr(toinclude[fn], "qo_callable") else True):
                    added = PythonFunc(node.token, fs, toinclude[fn])
                else:
                    added = VarVal(fs, toinclude[fn])
                self.Variables.setExistingAttr(outvar, added)
        elif os.path.isfile(libpath + incfile + ".qo"):
            qo.run([sys.argv[0], libpath + incfile + ".qo"])
            exported = qo.Variables.getVar("__export__")
            if exported is not None:
                for variable in exported.value:
                    self.Variables.setExistingAttr(
                        outvar, qo.Variables.getVar(variable))
        elif os.path.isfile(libpath + incfile + ".py"):
            toinclude = runpy.run_path(libpath + incfile + ".py")
            for fn, fs in toinclude["qolang_export"].items():
                if callable(toinclude[fn]) and (toinclude[fn].qo_callable if hasattr(toinclude[fn], "qo_callable") else True):
                    added = PythonFunc(node.token, fs, toinclude[fn])
                else:
                    added = VarVal(fs, toinclude[fn])
                self.Variables.setExistingAttr(outvar, added)

    def visit_Define(self, node):
        self.Variables.setVar(VarVal(node.token.value, node.value))

    def visit_Dict(self, node):
        return {k: self.visit(v) for k, v in node.values.items()}

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)
