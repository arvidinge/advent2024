wires: dict[str, object] = {}

def main():
  content: str
  with open('input_test.txt') as file:
    content = file.read()

  rvalues, expressions = content.split('\n\n')

  # x and y wires
  for line in rvalues.split('\n'):
    wire, value = line.split(': ')
    wires[wire] = int(value)

  # expressions to evaluate
  for line in expressions.split('\n'):
    value, wire = line.split(' -> ')
    wires[wire] = value

  maxz = 0
  while get_zname(maxz) in wires.keys():
    maxz += 1
  maxz -= 1
  
  final_sum = 0
  for i in range(maxz+1):
    final_sum += pow(2, i) * get_wire_value(get_zname(i))
  
  print(final_sum)


def get_zname(i: int) -> str:
  return f'z{str(i).zfill(2)}'
  

wire_cache: dict[str, int] = {}
# rdepth: int = 0
def get_wire_value(wire: str) -> int:
  # global rdepth
  global wire_cache
  # rdepth += 2
  # print(f'{rdepth*' '}lookup wire ', wire)
  # print(f'{rdepth*' '}cache: ', wire_cache)
  if wire in wire_cache.keys():
    # print(f'{rdepth*' '}cache hit, ', wire_cache[wire])
    # rdepth -= 2
    return wire_cache[wire]
  
  if type(wires[wire]) is int:
    # print(f'{rdepth*' '}base wire, ', wires[wire])
    # rdepth -= 2
    return wires[wire]
  
  else: 
    # print(f'{rdepth*' '}evaluating wire: ', wires[wire])
    a, op, b = wires[wire].split(' ')
    res = None
    if op == 'AND':
      res = get_wire_value(a) & get_wire_value(b)
    elif op == 'OR':
      res = get_wire_value(a) | get_wire_value(b)
    elif op == 'XOR':
      res = get_wire_value(a) ^ get_wire_value(b)

    if res is not None:
      wire_cache[wire] = res
      # rdepth -= 2
      return res
    else: 
      raise KeyError('someting wong wi tu lo')



if __name__ == "__main__":
  main()
