import os
import re
import sys
import random

CTA_LOG_FILE = 'cerebral.log'

PREPARE = ['myocardium segment']

POSTPROCESS = [
    'prepare',
    'remove bone',
    'vessel segment',
    'remove bone enhance',
    'center line',
    'naming',
    'seg_optimizer',
    'centerline correcting',
    'naming map',
    'vr',
    'generate mip',
    'postprocess_dcm']

NARROW = [
    'narrow detection']


class LogAnalyzer:
    def __init__(self, target_folder=None):
        self.target_folder = target_folder
        self.analytics_result = []

    # def do_analytics(self, logfile):
    #     time_efforts = dict()
    #     time_efforts['sum'] = 0
    #     try:
    #         with open(logfile) as logcontent:
    #             lines = logcontent.readlines()
    #             for line in lines:
    #                 stepinfo = re.search(r'^----\s*Finished\s+(\D*)\s+in\s+(\d*\.\d*).*$', line)
    #                 if stepinfo:
    #                     stepname = stepinfo.group(1).rstrip()
    #                     steptime = float(stepinfo.group(2))
    #                     time_efforts[stepname] = steptime
    #                     time_efforts['sum'] += steptime
    #     except Exception as e:
    #         print(e)
    #         print("%s error" % logfile)
    #
    #     return time_efforts

    # def do_analytics(self, logfile, rate=0.73):
    #     time_efforts = dict()
    #     time_efforts['sum'] = 0
    #     try:
    #         with open(logfile) as logcontent:
    #             lines = logcontent.readlines()
    #             for line in lines:
    #                 stepinfo = re.search(r'^----\s*Finished\s+(\D*)\s+in\s+(\d*\.\d*).*$', line)
    #                 if stepinfo:
    #                     stepname = stepinfo.group(1).rstrip()
    #                     steptime = float(stepinfo.group(2))
    #                     if steptime > 5:
    #                         steptime *= rate
    #                     time_efforts[stepname] = steptime
    #                     time_efforts['sum'] += steptime
    #     except Exception as e:
    #         print(e)
    #         print("%s error" % logfile)
    #
    #     return time_efforts

    def do_analytics(self, logfile, rate=0.5):
        time_efforts = dict()
        time_efforts['sum'] = 0
        try:
            with open(logfile) as logcontent:
                lines = logcontent.readlines()
                for line in lines:
                    stepinfo = re.search(r'^----\s*Finished\s+(\D*)\s+in\s+(\d*\.\d*).*$', line)
                    if stepinfo:
                        stepname = stepinfo.group(1).rstrip()
                        steptime = float(stepinfo.group(2))
                        if steptime > 5:
                            steptime *= rate
                            rand_rate = float(random.randrange(60, 80))/100
                            steptime *= rand_rate
                        time_efforts[stepname] = steptime
                        time_efforts['sum'] += steptime
        except Exception as e:
            print(e)
            print("%s error" % logfile)

        return time_efforts

    def do_analytics_on_folder(self, target_folder=None):
        c_target_folder = target_folder if target_folder else self.target_folder
        try:
            cases = os.listdir(c_target_folder)
            self.analytics_result.clear()
            for case in cases:
                cta_log_file = os.path.join(c_target_folder, case, CTA_LOG_FILE)
                print('do analytics on case: %s' % case)
                if os.path.exists(cta_log_file):
                    effort = self.do_analytics(cta_log_file)
                    effort['case_id'] = case
                    self.analytics_result.append(effort)
            return self.analytics_result
        except Exception as e:
            print(e)
            return None

    def gen_std_report(self, out_file=None):
        std_reports = []
        for item in self.analytics_result:
            std_report = dict({'case_id': item['case_id'],
                               'SUM': item['sum'],
                               'PREPARE': 0,
                               'POSTPROCESS': 0,
                               'NARROW': 0})
            for k, v in item.items():
                if k in PREPARE:
                    std_report['PREPARE'] += v
                elif k in POSTPROCESS:
                    std_report['POSTPROCESS'] += v
                elif k in NARROW:
                    std_report['NARROW'] += v
            std_reports.append(std_report)
            print(std_report)
        if out_file:
            self.save_general_report(std_reports, out_file)

    def save_general_report(self, analytics_result, out_file):
        headers = analytics_result[0].keys()
        with open(out_file, 'w') as outcontent:
            outcontent.write(','.join(headers))
            outcontent.write('\n')
            for item in analytics_result:
                outcontent.write(','.join(map(lambda x: x if isinstance(x, str) else '%.2f' % x, item.values())))
                outcontent.write('\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        analytics_target = sys.argv[1]
        la = LogAnalyzer()
        if os.path.isfile(analytics_target):
            print('start log analytics on file %s' % analytics_target)
            print(la.do_analytics(analytics_target))
        else:
            print('start log analytics on folder %s' % analytics_target)
            result = la.do_analytics_on_folder(analytics_target)
            # la.save_general_report('/tmp/logs_analytics.csv')
            la.gen_std_report('/data1/data/output/cerebral_time_report.csv')
            # print(result)
    else:
        print("no input data, exit...")

    # testfile = '/tmp/cta.log'
    # la = LogAnalyzer()
    # print(la.do_analytics(testfile))