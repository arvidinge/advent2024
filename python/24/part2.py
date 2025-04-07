from typing import Self
import re


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
nodes: dict[str, Node] = {}
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
    nodes[wire] = Node(name=wire, base_val=int(value))
    # base_wires[wire] = int(value)

  # internal wires
  for line in internal.split('\n'):
    value, wire = line.split(' -> ')
    a, op, b = re.split(r'\s(AND|OR|XOR)\s', value)
    if a not in nodes:
      node_a = Node(name=a, parents=set([wire]))
      nodes[a] = node_a
    if b not in nodes:
      node_b = Node(name=b, parents=set([wire]))
      nodes[b] = node_b
    wire_node = Node(name=wire, child_a=a, child_b=b, operand=op)
    nodes[a].parents.add(wire)
    nodes[b].parents.add(wire)
    nodes[wire] = wire_node

  for node in nodes.values():
    print(node)

  xval = get_full_wire_number('x')
  print('xval ', xval)

  yval = get_full_wire_number('y')
  print('yval ', yval)

  ztarget = xval + yval
  print('ztarget ', ztarget)

  curzval = get_full_wire_number('z')
  print('curzval ', curzval)

  swapdepth = 0


# def swap(cur_depth: int, sublist: dict[str, Node]):
#   if cur_depth == MAX_SWAPS:


def get_full_wire_number(xyorz: str) -> int:
  max_bit = get_full_wire_bit_count(xyorz)
  sum = 0
  for i in range(max_bit+1):
    sum += pow(2, i) * get_wire_value(wire_name(xyorz, i))
  return sum


def get_full_wire_bit_count(xyorz: str) -> int:
  i = 0
  while (wire_name(xyorz, i) in nodes):
    i += 1
  i -= 1
  return i


def wire_name(base_name: str, i: int) -> str:
  return f'{base_name}{str(i).zfill(2)}'


def get_wire_value(wire: str) -> int:
  global wire_value_cache
  if wire in wire_value_cache:
    return wire_value_cache[wire]

  if nodes[wire].base_val is not None:
    return nodes[wire].base_val

  else:
    a = nodes[wire].child_a
    op = nodes[wire].operand
    b = nodes[wire].child_b

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
