
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'st\xe2\xe65\x94\xef\xe0\xae!\xce\xf2\xb1\x8c\x1f\xe1'
    
_lr_action_items = {'RPAREN':([3,11,12,16,18,19,21,22,],[-8,-10,19,21,-9,-12,-11,-7,]),'NAME':([0,1,2,3,6,7,9,10,11,13,15,17,18,19,20,21,22,],[2,11,-10,-8,2,11,-6,11,-10,11,-4,11,-9,-12,-5,-11,-7,]),'INT':([0,1,2,3,6,7,9,10,11,13,15,17,18,19,20,21,22,],[3,3,-10,-8,3,3,-6,3,-10,3,-4,3,-9,-12,-5,-11,-7,]),'EQUALS':([2,],[13,]),'PLUS':([2,3,9,11,12,15,18,19,20,21,22,],[-10,-8,17,-10,17,17,-9,-12,17,-11,-7,]),'LPAREN':([0,1,2,3,6,7,8,9,10,11,13,15,17,18,19,20,21,22,],[1,1,-10,-8,1,1,16,-6,1,-10,1,-4,1,-9,-12,-5,-11,-7,]),'PRINT':([0,2,3,6,9,11,15,18,19,20,21,22,],[7,-10,-8,7,-6,-10,-4,-9,-12,-5,-11,-7,]),'INPUT':([0,1,2,3,6,7,9,10,11,13,15,17,18,19,20,21,22,],[8,8,-10,-8,8,8,-6,8,-10,8,-4,8,-9,-12,-5,-11,-7,]),'MINUS':([0,1,2,3,6,7,9,10,11,13,15,17,18,19,20,21,22,],[10,10,-10,-8,10,10,-6,10,-10,10,-4,10,-9,-12,-5,-11,-7,]),'$end':([2,3,4,5,6,9,11,14,15,18,19,20,21,22,],[-10,-8,-1,0,-2,-6,-10,-3,-4,-9,-12,-5,-11,-7,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[5,]),'expression':([0,1,6,7,10,13,17,],[9,12,9,15,18,20,22,]),'statement':([0,6,],[6,6,]),'module':([0,6,],[4,14,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> module','program',1,'p_program','parse.py',79),
  ('module -> statement','module',1,'p_module','parse.py',83),
  ('module -> statement module','module',2,'p_module','parse.py',84),
  ('statement -> PRINT expression','statement',2,'p_print_statement','parse.py',89),
  ('statement -> NAME EQUALS expression','statement',3,'p_statement_assign','parse.py',93),
  ('statement -> expression','statement',1,'p_statement_expr','parse.py',100),
  ('expression -> expression PLUS expression','expression',3,'p_plus_expression','parse.py',108),
  ('expression -> INT','expression',1,'p_int_expression','parse.py',112),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','parse.py',116),
  ('expression -> NAME','expression',1,'p_name_expression','parse.py',120),
  ('expression -> INPUT LPAREN RPAREN','expression',3,'p_input_expression','parse.py',124),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','parse.py',129),
]
