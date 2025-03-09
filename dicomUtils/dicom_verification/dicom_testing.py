import yaml
import sys
import os
import pydicom

if len(sys.argv) >= 3:
    path = sys.argv[2]
    product = sys.argv[1]

with open('conf.yaml', 'r') as conf_dicom:
    conf = yaml.load(conf_dicom, yaml.FullLoader)

cta = conf.get(product)
product_list = []
for one_key in cta:
    product_list.append(one_key)  # 字段


def test_dcm():
    dir_list = os.listdir(path)
    image = 0
    for case_images in dir_list:
        if case_images.endswith('.dcm'):  # 判断是否为dcm文件
            image += 1
            dcm_path = os.path.join(path, case_images)
            dcm = pydicom.read_file(dcm_path)
            photometricinterpretation = dcm.get('PhotometricInterpretation')
            cpr_type = dcm.get('SeriesDescription')
            try:
                seriesdescription = cpr_type.split(" ")[1]
            except IndexError:
                seriesdescription = 'ALL'
            if photometricinterpretation == 'RGB':  # 判断图片颜色
                print('***************************', case_images, '***************************', end='')
                print('RGB')
                for one_product in product_list:
                    rgb_each = conf[product][one_product]
                    if rgb_each['type_photometricinterpretation'] == 'ALL' or rgb_each['type_photometricinterpretation'] == 'RGB':  # 判断字段需要验证图片的类型
                        rgb_key = dcm.dir(one_product)
                        rgb_len = len(rgb_key)
                        if rgb_len == 0:  # 判断字段是否为空
                            print(one_product, "??????????????????无字段?????????????????")
                        else:
                            print(one_product, ' ', end='')
                        if rgb_each['value'] == 'True':  # “True”代表验证字段内容是否为空；如要需要验证具体内容请写详细内容
                            try:
                                rgb_value = str(dcm.get(one_product))
                                rgb_value_len = len(rgb_value)
                                if rgb_value == 'None':
                                    print('??????????????????无内容??????????????????')
                                elif rgb_value_len == 0:
                                    print('??????????????????无内容??????????????????')
                                elif rgb_value_len != 0:
                                    print('有内容:', rgb_value, ' ', end='')
                            except KeyError:
                                print('??????????????????无内容??????????????????')
                        else:  # “True”代表验证字段内容是否为空；如要需要验证具体内容请写详细内容
                            rgb_value = str(dcm.get(one_product))
                            if rgb_each['value'] == rgb_value:
                                print('内容正确:', rgb_value, ' ', end='')
                            else:
                                print('??????????????????内容错误??????????????????', '真确的是:', rgb_each['value'], '实际上的是:', rgb_value)
                        if rgb_each['value_decimal'] != False:  # 验证小数点后多少位，需要多少位写多少位，不需要验证不用写这条
                            rgb_decimal_key = dcm.get(one_product)
                            print('正确保留位数:', rgb_each['value_decimal'], '实际保留位数:', end='')
                            for rgb_decimal_sy in rgb_decimal_key:
                                rgb_decimal = str(rgb_decimal_sy)
                                try:
                                    if len(rgb_decimal.split('.')[1]) <= rgb_each['value_decimal']:
                                        print(len(rgb_decimal.split('.')[1]), ',', end='')
                                    else:
                                        print('验证小数内容:', rgb_decimal, '??????????????????小数点大于??????????????????', rgb_each['value_decimal'], '位',
                                              '实际小数点位数:', len(rgb_decimal.split('.')[1]))
                                except IndexError:
                                    if len(rgb_decimal) <= rgb_each['value_decimal']:
                                        print(len(rgb_decimal.split('.')[0]), ',', end='')
                                    else:
                                        print('验证小数内容:', rgb_decimal, '??????????????????小数点大于??????????????????',
                                              rgb_each['value_decimal'], '位',
                                              '实际小数点位数:', len(rgb_decimal.split('.')[0]))
                            print('')
                        else:
                            print('不验证内容长度')
                    else:
                        continue

            elif photometricinterpretation == 'MONOCHROME2':  # 判断图片颜色
                print('***************************', case_images, '***************************', end='')
                print('MONOCHROME2 ', end='')
                if seriesdescription == 'VR':  # 判断图片类型
                    print('VR ')
                    for two_product in product_list:
                        mono_each = conf[product][two_product]
                        if mono_each['type_seriesdescription'] == 'ALL' or mono_each['type_seriesdescription'] == 'VR':  # 判断字段需要验证的类型
                            if mono_each['type_photometricinterpretation'] == 'ALL' or mono_each['type_photometricinterpretation'] == 'MOMO2':  # 判断字段需要验证颜色
                                mono_key = dcm.dir(two_product)
                                mono_len = len(mono_key)
                                if mono_len == 0:  # 判断字段是否为空
                                    print(two_product, "??????????????????无字段?????????????????")
                                else:
                                    print(two_product, ' ', end='')
                                if mono_each['value'] == 'True':  # “True”代表验证字段内容是否为空；如要需要验证具体内容请写详细内容
                                    try:
                                        mono_value = str(dcm.get(two_product))
                                        mono_value_len = len(mono_value)
                                        if mono_value == 'None':
                                            print('??????????????????无内容??????????????????')
                                        elif mono_value_len == 0:
                                            print('??????????????????无内容??????????????????')
                                        elif mono_value_len != 0:
                                            print('有内容:', mono_value, ' ', end='')
                                    except KeyError:
                                        print('??????????????????无内容??????????????????')
                                else:  # “True”代表验证字段内容是否为空；如要需要验证具体内容请写详细内容
                                    mono_value = str(dcm.get(two_product))
                                    if mono_each['value'] == mono_value:
                                        print('内容正确:', mono_value, ' ',  end='')
                                    else:
                                        print('??????????????????内容错误??????????????????', '真确的是:', mono_each['value'], '实际上的是:', mono_value)
                                if mono_each['value_decimal'] != False:  # 验证小数点后多少位，需要多少位写多少位，不需要验证不用写这条
                                    mono_decimal_key = dcm.get(two_product)
                                    print('正确保留位数:', mono_each['value_decimal'], '实际保留位数:', end='')
                                    for mono_decimal_sy in mono_decimal_key:
                                        mono_decimal = str(mono_decimal_sy)
                                        try:
                                            if len(mono_decimal.split('.')[1]) <= mono_each['value_decimal']:
                                                print(len(mono_decimal.split('.')[1]), ',', end='')
                                            else:
                                                print('验证小数内容:', mono_decimal,
                                                      '??????????????????小数点大于??????????????????',
                                                      mono_each['value_decimal'], '位',
                                                      '实际小数点位数:', len(mono_decimal.split('.')[1]))
                                        except IndexError:
                                            if len(mono_decimal) <= mono_each['value_decimal']:
                                                print(len(mono_decimal.split('.')[0]), ',', end='')
                                            else:
                                                print('验证小数内容:', mono_decimal,
                                                      '??????????????????小数点大于??????????????????',
                                                      mono_each['value_decimal'], '位',
                                                      '实际小数点位数:', len(mono_decimal.split('.')[0]))
                                    print('')
                                else:
                                    print('不验证内容长度')

                        else:
                            continue
                else:  # 判断图片颜色"CPR/LUMEN/MIP......"
                    print('CPR/LUMEN/MIP...... ')
                    for three_product in product_list:
                        cpr_each = conf[product][three_product]
                        if cpr_each['type_seriesdescription'] == 'ALL' or cpr_each['type_seriesdescription'] == 'CPR/LUMEN':  # 字段需要判断图片类型
                            if cpr_each['type_photometricinterpretation'] == 'ALL' or cpr_each['type_photometricinterpretation'] == 'MOMO2':  # 字段需要判断图片颜色
                                cpr_key = dcm.dir(three_product)
                                cpr_len = len(cpr_key)
                                if cpr_len == 0:
                                    print(three_product, "??????????????????无字段?????????????????")
                                else:
                                    print(three_product, ' ', end='')
                                if cpr_each['value'] == 'True':
                                    try:
                                        cpr_value = str(dcm.get(three_product))
                                        cpr_value_len = len(cpr_value)
                                        if cpr_value == 'None':
                                            print('??????????????????无内容??????????????????')
                                        elif cpr_value_len == 0:
                                            print('??????????????????无内容??????????????????')
                                        elif cpr_value_len != 0:
                                            print('有内容:', cpr_value, ' ', end='')
                                    except KeyError:
                                        print('??????????????????无内容??????????????????')
                                else:
                                    cpr_value = str(dcm.get(three_product))
                                    if cpr_each['value'] == cpr_value:
                                        print('内容正确:', cpr_value, ' ', end='')
                                    else:
                                        print('??????????????????内容错误??????????????????', '正确的是:', cpr_each['value'], '实际上的是:', cpr_value)
                                if cpr_each['value_decimal'] != False:
                                    cpr_decimal_key = dcm.get(three_product)
                                    print('正确保留位数:', cpr_each['value_decimal'], '实际保留位数:', end='')
                                    for cpr_decimal_sy in cpr_decimal_key:
                                        cpr_decimal = str(cpr_decimal_sy)
                                        try:
                                            if len(cpr_decimal.split('.')[1]) <= cpr_each['value_decimal']:
                                                print(len(cpr_decimal.split('.')[1]), ',',  end='')

                                            else:
                                                print('验证小数内容:', cpr_decimal,
                                                      '??????????????????小数点大于??????????????????',
                                                      cpr_each['value_decimal'], '位',
                                                      '实际小数点位数:', len(cpr_decimal.split('.')[1]))
                                        except IndexError:
                                            if len(cpr_decimal) <= cpr_each['value_decimal']:
                                                print(len(cpr_decimal.split('.')[0]), ',', end='')
                                            else:
                                                print('验证小数内容:', cpr_decimal,
                                                      '??????????????????小数点大于??????????????????',
                                                      cpr_each['value_decimal'], '位',
                                                      '实际小数点位数:', len(cpr_decimal.split('.')[0]))
                                    print('')
                                else:
                                    print('不验证内容长度')
                        else:
                            continue

    print(' ', '总验证数量：', image)


if __name__ == '__main__':
    test_dcm()
