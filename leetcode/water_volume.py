def trap(height):
    """
    :type height: List[int]
    :rtype: int
    """
    n = len(height)
    peak_idx = 0
    highest_peak_idx = []
    volume = 0

    for i in range(0,n):
        print('i=' + str(i))
        if i == 0 or i == n-1:
            #最后一个
            print('最后一个')
            if i == n-1 and height[i] > height[i-1]:
                print('最后一个上升')
                peak_idx = n-1
                # if height[i] >= max([height[idx] for idx in peak_idx]):
                #     highest_peak_idx.append(i)
                # volume = volume + min(height[peak_idx],height[i])*(i-peak_idx-1) - sum(height[peak_idx+1:i])
                print('volume=' + str(volume))
            if i == 0 and height[i] > height[i+1]:
                print('第一个高于第二个')
                peak_idx = 0

                # volume = volume + min(height[peak_idx],height[i])*(i-peak_idx-1) - sum(height[peak_idx+1:i])
                # print('volume=' + str(volume))
        else:
            if height[i] > height[i-1] and height[i] > height[i+1]:
                #找到一个peak
                #jisuan volume
                

                # if height[i] >= max([height[idx] for idx in peak_idx]):
                #     highest_peak_idx.append(i)
                print('找到一个peak height[i]: ' + str(height[i]) +' height[i-1] '+ str(height[i-1]))

                if height[i] >= height[peak_idx]:
                    print('找到一个最高的peak')
                    
                    #jisuan volume
                    peak_idx = i
                else:
                    print('continue searching')
                # print('peak_idx=' + str(peak_idx))
                # volume = volume + min(height[peak_idx],height[i])*(i-peak_idx-1) - sum(height[peak_idx+1:i])
                # print('volume=' + str(volume))
                # peak_idx = i
            elif height[i] > height[i-1]:
                #上升趋势
                print('上升趋势')
    print('peak_idx=' + str(peak_idx))
    print('highest_peak_idx=' + str(highest_peak_idx))

    for j in range(0,len(peak_idx)-1):
        if height[peak_idx[j+1]] > height[peak_idx[j]]:

            volume = volume + min(height[peak_idx[j]],height[peak_idx[j+1]])*(peak_idx[j+1]-peak_idx[j]-1) - sum(height[peak_idx[j]+1:peak_idx[j+1]])
        else:
            print('keep searching')
        print('volume=' + str(volume))
    return volume
            
print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))
# print(trap([4,2,0,3,2,5]))