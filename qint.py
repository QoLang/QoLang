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
            f'No visit_{type(node).__name__} method, error on position {str(node.token.line)}:{str(node.token.col)}')
        sys.exit(1)


class Interpreter(NodeVisitor):
    def __init__(self, parser, variables, sourcefile):
        self.parser = parser
        self.Variables = variables
        self.sourcefile = sourcefile

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(left, VarVal):
            left = left.value
        if isinstance(right, VarVal):
            right = right.value
        match node.op.type:
            case Tokens.PLUS:
                return left + right
            case Tokens.MINUS:
                return left - right
            case Tokens.MULTIPLY:
                return left * right
            case Tokens.DIVIDE:
                return left / right
            case Tokens.LESS_THAN:
                return left < right
            case Tokens.GREATER_THAN:
                return left > right
            case Tokens.EQUAL:
                return left == right
            case Tokens.LESS_EQUAL:
                return left <= right
            case Tokens.GREATER_EQUAL:
                return left >= right
            case Tokens.NOT_EQUAL:
                return left != right
            case Tokens.AND:
                return left and right
            case Tokens.OR:
                return left or right
            case Tokens.POWER:
                return left ** right

    def visit_Num(self, node):
        return node.value

    def visit_Float(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
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

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass

    def visit_Assign(self, node):
        if node.left.token.type == Tokens.LISTITEM:
            llist = self.Variables.getVar(node.left.value)
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
            print(self.parser.lexer.text.splitlines()[node.token.line])
            print(" " * node.token.col + "^")
            print(
                f'Variable not found, error on position {str(node.token.line)}:{str(node.token.col)}')
            sys.exit(1)
        else:
            return val.value

    def visit_FncDec(self, node):
        self.Variables.setVar(node)

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
        if not len(node.args) == len(var.args):
            print("Interpreter Error")
            print(self.parser.lexer.text.splitlines()[node.token.line])
            print(" " * node.token.col + "^")
            print(
                f'Expected {str(len(node.args))} args, got {str(len(var.args))}, error on position {str(node.token.line)}:{str(node.token.col)}')
            sys.exit(1)
            
        # local variables
        actualvariables = self.Variables
        self.Variables = Vars()
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
        
        i = 0
        for arg in node.args:
            toadd = arg
            if isinstance(arg, Var):
                toadd = actualvariables.getVar(arg.value).value
            nvar = VarVal(var.args[i].value, toadd)
            self.Variables.setVar(nvar)
            i += 1

        ret = 0
        for node in var.node.children:
            if isinstance(node, Return):
                self.Variables = actualvariables
                return self.visit(node)
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
            return self.Variables.getVar(node.value).value[self.visit(node.item)]
        elif node.attributes.steps is None:
            start = self.visit(node.attributes.slice[0])
            stop = self.visit(node.attributes.slice[1])
            if stop is None:
                return [val for val in self.Variables.getVar(node.value).value[start:]]
            else:
                return [val for val in self.Variables.getVar(node.value).value[start:stop]]
        else:
            start = self.visit(node.attributes.slice[0])
            stop = self.visit(node.attributes.slice[1])
            steps = self.visit(node.attributes.steps)
            if stop is None:
                return [val for val in self.Variables.getVar(node.value).value[start::steps]]
            else:
                return [val for val in self.Variables.getVar(node.value).value[start:stop:steps]]

    def visit_Foreach_St(self, node):
        for item in self.visit(node.llist):
            self.Variables.setVar(VarVal(node.pointer, item))
            for statement in node.statements:
                self.visit(statement)

    def visit_None_Type(self, node):
        return None

    def visit_Add(self, node):
        if node.left.token.type == Tokens.LISTITEM:
            llist = self.Variables.getVar(node.left.value)
            llist.value[self.visit(node.left.item)] += self.visit(node.right)
            self.Variables.setVar(llist)
        else:
            var_old = self.Variables.getVar(node.left.value).value
            var_new = self.visit(node.right)
            var = VarVal(node.left.value, var_old + var_new)
            self.Variables.setVar(var)

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
            for variable in qo.Variables.getVar("__export__").value:
                self.Variables.setExistingAttr(
                    outvar, qo.Variables.getVar(variable))
        elif os.path.isfile(os.path.join(sourcedir, incfile + ".py")):
            toinclude = runpy.run_path(
                os.path.join(sourcedir, incfile + ".py"))
            for fn, fs in toinclude["qolang_export"].items():
                if callable(toinclude[fn]):
                    added = PythonFunc(node.token, fs, toinclude[fn])
                else:
                    added = VarVal(fs, toinclude[fn])
                self.Variables.setExistingAttr(outvar, added)
        elif os.path.isfile(libpath + incfile + ".qo"):
            qo.run([sys.argv[0], libpath + incfile + ".qo"])
            for variable in qo.Variables.getVar("__export__").value:
                self.Variables.setExistingAttr(
                    outvar, qo.Variables.getVar(variable))
        elif os.path.isfile(libpath + incfile + ".py"):
            toinclude = runpy.run_path(libpath + incfile + ".py")
            for fn, fs in toinclude["qolang_export"].items():
                if callable(toinclude[fn]):
                    added = PythonFunc(node.token, fs, toinclude[fn])
                else:
                    added = VarVal(fs, toinclude[fn])
                self.Variables.setExistingAttr(outvar, added)

    def visit_Define(self, node):
        self.Variables.setVar(VarVal(node.token.value, node.value))

    def visit_Sub(self, node):
        if node.left.token.type == Tokens.LISTITEM:
            llist = self.Variables.getVar(node.left.value)
            llist.value[self.visit(node.left.item)] -= self.visit(node.right)
            self.Variables.setVar(llist)
        else:
            var_old = self.Variables.getVar(node.left.value).value
            var_new = self.visit(node.right)
            var = VarVal(node.left.value, var_old - var_new)
            self.Variables.setVar(var)

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)
