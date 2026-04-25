from SymbolTable import *
from Type import *

class Node:
    def eval(self, env):
        pass

class Numeric(Node):
    def eval(self, env):
        pass

class Logic(Node):
    def eval(self, env):
        pass

class Void(Node):
    def eval(self, env):
        pass

# --- NUMERIC --- #
class Number(Numeric):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value

class Identifier(Numeric):
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def eval(self, env):
        result = env.lookup(self.name)
        if result != None:
            (_, value) = result
            return value
        else:
            text = "Line " + str(self.line) + " - " + self.name + " has not been declared"
            raise Exception(text)

class Minus(Numeric):
    def __init__(self, right):
        self.right = right

    def eval(self, env):
        right = float(self.right.eval(env))
        return -1 * right

class Add(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left + right

class Sub(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left - right

class Mul(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left * right

class Div(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        if right == 0:
            raise Exception("Division by zero")
        return left / right

class Mod(Numeric):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left % right

# --- LOGIC --- #
class TrueVal(Logic):
    def eval(self, env):
        return True

class FalseVal(Logic):
    def eval(self, env):
        return False

class Not(Logic):
    def __init__(self, right):
        self.right = right

    def eval(self, env):
        right = self.right.eval(env)
        return not right

class And(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = bool(self.left.eval(env))
        if not left:
            return False
        right = bool(self.right.eval(env))
        return right

class Or(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = bool(self.left.eval(env))
        if left:
            return True
        right = bool(self.right.eval(env))
        return right

class LessThan(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left < right

class GreaterThan(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left > right

class LessOrEqual(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left <= right

class GreaterOrEqual(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = float(self.left.eval(env))
        right = float(self.right.eval(env))
        return left >= right

class Equal(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = self.left.eval(env)
        right = self.right.eval(env)
        return left == right

class NEQ(Logic):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, env):
        left = self.left.eval(env)
        right = self.right.eval(env)
        return left != right

# --- VOID (statements) --- #
class Print(Void):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, env):
        value = self.expression.eval(env)
        print(value)

class Assignment(Void):
    def __init__(self, name, expression, line):
        self.name = name
        self.expression = expression
        self.line = line

    def eval(self, env):
        value = self.expression.eval(env)
        value_type = Type.BOOLEAN if isinstance(value, bool) else Type.NUMBER
        if not env.set(self.name, value_type, value):
            text = "Line " + str(self.line) + " - " + self.name + " has not been declared"
            raise Exception(text)

class StatementSequence(Void):
    def __init__(self, statements):
        self.statements = statements

    def eval(self, env):
        for stmt in self.statements:
            stmt.eval(env)

class Declaration(Void):
    def __init__(self, names, line):
        self.names = names
        self.line = line

    def eval(self, env):
        for name in self.names:
            if not env.insert(name):
                text = "Line " + str(self.line) + " - " + name + " has already been declared"
                raise Exception(text)

class Program(Void):
    def __init__(self, declaration, statements):
        self.declaration = declaration
        self.statements = statements

    def eval(self, env):
        self.declaration.eval(env)
        self.statements.eval(env)
