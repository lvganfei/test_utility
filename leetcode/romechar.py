def intToRoman(num):
        """
        :type num: int
        :rtype: ret
        """
        import math
        char_dict = {
            1: "I",
            4: "IV",
            5: "V",
            9: "IX",
            10: "X",
            40: "XL",
            50: "L",
            90: "XC",
            100: "C",
            400: "CD",
            500: "D",
            900: "CM",
            1000: "M"
        }
        #3749
        #处理千位
        ret = ''
        ret = ret + int(math.floor(num//1000))* char_dict[1000]

        num_str = str(num)
         
        hundred_digit = (0,int(num_str[-3:]))[len(num_str) >= 3]
        ten_digit = (0, int(num_str[-2:]))[len(num_str) >= 2]
        last_digit = (0, int(num_str[-1]))[len(num_str) >= 1]

        #处理百位数字
        n_h = int(math.floor(hundred_digit/100))
        if n_h == 9:
            ret = ret + char_dict[900]
        elif n_h == 4:
            ret = ret + char_dict[400]
        elif 0 <= n_h < 4:
            ret = ret + n_h* char_dict[100]
        else:
            ret = ret + int(math.floor(hundred_digit/500))* char_dict[500] + (n_h - 5)*char_dict[100]

        #处理十位数字
        n_t = math.floor(ten_digit/10)
        if n_t == 9:
            ret = ret + char_dict[90]
        elif n_t == 4:
            ret = ret + char_dict[40]
        elif 0 <= n_t < 4:
            ret = ret + n_t* char_dict[10]
        else:
            ret = ret + math.floor(ten_digit/50)* char_dict[50] + (n_t - 5)*char_dict[10]

        #处理个位数字
        if last_digit == 9:
            ret = ret + char_dict[9]
        elif last_digit == 4:
            ret = ret + char_dict[4]
        elif 0 <= last_digit < 4:
            ret = ret + last_digit* char_dict[1]
        else:
            ret = ret + math.floor(last_digit/5)* char_dict[5] + (last_digit - 5)*char_dict[1]

        return ret


# print(intToRoman(3749))
print(intToRoman(3949))
# print(intToRoman(58))