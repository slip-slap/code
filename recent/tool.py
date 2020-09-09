import copy
"""
argument: [1,3,2]
return  : [1,3,2,2,3,1]
"""
def get_symmetry_list(half_list):
    upper_half = copy.deepcopy(half_list)
    half_list.reverse()
    return upper_half + half_list

def get_positive(a_list):
    pos = 0
    neg = 0
    for i in range(len(a_list)):
        if a_list[i] > 0:
            pos = pos + 1
        if a_list[i] < 0:
            neg = neg + 1
    print("neg: " + str(neg))
    print("pos: " + str(pos))



if __name__ == '__main__':

    #ma=[-45{gr_9} 45{gr_9}     -45 {ca_2}    45 {ca_2}
                 
    angle=[-45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'carbon_epoxy', -45, 'carbon_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'carbon_epoxy', -45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'graphite_epoxy', 45, 'graphite_epoxy', 45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'carbon_epoxy', -45, 'graphite_epoxy', 45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy', -45, 'carbon_epoxy', 45, 'graphite_epoxy', 45, 'graphite_epoxy', 45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'carbon_epoxy', -45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'carbon_epoxy', 45, 'carbon_epoxy', -45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy', 45, 'graphite_epoxy', -45, 'graphite_epoxy']
    get_positive(angle)


