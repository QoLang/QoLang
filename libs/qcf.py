# QoLang Configuration File library
from qclasses import VarVal, Tokens, PythonFunc, Token
import sys
import os
qolang_export = {
    "newqcf": "new"
}

class QCFGet:
    def __init__(self, QCFI, QCFF):
        self.QCFI = QCFI
        self.QCFF = QCFF
    
    def __call__(self, Variables, args):
        return (Variables, Variables.getVar(self.QCFI).value.getVar(args[0]).value)
    
    __code__ = __call__.__code__

class QCFSet:
    def __init__(self, QCFI, QCFF):
        self.QCFI = QCFI
        self.QCFF = QCFF
    
    def __call__(self, Variables, args):
        qcfi = Variables.getVar(self.QCFI)
        qcfi.value.setVar(VarVal(args[0], args[1]))
        Variables.setVar(qcfi)
        return (Variables, None)
    
    __code__ = __call__.__code__

def newqcf(Variables, args):
    """
    Export all variables.
    """
    import qo
    ftr = os.path.join(os.path.dirname(os.path.realpath(sys.argv[1])), args[0])
    qo.run([sys.argv[0], ftr], qcf=True)
    Variables.setVar(VarVal(args[1], qo.Variables))
    Variables.setAttr(args[1], 'get', QCFGet(args[1], args[0]))
    Variables.setAttr(args[1], 'set', QCFSet(args[1], args[0]))
    return (Variables, None)