import numpy as np



# def inner_multiply(a, b):
#     return np.dot(a, b)

# def externel_multiply(a,b):
#     return np.multiply(a,b)



a = np.array([1,2,3,4])
b = np.tile(a,(4,1))
c = np.repeat(a,repeats=4, axis=0)
# print(b)
# print(c)
def productExceptSelf(nums):
    """
    :type nums: List[int]
    :rtype: List[int]
    """
    length = len(nums)
    zero_idx = []
    multip_res = 1
    result = []
    for i in range(length):
        if nums[i] == 0:
            zero_idx.append(i)
            continue
        else:
            multip_res = multip_res *nums[i]

    print(zero_idx)
    if len(zero_idx) > 1:
        result =  np.zeros(length,dtype=int).tolist()
    elif len(zero_idx) == 1:
        result = np.zeros(length,dtype=int).tolist()
        result[zero_idx[0]] = multip_res
        
    else:
        for k in nums:
            result.append(int(multip_res/k))
    return result


for j in [[1,2,3,4],[-1,1,0,-3,3],[-1,1,0,-3,0]]:
    print(productExceptSelf(j))