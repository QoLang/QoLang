# QoLang Configuration File library
from qclasses import VarVal, Tokens, PythonFunc, Token
import sys
import os
qolang_export = {
    "newqcf": "new"
}

class QCFInstance:
    def __init__(self, name, file, Variables):
        self.name = name
        self.file = file
        self.Variables = Variables
    
    def __str__(self):
        return f"QCFI({self.name})"

class QCFGet:
    def __init__(self, QCFI):
        self.QCFI = QCFI
    
    def __call__(self, Variables, args):
        return (Variables, Variables.getVar(self.QCFI).Variables.getVar(args[0]).value)
    
    __code__ = __call__.__code__

class QCFSet:
    def __init__(self, QCFI):
        self.QCFI = QCFI
    
    def __call__(self, Variables, args):
        qcfi = Variables.getVar(self.QCFI)
        qcfi.Variables.setVar(VarVal(args[0], args[1]))
        Variables.setVar(qcfi)
        return (Variables, None)
    
    __code__ = __call__.__code__

def newqcf(Variables, args):
    """
    Create a new QCF instance.
    """
    import qo
    ftr = os.path.join(os.path.dirname(os.path.realpath(sys.argv[1])), args[0])
    qo.run([sys.argv[0], ftr], qcf=True)
    Variables.setVar(QCFInstance(args[1], args[0], qo.Variables))
    Variables.setAttr(args[1], 'get', QCFGet(args[1]))
    Variables.setAttr(args[1], 'set', QCFSet(args[1]))
    return (Variables, None)