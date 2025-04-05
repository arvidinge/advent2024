

def main():
  keys: list[str] = []
  locks: list[str] = []
  content: str
  with open('input.txt') as file:
    content = file.read()

  keys_locks = content.split('\n\n')

  for key_or_lock in keys_locks:
    if key_or_lock.split('\n')[0].startswith("#"):
      locks.append(key_or_lock)
    else:
      keys.append(key_or_lock)

  key_heights: list[list[int]] = []
  for key in keys:
    key_heights.append(key_str_to_heights(key))

  lock_heights: list[list[int]] = []
  for lock in locks:
    lock_heights.append(lock_str_to_heights(lock))

  correct_pairs = 0
  for lock in lock_heights:
    for key in key_heights:

      bad_combo: bool = False
      for i in range(len(lock)):
        if lock[i] + key[i] > 5: 
          bad_combo = True
          break
      if not bad_combo:
        correct_pairs += 1

  print(correct_pairs)
          

def key_str_to_heights(key: str) -> list[int]:
  columns = [0, 0, 0, 0, 0]
  key_lines = key.split('\n')

  for i in range(len(key_lines)-2, 0, -1):
    for c in range(len(key_lines[i])):
      if key_lines[i][c] == '#':
        columns[c] += 1

  return columns

def lock_str_to_heights(lock: str) -> list[int]:
  columns = [0, 0, 0, 0, 0]
  lock_lines = lock.split('\n')

  for i in range(1, len(lock_lines)-1):
    for c in range(len(lock_lines[i])):
      if lock_lines[i][c] == '#':
        columns[c] += 1

  return columns


if __name__ == "__main__":
  main()
