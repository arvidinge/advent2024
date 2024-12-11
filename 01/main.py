

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

  total_diff = 0

  for i in range(len(list1)):
    num1, num2 = list1[i], list2[i]
    total_diff += abs(num1-num2)
  
  print(total_diff)
    


if __name__ == "__main__":
  main()  