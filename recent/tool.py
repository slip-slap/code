import copy
"""
argument: [1,3,2]
return  : [1,3,2,2,3,1]
"""
def get_symmetry_list(half_list):
    upper_half = copy.deepcopy(half_list)
    half_list.reverse()
    return upper_half + half_list


if __name__ == '__main__':
    result = get_symmetry_list([2,1,0,9])
    print(result)
