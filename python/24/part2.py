from typing import Self
import re
import itertools


class Node:
  name: str = None
  parents: set[str] = []  # empty == roots (z wires)
  child_a: str = None,
  child_b: str = None,
  base_val: int = None  # has value only if no children (xy wires)
  operand: str = None  # has value only if children (not xy wires)

  def __init__(self,
               name: str,
               parents: set[str] = set(),
               child_a: str = None,
               child_b: str = None,
               base_val: int = None,
               operand: str = None
               ):
    self.name = name
    self.parents = parents
    self.child_a = child_a
    self.child_b = child_b
    self.base_val = base_val
    self.operand = operand

  def __repr__(self):
    if self.base_val is not None:
      return f'{self.name}: {self.base_val}'
    return f'{self.child_a or '?a'} {self.operand or '?op'} {self.child_b or '?b'} -> {self.name}'


MAX_SWAPS = 4
node_lookup: dict[str, int] = {}
node_list: list[tuple[str, Node]] = []
xval: int = None
yval: int = None
ztarget: int = None
wire_value_cache: dict[str, int] = {}


def main():
  global xval
  global yval
  global curzval
  global ztarget

  content: str
  with open('input.txt') as file:
    content = file.read()

  xandy, internal = content.split('\n\n')

  # construct the nodes and wire tables
  # base (x and y) wires
  for line in xandy.split('\n'):
    wire, value = line.split(': ')
    node_list.append((wire, Node(name=wire, base_val=int(value))))
    node_lookup[wire] = len(node_list) - 1

  # internal wires
  for line in internal.split('\n'):
    value, wire = line.split(' -> ')
    a, op, b = re.split(r'\s(AND|OR|XOR)\s', value)
    if a not in node_lookup:
      node_list.append((a, Node(name=a, parents=set([wire]))))
      node_lookup[a] = len(node_list) - 1
    if b not in node_lookup:
      node_list.append((b, Node(name=b, parents=set([wire]))))
      node_lookup[b] = len(node_list) - 1
    wire_node = Node(name=wire, child_a=a, child_b=b, operand=op)
    node_list[node_lookup[a]][1].parents.add(wire)
    node_list[node_lookup[b]][1].parents.add(wire)
    node_list.append((wire, wire_node))
    node_lookup[wire] = len(node_list) - 1

  for node in node_list:
    print(node)

  xval = get_full_wire_number('x')
  print('xval ', xval)

  yval = get_full_wire_number('y')
  print('yval ', yval)

  ztarget = xval + yval
  print('ztarget ', ztarget)

  curzval = get_full_wire_number('z')
  print('curzval ', curzval)

  print('first internal ', get_first_internal_node_index())

  swapdepth = 0


def check_subswaps(cur_depth: int, sublist: dict[str, Node]) -> None | list[int]:
  '''
  Return None if no swap resulted in a 
  '''
  # if cur_depth == MAX_SWAPS:
  for i in range(len(sublist)):
    for j in range(i+1, len(sublist)-1):
      print('swap ', i, j)


def get_first_internal_node_index():
  i=0
  while node_list[i][1].base_val is not None:
    i+=1
  return i


def is_base_wire(wire:str) -> bool:
  return wire.startswith('x') or wire.startswith('y')


def get_full_wire_number(xyorz: str) -> int:
  max_bit = get_full_wire_bit_count(xyorz)
  sum = 0
  for i in range(max_bit+1):
    sum += pow(2, i) * get_wire_value(wire_name(xyorz, i))
  return sum


def get_full_wire_bit_count(xyorz: str) -> int:
  i = 0
  wire_names = [entry[0] for entry in node_list]
  while (wire_name(xyorz, i) in wire_names):
    i += 1
  i -= 1
  return i


def wire_name(base_name: str, i: int) -> str:
  return f'{base_name}{str(i).zfill(2)}'


def get_wire_value(wire: str) -> int:
  global wire_value_cache
  if wire in wire_value_cache:
    return wire_value_cache[wire]

  if node_list[node_lookup[wire]][1].base_val is not None:
    return node_list[node_lookup[wire]][1].base_val

  else:
    a = node_list[node_lookup[wire]][1].child_a
    op = node_list[node_lookup[wire]][1].operand
    b = node_list[node_lookup[wire]][1].child_b

    res = None
    if op == 'AND':
      res = get_wire_value(a) & get_wire_value(b)
    elif op == 'OR':
      res = get_wire_value(a) | get_wire_value(b)
    elif op == 'XOR':
      res = get_wire_value(a) ^ get_wire_value(b)

    if res is not None:
      wire_value_cache[wire] = res
      return res
    else:
      raise KeyError('sum ting wong wi tu lo')


if __name__ == "__main__":
  main()
