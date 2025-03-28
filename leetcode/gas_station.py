import numpy as np 

def canCompleteCircuit(gas, cost):
        """
        :type gas: List[int]
        :type cost: List[int]
        :rtype: int
        """
        # 如果cost[i]>gas[i]跳过，否则,gas_sum = gas[i]-cost[i], if gas_sum >0 continue
        length = len(gas)
        gas_remain = 0
        i = 0 
        valid_station = []
        while i<2*length and len(valid_station) < length:
            
            if gas_remain + gas[i%length] > cost[i%length]:
                
                valid_station.append(i%length)
                gas_remain = gas_remain + gas[i%length] - cost[i%length]
                print('gas remain' + str(gas_remain))
            else:
                print( str(i)  + ' not enough gas, next')
                valid_station = []
                gas_remain = 0
                
            i += 1
        print(valid_station)
        if len(valid_station) < length:
            return -1
        else:
            return valid_station[0]