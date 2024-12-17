

def main():
  list1: list[int] = []
  list2: list[int] = []
  with open('input.txt') as file:
    for line in file.readlines():
      num1, num2 = line.split('   ')
      list1.append(int(num1.strip()))
      list2.append(int(num2.strip()))
  
  list1.sort()
  list2.sort()
  factors: dict[int, int] = {}
  for num in list2:
    if num not in factors:
      factors[num] = 0
    factors[num] += 1

  total_similarity = 0
  for num in list1:
    if num not in factors:
      continue
    total_similarity += num * factors[num]
  
  print(total_similarity)


if __name__ == "__main__":
  main()  