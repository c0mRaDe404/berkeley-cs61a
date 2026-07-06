"""A Scheme interpreter and its read-eval-print loop."""
from __future__ import print_function  # Python 2 compatibility

import sys
import os

from scheme_builtins import *
from scheme_reader import *
from ucb import main, trace
from scheme_builtins import scheme_list 

##############
# Eval/Apply #
##############



def scheme_eval(expr, env, _=None): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in environment ENV.
    

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    
    if isinstance(expr, Pair):
        first = scheme_eval(expr.first, env)
        return scheme_apply(first, expr.rest, env)
    else:
        if isinstance(expr, str):
            if expr in special_forms.keys():
                return SpecialForm(expr)
            return env.lookup(expr)
    return expr 


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    environment ENV."""
    # PROBLEM 2
    if scheme_builtin(procedure):
        return procedure.apply(args, env)
    if scheme_special_form(procedure):
        return procedure.apply(args, env) 
    if scheme_user_defined(procedure):
        new_args = []
        temp = args
        while temp is not nil: #evaluate arguments before executing the body
            new_args.append(scheme_eval(temp.first, env))
            temp = temp.rest
        args = scheme_list(*new_args)
        return procedure.apply(args, env)
    else:
        raise SchemeError(str(type(procedure).__name__) + f' is not callable: {procedure}')

    return 'Yet to be implemented'



################
# Environments #
################

class Frame(object):
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None)."""
        "Your Code Here"
        # Note: you should define instance variables self.parent and self.bindings
        self.parent = parent 
        self.bindings = {}
    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, key, value):
        """Define Scheme SYMBOL to have VALUE."""
        self.bindings[key] = value 

    def lookup(self, key):
        try:
            return self.bindings[key]
        except KeyError:
            parent = self.parent
            if parent is not None:
                return parent.lookup(key)
            raise SchemeError(f"unknown identifier: {key}") 
    
##############
# Procedures #
##############

class Procedure(object):
    """The supertype of all Scheme procedures."""

def scheme_procedurep(x):
    return isinstance(x, Procedure)

class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function."""

    def __init__(self, fn, use_env=False, name='builtin'):
        self.name = name
        self.fn = fn
        self.use_env = use_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

    def apply(self, args, env):
        """Apply SELF to ARGS in ENV, where ARGS is a Scheme list.

        >>> env = create_global_frame()
        >>> plus = env.bindings['+']
        >>> twos = Pair(2, Pair(2, nil))
        >>> plus.apply(twos, env)
        4
        """
        operands = []
        cur = args
        while cur is not nil:
            operands.append(scheme_eval(cur.first, env)) 
            cur = cur.rest 
        if self.use_env:
            operands.append(env)
        
        try: 
            return self.fn(*operands)
        except TypeError:
            raise SchemeError("invalid arguments count")

        # END PROBLEM 2

def scheme_builtin(x):
    return isinstance(x, BuiltinProcedure)

class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form."""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV."""
        self.formals = formals
        self.body = body
        self.env = env


    def apply(self, body, env):
        
        new_env = Frame(self.env)
        formals, args = self.formals, body 

        while formals is not nil and args is not nil:
            new_env.define(formals.first, args.first)
            formals, args = formals.rest, args.rest
        if formals is not nil or args is not nil:
            raise SchemeError("Incorrect number of arguments to function call")

        return do_begin_form(self.body, new_env)     
    
    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

def scheme_user_defined(x):
    return isinstance(x, LambdaProcedure) or isinstance(x, MuProcedure)


def add_builtins(frame, funcs_and_names):
    """Enter bindings in FUNCS_AND_NAMES into FRAME, an environment frame,
    as built-in procedures. Each item in FUNCS_AND_NAMES has the form
    (NAME, PYTHON-FUNCTION, INTERNAL-NAME)."""
    for name, fn, proc_name in funcs_and_names:
        frame.define(name, BuiltinProcedure(fn, name=proc_name))

#################
# Special Forms #
#################
"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""


class SpecialForm:
    def __init__(self, name):
        self.name = name
    
    def apply(self, body, env):
        return special_forms[self.name](body, env)
        

def scheme_special_form(x):
    return isinstance(x, SpecialForm)

def symbol(x):
    return isinstance(x, str)

def do_define_form(body, env):
    
    if body is nil:
            raise SchemeError("too few operands in form")
    
    target = body.first
    if symbol(target):
        if body.rest is nil: 
            raise SyntaxError("too few operands in form")
        elif len(body.rest) >= 2:
            raise SyntaxError("too many operands in form")
        else:
            env.define(target, scheme_eval(body.rest.first, env)) 
            return target
    elif isinstance(target, Pair):    
        function_id = target.first 
        function_formals = target.rest 
        function_body = body.rest
        env.define(function_id, LambdaProcedure(function_formals, function_body, env))
        return function_id 

    raise SchemeError(f"non-symbol: {target}")


def do_quote_form(body, env):
    if body is nil:
            raise SchemeError("too few operands in form")   
    if body.rest is not nil:
            raise SchemeError("too many operands in form")
    return body.first 

def do_begin_form(body, env):
    cur = body
    final_result = None 
    while cur is not nil:
        final_result = scheme_eval(cur.first, env)
        cur = cur.rest
    
    return final_result 


def do_lambda_form(body, env):
    if body is nil:
            raise SchemeError("too few operands in form")   
    formals = body.first 
    expr = body.rest 
    
    if expr is nil:
        raise SchemeError("too few operands in form")
    
    return LambdaProcedure(formals, expr, env)

def do_mu_form(body, env):
    if body is nil:
            raise SchemeError("too few operands in form")   
    formals = body.first 
    expr = body.rest 
    
    if expr is nil:
        raise SchemeError("too few operands in form")
    
    return MuProcedure(formals, expr)


def is_scheme_true(value):
    return value is not False  

def is_scheme_false(value):
    return value is False 


def do_and_form(body, env):
    expr = body 
    result = True
    while expr is not nil:
        result = scheme_eval(expr.first, env)
        if is_scheme_false(result):
            return result
        expr = expr.rest 
    return result

def do_or_form(body, env):
    expr = body 
    result = False
    while expr is not nil:
        result = scheme_eval(expr.first, env)
        if is_scheme_true(result):
            return result 
        expr = expr.rest 
    return result

def do_if_form(body, env):
    if body is nil:
        raise SchemeError("too few operands in form")

    predicate = body.first

    if body.rest is nil:
        raise SchemeError("too few operands in form")
    
    consequent = body.rest.first
    alternative = None

    if body.rest.rest is not nil:
        alternative = body.rest.rest.first 
    if body.rest.rest.rest is not nil:
        raise SchemeError("too many operands in form")
    if is_scheme_true(scheme_eval(predicate, env)):
        return scheme_eval(consequent, env)
    else:
        if alternative is None:
            return None 
        return scheme_eval(alternative, env)

def is_clause(expr):
    return isinstance(expr, Pair)

def do_cond_form(body, env): 
    cond_body = body 
    while cond_body is not nil:
        clause = cond_body.first
        if not is_clause(clause):
            raise SchemeError(f"badly formed expression {clause}") 

        if clause.first == "else":
            if cond_body.rest is not nil:
                raise SchemeError("else must be last")
            return do_begin_form(clause.rest, env)
        
        expr = scheme_eval(clause.first, env)
        if is_scheme_true(expr):
            if clause.rest is nil:
                return expr
            return do_begin_form(clause.rest, env)
        cond_body = cond_body.rest


def is_valid_binding(binding):
    return isinstance(binding, Pair)

def do_let_form(body, env):
    
    if body is nil:
        raise SchemeError("too few operands in form")

    head = body.first
    if not is_valid_binding(head):
        raise SchemeError("too few operands in form")

    tail = body.rest
    
    formals, args = [], [] 
    
    while head is not nil:
        binding = head.first
        if not is_valid_binding(binding):
            raise SchemeError("too few operands in form") 
        else:
            if not symbol(binding.first):
                raise SchemeError("invalid formal")
            if binding.rest is nil:
                raise SchemeError("too few operands in form")
            if len(binding) > 2:
                raise SchemeError("too many operands in form")
       

        formals.append(binding.first) 
        args.append(binding.rest.first) 
        head = head.rest 
     
    formals = scheme_list(*formals)
    args    = scheme_list(*args)
    #import pudb 
    #pudb.set_trace()
    proc = LambdaProcedure(formals, tail, env) 
    return scheme_apply(proc, args, env)


special_forms = {"define": do_define_form,
                 "quote" : do_quote_form,
                 "begin" : do_begin_form,
                 "lambda": do_lambda_form,
                 "and"   : do_and_form,
                 "or"    : do_or_form,
                 "if"    : do_if_form,
                 "cond"  : do_cond_form,
                 "let"   : do_let_form,
                 "mu"    : do_mu_form
                }





# Utility methods for checking the structure of Scheme programs

def validate_form(expr, min, max=float('inf')):
    """Check EXPR is a proper list whose length is at least MIN and no more
    than MAX (default: no maximum). Raises a SchemeError if this is not the
    case.

    >>> validate_form(read_line('(a b)'), 2)
    """
    if not scheme_listp(expr):
        raise SchemeError('badly formed expression: ' + repl_str(expr))
    length = len(expr)
    if length < min:
        raise SchemeError('too few operands in form')
    elif length > max:
        raise SchemeError('too many operands in form')

def validate_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct. Raise a SchemeError if the list of
    formals is not a list of symbols or if any symbol is repeated.

    >>> validate_formals(read_line('(a b c)'))
    """
    symbols = set()
    def validate_and_add(symbol, is_last):
        if not scheme_symbolp(symbol):
            raise SchemeError('non-symbol: {0}'.format(symbol))
        if symbol in symbols:
            raise SchemeError('duplicate symbol: {0}'.format(symbol))
        symbols.add(symbol)

    while isinstance(formals, Pair):
        validate_and_add(formals.first, formals.rest is nil)
        formals = formals.rest

    # here for compatibility with DOTS_ARE_CONS
    if formals != nil:
        validate_and_add(formals, True)

def validate_procedure(procedure):
    """Check that PROCEDURE is a valid Scheme procedure."""
    if not scheme_procedurep(procedure):
        raise SchemeError('{0} is not callable: {1}'.format(
            type(procedure).__name__.lower(), repl_str(procedure)))

#################
# Dynamic Scope #
#################

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition."""
        self.formals = formals
        self.body = body


    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))

    def apply(self, body, env):
        
        new_env = Frame(env)
        formals, args = self.formals, body 

        while formals is not nil and args is not nil:
            new_env.define(formals.first, args.first)
            formals, args = formals.rest, args.rest
        if formals is not nil or args is not nil:
            raise SchemeError("Incorrect number of arguments to function call")

        return do_begin_form(self.body, new_env)     
    


##################
# Tail Recursion #
##################


# Make classes/functions for creating tail recursive programs here?

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not a Thunk.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the optional questions."""
    val = scheme_apply(procedure, args, env)
    # Add stuff here?
    return val

# BEGIN PROBLEM 8
"*** YOUR CODE HERE ***"
# END PROBLEM 8


####################
# Extra Procedures #
####################

def scheme_map(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'map')
    validate_type(s, scheme_listp, 1, 'map')
    return s.map(lambda x: complete_apply(fn, Pair(x, nil), env))

def scheme_filter(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'filter')
    validate_type(s, scheme_listp, 1, 'filter')
    head, current = nil, nil
    while s is not nil:
        item, s = s.first, s.rest
        if complete_apply(fn, Pair(item, nil), env):
            if head is nil:
                head = Pair(item, nil)
                current = head
            else:
                current.rest = Pair(item, nil)
                current = current.rest
    return head

def scheme_reduce(fn, s, env):
    validate_type(fn, scheme_procedurep, 0, 'reduce')
    validate_type(s, lambda x: x is not nil, 1, 'reduce')
    validate_type(s, scheme_listp, 1, 'reduce')
    value, s = s.first, s.rest
    while s is not nil:
        value = complete_apply(fn, scheme_list(value, s.first), env)
        s = s.rest
    return value

################
# Input/Output #
################

def read_eval_print_loop(next_line, env, interactive=False, quiet=False,
                         startup=False, load_files=()):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    if startup:
        for filename in load_files:
            scheme_load(filename, True, env)
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if not quiet and result is not None:
                    print(repl_str(result))
        except (SchemeError, SyntaxError, ValueError, RuntimeError) as err:
            if (isinstance(err, RuntimeError) and
                'maximum recursion depth exceeded' not in getattr(err, 'args')[0]):
                raise
            elif isinstance(err, RuntimeError):
                print('Error: maximum recursion depth exceeded')
            else:
                print('Error:', err)
        except KeyboardInterrupt:  # <Control>-C
            if not startup:
                raise
            print()
            print('KeyboardInterrupt')
            if not interactive:
                return
        except EOFError:  # <Control>-D, etc.
            print()
            return

def scheme_load(*args):
    """Load a Scheme source file. ARGS should be of the form (SYM, ENV) or
    (SYM, QUIET, ENV). The file named SYM is loaded into environment ENV,
    with verbosity determined by QUIET (default true)."""
    if not (2 <= len(args) <= 3):
        expressions = args[:-1]
        raise SchemeError('"load" given incorrect number of arguments: '
                          '{0}'.format(len(expressions)))
    sym = args[0]
    quiet = args[1] if len(args) > 2 else True
    env = args[-1]
    if (scheme_stringp(sym)):
        sym = eval(sym)
    validate_type(sym, scheme_symbolp, 0, 'load')
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    args = (lines, None) if quiet else (lines,)
    def next_line():
        return buffer_lines(*args)

    read_eval_print_loop(next_line, env, quiet=quiet)

def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))

def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    env.define('eval',
               BuiltinProcedure(scheme_eval, True, 'eval'))
    env.define('apply',
               BuiltinProcedure(complete_apply, True, 'apply'))
    env.define('load',
               BuiltinProcedure(scheme_load, True, 'load'))
    env.define('procedure?',
               BuiltinProcedure(scheme_procedurep, False, 'procedure?'))
    env.define('map',
               BuiltinProcedure(scheme_map, True, 'map'))
    env.define('filter',
               BuiltinProcedure(scheme_filter, True, 'filter'))
    env.define('reduce',
               BuiltinProcedure(scheme_reduce, True, 'reduce'))
    env.define('undefined', None)
    add_builtins(env, BUILTINS)
    return env

@main
def run(*argv):
    import argparse
    parser = argparse.ArgumentParser(description='CS 61A Scheme Interpreter')
    parser.add_argument('--pillow-turtle', action='store_true',
                        help='run with pillow-based turtle. This is much faster for rendering but there is no GUI')
    parser.add_argument('--turtle-save-path', default=None,
                        help='save the image to this location when done')
    parser.add_argument('-load', '-i', action='store_true',
                       help='run file interactively')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=None,
                        help='Scheme file to run')
    args = parser.parse_args()

    import scheme
    scheme.TK_TURTLE = not args.pillow_turtle
    scheme.TURTLE_SAVE_PATH = args.turtle_save_path
    sys.path.insert(0, '')
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(scheme.__file__))))

    next_line = buffer_input
    interactive = True
    load_files = []

    if args.file is not None:
        if args.load:
            load_files.append(getattr(args.file, 'name'))
        else:
            lines = args.file.readlines()
            def next_line():
                return buffer_lines(lines)
            interactive = False

    read_eval_print_loop(next_line, create_global_frame(), startup=True,
                         interactive=interactive, load_files=load_files)
    tscheme_exitonclick()
