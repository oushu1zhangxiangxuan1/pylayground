def multiply_list_elements(numbers):
    result = 1
    for number in numbers:
        result *= number
    return result

output = multiply_list_elements([1, 2, 3, 4, 5])
print(output)
