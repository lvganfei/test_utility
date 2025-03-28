
def candy(ratings):
    """
    :type ratings: List[int]
    :rtype: int
    """
    sum = 0
    max_idx = 0
    min_idx = 0
    equal_count = 0
    for i in range(1,len(ratings)):
        print('i=' + str(i))
        
        if ratings[i] > ratings[i-1]:
        #判断是否连续上升，是否要换方向
            equal_count = 0
            

            if max_idx == i-1:
                print("连续上升，继续")
                if i == len(ratings)-1:
                    print('连续上升到最后一个')
                    
                    n = i - min_idx + 1
                    sum = sum + n*(n+1)/2 + n
                    print('sum=' + str(sum))
                else:
                    max_idx=i

            else:
                print('下降趋势结束,以上一个位置i-1结算')
                n = min_idx - max_idx + 1
                sum = sum + n*(n+1)/2 
                print('sum=' + str(sum))

                if i == len(ratings)-1:
                    
                    sum = sum + 2
                    print('sum=' + str(sum))
                else:
                    max_idx = i
                    min_idx = i
        elif ratings[i] < ratings[i-1]:
        #判断是否连续下降，是否要换方向
            equal_count = 0
            
            
            if min_idx == i-1:
                print("连续下降，继续")

                if i == len(ratings)-1:
                    print('处理连续下降最后一个')
                    
                    n = i - max_idx + 1
                    print(n)
                    sum = sum + n*(n+1)/2
                    print('sum=' + str(sum))
                else:
                    min_idx=i
        
            else:
                #换向了,结算
                print('上升趋势结束,以上一个位置i-1结算')
                n = max_idx - min_idx + 1
                sum = sum + n*(n+1)/2
                print('sum=' + str(sum))

                if i == len(ratings)-1:
                    print('最后一个换成下降方向')
                    
                    sum = sum + 1
                    print('sum=' + str(sum))
                else:
                    max_idx = i
                    min_idx = i
        else:
            #ratings[i] == ratings[i-1]
            print('ratings[i] == ratings[i-1]')
            #先结算之前的
            equal_count = equal_count + 1
            if equal_count == 1:
                print('1个连续相等，结算之前')
                print('---max_idx=' + str(max_idx))
                print('---min_idx=' + str(min_idx))
                n = abs(max_idx - min_idx) + 1
                sum = sum + n*(n+1)/2
                if i == len(ratings)-1:
                    sum = sum + 1
            else:    
                print('多个连续相等，结算本体')
                #加本体
                sum = sum + 1
            print('sum=' + str(sum))
            max_idx = i
            min_idx = i
            
            
            

        print('max_idx=' + str(max_idx))
        print('min_idx=' + str(min_idx))
    return int(sum)


# a = [5,4,3,2,1,0,1,2,3,4,5]
# a = [1,0,2]
# a=[1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1]
# a = [1,2,2]
# a = [5,4,3,2,1,0,0,0]
# a=[1,3,4,5,2]
a=[1,6,10,8,7,3,2]

print(candy(a))