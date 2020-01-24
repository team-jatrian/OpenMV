
numbers = [20, 21, 10, 3, 80, 2, 12, 11, 9, 8, 7, 6, 5, 4, 3]
amount = []

def compareIntArray(arr, variation, minimum, maximum):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if abs(arr[j]-arr[i]) <= variation:
                if arr[i] > minimum and arr[j] > minimum:
                    if arr[i] < maximum and arr[j] < maximum:
                        amount.append(arr[i])
                        amount.append(arr[j])
    return amount
print(compareIntArray(numbers, 4, 8, 20))
