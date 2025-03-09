from press.conf import use_logger
from press.depend import (CoronaryDbSession, CerebralDbSession, CalciumDbSession, ThoracicDbSession, DicomDbSession,
                          CoronaryMongo, CerebralMongo, CalciumMongo, ThoracicMongo
                          )
from press.conf import config
from pymongo import ASCENDING


logger = use_logger()


class ProductDataClass(object):
    def __init__(self, url=None):
        self.coronary_db = CoronaryDbSession(url)
        self.cerebral_db = CerebralDbSession()
        self.calcium_db = CalciumDbSession()
        self.thoracic_db = ThoracicDbSession()
        self.dicom_db = DicomDbSession()
        self.coronary_session = self.coronary_db.make_session()
        self.cerebral_session = self.cerebral_db.make_session()
        self.calcium_session = self.calcium_db.make_session()
        self.thoracic_session = self.thoracic_db.make_session()
        self.dicom_session = self.dicom_db.make_session()
        self.coronary_cases = self.coronary_db.table('cases')
        self.cerebral_cases = self.cerebral_db.table('cases')
        self.calcium_cases = self.calcium_db.table('cases')
        self.thoracic_cases = self.thoracic_db.table('cases')
        self.dicom_patient = self.dicom_db.table('patient')
        self.dicom_study = self.dicom_db.table('study')
        self.dicom_series = self.dicom_db.table('series')
        self.dicom_apply_record = self.dicom_db.table('apply_record')

    @staticmethod
    def select_case(class_list, session, cases):
        values = [v[vb].strip(' ') for v in class_list for vb in v]
        res = session.query(cases).filter(cases.patient_num == values[0]).\
            filter(cases.patient_name == values[1]).\
            filter(cases.series_description == values[2]).\
            filter(cases.study_identifier == values[3]).first()
        session.commit()
        if res:
            return True
        return False

    @staticmethod
    def select_case_count(session, cases):
        res = session.query(cases.patient_num).count()
        session.commit()
        return res

    def select_dicom_count(self):
        res = self.dicom_session.query(self.dicom_series.series_instance_uid).count()
        self.dicom_session.commit()
        return res

    def select_plt_state(self):
        res = self.dicom_session.query(self.dicom_series).filter(
            self.dicom_series.state.in_(['UNAPPLY', 'DELETED'])).count()
        self.dicom_session.commit()
        return res

    def select_dicom_coronary(self):
        res = self.dicom_session.query(self.dicom_apply_record).filter(
            self.dicom_apply_record.applied_service == 'coronary').count()
        self.dicom_session.commit()
        return res

    def select_dicom_cerebral(self):
        res = self.dicom_session.query(self.dicom_apply_record).filter(
            self.dicom_apply_record.apply_record == 'cerebral').count()
        self.dicom_session.commit()
        return res

    def select_dicom_pull_cerebral(self):
        res = self.dicom_session.query(self.dicom_series).filter(
            self.dicom_series == 'ORTHANC').count()
        self.dicom_session.commit()
        return res

    @staticmethod
    def check_case_completed(session, case):
        res = session.query(case).filter(case.state.in_([1, 11])).count()
        session.commit()
        res = True if res == 0 else False
        return res

    @staticmethod
    def init_cases(session, case):
        session.query(case).filter(case.state != 0).delete()
        session.commit()

    def init_dicom(self):
        self.dicom_session.query(self.dicom_patient).delete()
        self.dicom_session.query(self.dicom_study).delete()
        self.dicom_session.query(self.dicom_series).delete()
        self.dicom_session.query(self.dicom_apply_record).delete()
        self.dicom_session.commit()

    @staticmethod
    def get_mysql_calculate(engine):
        return engine.execute(
            "select case_num, " +
            "image_count, " +
            "alg_start_at, " +
            "finish_time, " +
            "avg(unix_timestamp(finish_time) - unix_timestamp(alg_start_at))as used_time " +
            "from cases " +
            "where state !=6 and " +
            "image_count !=0  and " +
            "alg_finish_at is not null and " +
            "finish_time > alg_start_at  " +
            "group by case_num;"
        )


class PressMongo:
    def __init__(self):
        self.coronary = CoronaryMongo(config.CORONARY_MONGO_URI)
        self.cerebral = CerebralMongo(config.CEREBRAL_MONGO_URI)
        self.calcium = CalciumMongo(config.CALCIUM_MONGO_URI)
        self.thoracic = ThoracicMongo(config.THORACIC_MONGO_URI)

    def remove_all_products(self):
        self.coronary.db.metas.drop()
        self.cerebral.db.metas.drop()
        self.calcium.db.metas.drop()
        self.thoracic.db.metas.drop()
        self.coronary.db.reports.drop()
        self.cerebral.db.reports.drop()
        self.calcium.db.reports.drop()
        self.thoracic.db.reports.drop()

    def create_all_products(self):
        self.coronary.db.metas.create_index([('case_num', ASCENDING)], unique=True)
        self.coronary.db.reports.create_index([('case_num', ASCENDING)], unique=True)
        self.cerebral.db.metas.create_index([('case_num', ASCENDING)], unique=True)
        self.cerebral.db.reports.create_index([('case_num', ASCENDING)], unique=True)
        self.calcium.db.metas.create_index([('case_num', ASCENDING)], unique=True)
        self.calcium.db.reports.create_index([('case_num', ASCENDING)], unique=True)
        self.thoracic.db.metas.create_index([('case_num', ASCENDING)], unique=True)
        self.thoracic.db.reports.create_index([('case_num', ASCENDING)], unique=True)
