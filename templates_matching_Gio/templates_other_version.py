#another version of the templates 
# made by Giovanni Concheri, for the templates matching

import re
import numpy as np

# def string_to_list(string):
#     # Split the string into lines
#     lines = string.splitlines()
#     # Take lines from the fourth onward
#     relevant_lines = lines[3:]
#     # List to store extracted elements
#     elements = []
#     for line in relevant_lines:
#         # Split by ';', strip whitespace, and ignore empty parts
#         parts = [part.strip() for part in line.split(';') if part.strip()]
#         elements.extend(parts)
#     return elements


def extract_elements(string):
    lines = string.splitlines()[3:]  # Skip first three lines
    result = []
    label_pattern = re.compile(r'^(\w+)\s*((?:q\[\d+\],?\s*)+);?$')
    number_pattern = re.compile(r'q\[(\d+)\]')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = label_pattern.match(line)
        if match:
            label = match.group(1)
            numbers = [int(n) for n in number_pattern.findall(match.group(2))]
            result.append([label] + numbers)
    return result

# def find_valid_cx_triplets(lst):
#     # Step 1: Find all cx sublists and their indices
#     cx_indices = [(i, item) for i, item in enumerate(lst) if item[0] == 'cx']
#     triplets = []
#     # Step 2: Group them in triplets
#     for i in range(len(cx_indices) - 2):
#         group = cx_indices[i:i+3]
#         indices = [idx for idx, _ in group]
#         cx_numbers = set()
#         for _, item in group:
#             cx_numbers.update(item[1:])
#         # Step 3: Check for interfering sublists
#         start, end = indices[0], indices[2]
#         interfering = False
#         for j in range(start, end + 1):
#             if lst[j][0] != 'cx':
#                 numbers = set(lst[j][1:])
#                 if cx_numbers & numbers:
#                     interfering = True
#                     break
#         if not interfering:
#             triplets.append([item for _, item in group])
#     return triplets


def find_cx_triplets(lst, toffoli):
    # Step 1: Collect all cx sublists and their indices
    cx_indices = [(i, item) for i, item in enumerate(lst) if item[0] == 'cx']
    triplets = []
    # Step 2: Find all triplets with overlapping numbers
    n = len(cx_indices)

    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):

                idx1, cx1 = cx_indices[i]
                idx2, cx2 = cx_indices[j]
                idx3, cx3 = cx_indices[k]

                nums1 = cx1[1:]
                nums2 = cx2[1:]
                nums3 = cx3[1:]

                array, pair = toffoli

                cond1 = nums1[array[0,0]] == nums2[array[0,1]]
                cond2 = nums2[array[1,0]] == nums3[array[1,1]]
                cond3 = nums3[array[2,0]] == nums1[array[2,1]]
                cond4 = nums1[pair[0]] != nums2[pair[1]]

                if cond1 and cond2 and cond3 and cond4:
                    indices = sorted([idx1, idx2, idx3])

                    # Intervallo tra la prima e la seconda sublist (esclusi gli estremi)
                    for el in lst[indices[0]+1:indices[1]]:
                        if any(num in nums1 for num in el[1:]):
                            break  # Esci: c'è sovrapposizione tra 1 e 2
                    else:
                        # Intervallo tra la seconda e la terza sublist (esclusi gli estremi)
                        for el in lst[indices[1]+1:indices[2]]:
                                if any(num in nums3 for num in el[1:]):
                                    break  # Esci: c'è sovrapposizione tra 2 e 3
                        else:
                            # Solo se nessun break è avvenuto, aggiungi il triplet
                            triplets.append([cx1, cx2, cx3])
    return triplets

# list_of_ops = [['x', 0], ['z', 1], ['cx', 0, 4], ['cx', 1, 2], ['cx', 3, 4], ['cx', 3, 0], ['z', 4]]

# a = np.array([[1,1],[0,0],[1,0]])

# triplets = find_cx_triplets(list_of_ops,a)
# print(triplets)


toffoli = {
    0: [np.array([[1,1],[0,0],[1,0]]), (0,0)],
    1: [np.array([[0,1],[1,0],[1,1]]), (0,0)],
    2: [np.array([[1,0],[0,1],[0,0]]), (0,1)]
    
    }

list_of_ops = [['x', 0], ['z', 1], ['cx', 2, 3], ['cx', 3, 4], ['cx', 0, 1], ['z', 4], ['cx', 2, 3]]
triplets = find_cx_triplets(list_of_ops,toffoli[2])
print(triplets)
