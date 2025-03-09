# 在这里写各个模块的断言并输出log
from press.conf import use_logger
from press.common import ps_log
from press.common import ProductsCsv, compare_dicom_meta
from press.DTO import ProductDataClass


logger = use_logger()
pv = ProductsCsv()
pdc = ProductDataClass()
products = {'coronary': [pdc.coronary_session, pdc.coronary_cases],
            'cerebral': [pdc.cerebral_session, pdc.cerebral_cases],
            'calcium': [pdc.calcium_session, pdc.calcium_cases],
            'thoracic': [pdc.thoracic_session, pdc.thoracic_cases]}


def cp_str(old, new):
    if type(old) != type(new):
        logger.info(f"old {old}, new {new}")
        logger.info('compare data is not the same type')
        return False
    if old == new:
        return True
    return False


def compare_case_count(product):
    logger.info(f" {product} start to compare_case_count ")
    shape_count, v_list = pv.shape_product(product)
    case_count = pdc.select_case_count(products[product][0], products[product][1])
    sn = len(shape_count['product_index'])
    res = cp_str(sn, case_count)
    if not res:
        ps_log(f'compare_case_count count case num error csv: {sn}, mysql: {case_count} !!!', product)
    else:
        ps_log("compare_case_count count case num pass", product)


def compare_dicom_info(product):
    result = True
    logger.info(f" {product} compare_dicom_info ")
    dicoms = pv.get_dicom(product)
    rev = compare_dicom_meta(dicoms, product, products[product][0], products[product][1])
    if not rev:
        result = False
    return result


def dicom_assert():
    product = 'dicom'

    def compare_dicom_case_count():
        count = pv.shape_product('dicom')
        test_count = pdc.select_dicom_count()
        res = cp_str(test_count, len(count[1]))
        if not res:
            ps_log(f'compare_case_count count case num error csv:{len(count[1])}, mysql: {test_count} !!!', product)
        else:
            ps_log("compare_case_count count case num pass ", product)

    def compare_case_state():
        state = pdc.select_plt_state()
        if state == 0:
            ps_log(f'compare_case_state case state error !!!', product)
        else:
            ps_log("compare_case_state count case num pass", product)

    # 查看平台病例分发应用状态
    def dicom_compare_coronary_count():
        product_count = pv.shape_product('coronary')
        test_count = pdc.select_dicom_coronary()
        pc = len(product_count[0]['product_index'])
        res = cp_str(pc, test_count)
        if not res:
            ps_log(f'dicom_compare_coronary_count case num error csv: {pc}, mysql: {test_count} !!!', product)
        else:
            ps_log("dicom_compare_coronary_count case num pass", product)

    def compare_cerebral_pull_count():
        cer_count = pdc.select_dicom_pull_cerebral()
        if int(cer_count) != 20:
            ps_log(f'compare_cerebral_pull_count error, mysql:{cer_count} !!!', product)
        else:
            ps_log("compare_cerebral_pull_count pass", product)

    compare_dicom_case_count()
    compare_case_state()
    dicom_compare_coronary_count()
    compare_cerebral_pull_count()


def products_assert():
    for p in products:
        compare_case_count(p)
        compare_dicom_info(p)
        logger.info(f"check {p} finish")
