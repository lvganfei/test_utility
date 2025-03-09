import csv
import dataclasses
import datetime
import json
import logging
import math
import uuid
from io import StringIO
from typing import (
    Optional,
    List,
    Dict,
    Tuple,
)

import dacite
import inject
import mashumaro
from sqlalchemy import or_

from app.dependencies import CacheRedis, MainDBSession
from app.models.case import Case
from app.services.pneumonia import get_pneumonia_info, get_pneumonia_info_resp
from app.services.thoracic import get_meta_simple
from app.utils.common import get_dicom_from_output
from app.utils.translate import Translate

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class PneumoniaExportReq(mashumaro.DataClassDictMixin):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    search_text: Optional[str] = None
    case_num_arr: Optional[List[str]] = None
    lng: str = 'en'


def get_pneumonia_result_map(translate: Translate) -> Dict[int, str]:
    _ = translate.gettext
    return {
        3: _('疑似病毒性肺炎'),
        2: _('疑似非病毒性肺炎'),
        1: _('未见肺炎'),
    }


def get_pneumonia_sub_result_map(translate: Translate) -> Dict[Tuple[int, int], str]:
    _ = translate.gettext
    return {
        (3, 1): _('其他病毒性肺炎'),
        (3, 2): _('疑似新冠肺炎'),

        (2, 1): _('细菌性肺炎'),
        (2, 2): _('真菌性肺炎'),
        (2, 3): _('非典型病原体肺炎'),
        (2, 4): _('结核及其他'),
    }


def get_pneumonia_export_filename(export_key: str):
    redis_cli = inject.instance(CacheRedis)
    req = dacite.from_dict(PneumoniaExportReq, json.loads(redis_cli.get(export_key)))
    start_date = datetime.datetime.strptime(req.start_date, '%Y-%m-%d')
    start_date_str = start_date.strftime('%Y%m%d')
    end_date = datetime.datetime.strptime(req.end_date, '%Y-%m-%d') - datetime.timedelta(days=1)
    end_date_str = end_date.strftime('%Y%m%d')
    return f'NCP-{start_date_str}-{end_date_str}.csv'


def d(a, b):
    if b == 0:
        return math.nan
    else:
        return a / b


def export_pneumonia_data(export_key: str):
    from app.services.pneumonia import CT_RANGE_ARR
    redis_cli = inject.instance(CacheRedis)
    req = PneumoniaExportReq.from_dict(json.loads(redis_cli.get(export_key)))
    session = inject.instance(MainDBSession)
    if req.case_num_arr:
        case_arr: List[Case] = session.query(Case).filter(
            Case.state == Case.GENERATED,
            Case.case_num.in_(req.case_num_arr)
        ).all()
    else:
        q = session.query(Case).filter(
            Case.state == Case.GENERATED,
            Case.study_datetime >= datetime.datetime.strptime(req.start_date, '%Y-%m-%d'),
            Case.study_datetime < datetime.datetime.strptime(req.end_date, '%Y-%m-%d'),
        )
        if req.search_text:
            search_text = f'%{req.search_text}%'
            q = q.filter(
                or_(
                    Case.patient_name.like(search_text),
                    Case.patient_num.like(search_text),
                )
            )
        case_arr = q.order_by(Case.study_datetime.desc()).all()
    output = StringIO()
    writer = csv.writer(output)
    translate = Translate(req.lng)
    _ = translate.gettext
    encoding = translate.get_encoding_recommendation()
    header_row = [
        _('姓名'), _('患者ID'), _('性别'), _('出生日期'),
        _('检查时间'), _('序列名称'),
        _('诊断意见'), _('肺炎分类'),

        _('全肺容积（cm3）'), _('左肺容积（cm3）'), _('右肺容积（cm3）'),
        _('左肺上叶容积（cm3）'), _('左肺下叶容积（cm3）'),
        _('右肺上叶容积（cm3）'), _('右肺中叶容积（cm3）'), _('右肺下叶容积（cm3）'),

        _('全肺炎症病灶体积（cm3）'),
        _('左肺炎症病灶体积（cm3）'), _('右肺炎症病灶体积（cm3）'),
        _('左肺上叶炎症病灶体积（cm3）'), _('左肺下叶炎症病灶体积（cm3）'),
        _('右肺上叶炎症病灶体积（cm3）'), _('右肺中叶炎症病灶体积（cm3）'), _('右肺下叶炎症病灶体积（cm3）'),

        _('全肺炎症病灶体积/全肺容积（%）'),
        _('左肺炎症病灶体积/全肺容积（%）'),
        _('右肺炎症病灶体积/全肺容积（%）'),
        _('左肺上叶炎症病灶体积/全肺容积（%）'),
        _('左肺下叶炎症病灶体积/全肺容积（%）'),
        _('右肺上叶炎症病灶体积/全肺容积（%）'),
        _('右肺中叶炎症病灶体积/全肺容积（%）'),
        _('右肺下叶炎症病灶体积/全肺容积（%）'),
        _('左肺炎症病灶体积/左肺容积（%）'),
        _('右肺炎症病灶体积/右肺容积（%）'),
        _('左肺上叶炎症病灶体积/左肺上叶容积（%）'),
        _('左肺下叶炎症病灶体积/左肺下叶容积（%）'),
        _('右肺上叶炎症病灶体积/右肺上叶容积（%）'),
        _('右肺中叶炎症病灶体积/右肺中叶容积（%）'),
        _('右肺下叶炎症病灶体积/右肺下叶容积（%）'),

        _('全肺炎症病灶平均密度（Hu）'), _('左肺炎症病灶平均密度（Hu）'), _('右肺炎症病灶平均密度（Hu）'),
        _('左肺上叶炎症病灶平均密度（Hu）'), _('左肺下叶炎症病灶平均密度（Hu）'),
        _('右肺上叶炎症病灶平均密度（Hu）'), _('右肺中叶炎症病灶平均密度（Hu）'), _('右肺下叶炎症病灶平均密度（Hu）'),
    ]
    for position in [
            _('全肺{}肺炎病灶(cm3)'), _('左肺{}肺炎病灶(cm3)'), _('右肺{}肺炎病灶(cm3)'), _('左肺上叶{}肺炎病灶(cm3)'),
            _('左肺下叶{}肺炎病灶(cm3)'), _('右肺上叶{}肺炎病灶(cm3)'), _('右肺中叶{}肺炎病灶(cm3)'),
            _('右肺下叶{}肺炎病灶(cm3)')]:
        for range_start, range_end in CT_RANGE_ARR:
            if math.isinf(range_end):
                label = f">{range_start}"
            else:
                label = f"{range_start}~{range_end}"
            label = position.format(label)
            header_row.append(label)
    writer.writerow(header_row)
    yield output.getvalue().encode(encoding)
    output.seek(0)
    output.truncate(0)
    pneumonia_result_map = get_pneumonia_result_map(translate)
    pneumonia_sub_result_map = get_pneumonia_sub_result_map(translate)
    for case in case_arr:
        try:
            dicom_file = get_dicom_from_output(case.case_num)
            info = get_pneumonia_info(case.case_num)
            if not info:
                continue
            meta = get_meta_simple(case.case_num)
            birth_date = dicom_file.PatientBirthDate
            if birth_date:
                birth_date = str(birth_date)
            else:
                birth_date = ''
            pneumonia_result = pneumonia_result_map.get(case.pneumonia_result, '')
            pneumonia_sub_result = pneumonia_sub_result_map.get((case.pneumonia_result, case.pneumonia_sub_result), '')

            data = []
            # 肺体积
            for key in ['lung', 'left_lung', 'right_lung', '4', '5', '1', '2', '3']:
                data.append(info.statistics_info[key].lung_volume * 1000)
            # 病灶体积
            for key in ['lung', 'left_lung', 'right_lung', '4', '5', '1', '2', '3']:
                data.append(info.statistics_info[key].volume * 1000)
            # 炎症/全肺容积(%)
            for key in ['lung', 'left_lung', 'right_lung', '4', '5', '1', '2', '3']:
                data.append(d(info.statistics_info[key].volume, info.statistics_info['lung'].lung_volume) * 100)
            # 炎症/部位容积(%)
            for key in ['left_lung', 'right_lung', '4', '5', '1', '2', '3']:
                data.append(d(info.statistics_info[key].volume, info.statistics_info[key].lung_volume) * 100)
            # 平均密度
            for key in ['lung', 'left_lung', 'right_lung', '4', '5', '1', '2', '3']:
                data.append(info.statistics_info[key].ct_average)

            info_resp = get_pneumonia_info_resp(meta, info)
            del info
            for key in ['lung', 'left_lung', 'right_lung', '4', '5', '1', '2', '3']:
                for ct_range_x in info_resp.ct_range[key]:
                    data.append(ct_range_x.volume)
            data_str_arr = []
            for x in data:
                if math.isnan(x):
                    data_str_arr.append('')
                else:
                    data_str_arr.append(f'{x:.2f}')
            writer.writerow([
                case.patient_name, case.patient_num, case.patient_sex, birth_date,
                case.study_datetime.strftime('%Y-%m-%d %H:%M:%S'), case.series_description,
                pneumonia_result, pneumonia_sub_result,
            ] + data_str_arr)
            yield output.getvalue().encode(encoding)

            output.seek(0)
            output.truncate(0)
        except KeyboardInterrupt:
            raise
        except Exception:  # qa
            logger.warning(f'failed to export {case.case_num}', exc_info=True)


def create_pneumonia_data_export(start_date: datetime.datetime, end_date: datetime.datetime, search_text: str,
                                 case_num_arr: List[str], lng='en') -> str:
    redis_cli = inject.instance(CacheRedis)
    export_key = f'ncp-export-{uuid.uuid4().hex}'
    redis_cli.set(export_key, json.dumps(dataclasses.asdict(
        PneumoniaExportReq(
            start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'),
            search_text,
            case_num_arr,
            lng
        ))), 3600)
    return export_key
