import argparse
import os
import os.path as osp
import pydicom
import csv
from hashlib import md5
import time
import mysql.connector
import pymongo
from pyDes import des, PAD_PKCS5, CBC
import binascii

# import rsa

'''
version:1.1

run脚本之前需要安装这两个包
pip3 install mysql-connector -i https://mirrors.aliyun.com/pypi/simple/
pip3 install pymongo -i https://mirrors.aliyun.com/pypi/simple/
# pip3 install rsa -i https://mirrors.aliyun.com/pypi/simple/
pip3 install pyDes -i https://mirrors.aliyun.com/pypi/simple/
python3 annoymize.py --data-dir=/data1/demo/data  --port=13311 --mongo-port=17022 --products=jupiter --last-record-csv anonymization_20211026001028.csv --anonymize-db-only=true
10.13.4.16 mark1
python3 annoymize.py --data-dir=/data1/mark1/data  --port=13307 --mongo-port=27018 --products=jupiter
10.13.4.16 mark2
python3 annoymize.py --data-dir=/data1/mark2/data  --port=23308 --mongo-port=27019 --products=jupiter
10.13.4.16 mark3
python3 annoymize_1.py --data-dir=/data1/mark3/data  --port=23309 --mongo-port=27020 --products=jupiter
10.13.4.16 mark4
python3 annoymize.py --data-dir=/data1/mark4/data  --port=23310 --mongo-port=27021 --products=jupiter
'''

new_id_prefix = 'sk_'
zhongtai_id_prefix = '9CPn8'
des_key = 'xujiahui'


def parse_args():
    parser = argparse.ArgumentParser()

    # 生成rsa key
    parser.add_argument('--gen-rsa', default='false')

    # 只脱敏dcm的数据
    parser.add_argument('--anonymize-dcm-only', default='false')
    # 需要脱敏的数据目录
    parser.add_argument('--data-dir')

    # data-dir给的目录是不是产品的data目录，如果是会脱敏下面的的original、source、output
    parser.add_argument('--is-product', default='true')

    # 只脱敏数据库数据
    parser.add_argument('--anonymize-db-only', default='false')

    # 脱敏数据库需要的用户名
    parser.add_argument('--username', default='root')

    # 脱敏数据库需要的密码
    parser.add_argument('--password', default='qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj')

    # 脱敏数据库需对应的host
    parser.add_argument('--host', default='127.0.0.1')

    # 脱敏数据库对应的密码
    parser.add_argument('--port', type=int, default=13306)

    # 脱敏mongo需要的用户名
    parser.add_argument('--mongo-username', default='root')

    # 脱敏mongo需要的密码
    parser.add_argument('--mongo-password', default='qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj')

    # 脱敏mongo需要的端口
    parser.add_argument('--mongo-port', type=int, default=17017)

    # 上次的脱敏记录
    parser.add_argument('--last-record-csv')

    # 除了脱敏平台之外还需要脱敏哪些产品
    parser.add_argument('--products')

    args = parser.parse_args()

    return args


# def create_keys():
#     '''
#     生成公钥和私钥
#     :return:
#     '''
#     (pubkey, privkey) = rsa.newkeys(1024)
#     pub = pubkey.save_pkcs1()
#     with open('public.pem', 'wb+')as f:
#         f.write(pub)
#
#     pri = privkey.save_pkcs1()
#     with open('private.pem', 'wb+')as f:
#         f.write(pri)
#     print('generate public.pem、private.pem done.')
#
#
# def encrypt():
#     '''
#     用公钥加密
#     '''
#     with open('public.pem', 'rb') as publickfile:
#         p = publickfile.read()
#     pubkey = rsa.PublicKey.load_pkcs1(p)
#     original_text = 'have a good time'.encode('utf8')
#     crypt_text = base64.b64encode(rsa.encrypt(original_text, pubkey))
#     print(crypt_text.decode('utf-8'))
#     return crypt_text
#
#
# def decrypt(crypt_text):  # 用私钥解密
#     with open('private.pem', 'rb') as privatefile:
#         p = privatefile.read()
#     privkey = rsa.PrivateKey.load_pkcs1(p)
#     lase_text = rsa.decrypt(crypt_text, privkey).decode()  # 注意，这里如果结果是bytes类型，就需要进行decode()转化为str
#
#     print(lase_text)

def encrypt(text):
    if text is None:
        text = ''
    des_ins = des(des_key, CBC, des_key, pad=None, padmode=PAD_PKCS5)
    e_text = des_ins.encrypt(text, padmode=PAD_PKCS5)
    return str(binascii.b2a_hex(e_text), "utf-8")


def decrypt(patient_id, patient_name):
    e_text = patient_id[3:] + patient_name
    des_ins = des(des_key, CBC, des_key, pad=None, padmode=PAD_PKCS5)
    text = des_ins.decrypt(binascii.a2b_hex(e_text), padmode=PAD_PKCS5)
    return str(text, "utf-8")


def link_file(file_path):
    '''
    判断文件是否为连接，如果是责不进行后续处理
    :param file_path:
    :return:
    '''
    '''
    check if link(hard or soft) file
    :param file_path:
    :return:
    '''
    return os.stat(file_path).st_nlink > 1 or os.path.islink(file_path)


def gen_key(study_instance_uid, series_instance_uid):
    '''
    生成新的id
    :param study_instance_uid:
    :param series_instance_uid:
    :return:
    '''
    return '_'.join([study_instance_uid, series_instance_uid])


def parse_record_csv(reader):
    '''
    解析csv结果
    key, study_instance_uid, series_instance_uid, old_patient_id, old_patient_name, old_accession_number, old_institution_name, old_institution_address, new_patient_id, new_patient_name, series_path, case_num
    :param reader:
    :return:
    '''
    if reader is None:
        return {}

    t_map = {}
    line_num = 0
    for line in reader:
        key = gen_key(line[0], line[1])
        t_map[key] = line
        line_num = line_num + 1
    return t_map, line_num


def hash_patient_id(patient_id: str, length: int = 13) -> str:
    '''
    生成新的id
    :param patient_id:
    :param length:
    :return:
    '''
    result = encrypt(patient_id)
    if len(result) <= length:
        return 'sk_' + result, 'sk_' + result
    else:
        return 'sk_' + result[:length], result[length:]
    # m = md5()
    # m.update(patient_id.encode('utf-8'))
    # result = new_id_prefix + m.hexdigest()[:length]
    # return result


def parse_case_num(path_path):
    '''
    获取目录中的case_num
    :param path_path:
    :return:
    '''
    return path_path.split('/')[-1]


def get_attr(ds, tag_name):
    '''
    获取ds中的tag值
    :param ds:
    :param tag_name:
    :return:
    '''
    return ds.get(tag_name)


def anonymize_dcm(root_path, file_path, anonymize_map, record_writer, case_num, line_num, failed_dcms_csv_writer):
    '''
    脱敏某一个dcm文件
    :param root_path:
    :param file_path:
    :param anonymize_map:
    :param record_writer:
    :param case_num:
    :param line_num:
    :return:
    '''
    try:
        ds = pydicom.dcmread(file_path, force=True)
        old_patient_id = get_attr(ds, 'PatientID')
        if old_patient_id.startswith(new_id_prefix) or old_patient_id.startswith(zhongtai_id_prefix):
            return line_num

        old_patient_name = get_attr(ds, 'PatientName')
        old_accession_number = get_attr(ds, 'AccessionNumber')
        old_institution_name = get_attr(ds, 'InstitutionName')
        old_institution_address = get_attr(ds, 'InstitutionAddress')
        study_instance_uid = get_attr(ds, 'StudyInstanceUID')
        series_instance_uid = get_attr(ds, 'SeriesInstanceUID')

        key = gen_key(study_instance_uid, series_instance_uid)
        existing_record = anonymize_map.get(key)

        if existing_record is not None:
            new_patient_id = existing_record[7]
            new_patient_name = existing_record[8]
        else:
            # 如果曾经没有生成过脱敏后的id，则生成新的id，否则保持第一次脱敏生成的id
            if not old_patient_id.startswith(new_id_prefix):
                new_patient_id, new_patient_name = hash_patient_id(old_patient_id)
            else:
                new_patient_id = old_patient_id
                new_patient_name = old_patient_name
            line_num = line_num + 1
            print(str(line_num), ' series is processed:', root_path)
            anonymize_map[key] = [study_instance_uid, series_instance_uid, old_patient_id, old_patient_name,
                                  old_accession_number, old_institution_name, old_institution_address,
                                  new_patient_id, new_patient_name, root_path, case_num]
            record_writer.writerow([study_instance_uid, series_instance_uid, old_patient_id, old_patient_name,
                                    old_accession_number, old_institution_name, old_institution_address,
                                    new_patient_id, new_patient_name, root_path, case_num])
        # 如果没有脱敏过，则执行脱敏
        if not (old_patient_id.startswith(new_id_prefix) or old_patient_id.startswith(zhongtai_id_prefix)):
            ds.PatientName = new_patient_name
            ds.PatientID = new_patient_id
            ds.AccessionNumber = new_patient_id
            ds.InstitutionName = 'Anonymous'
            ds.InstitutionAddress = 'Anonymous'
            ds.save_as(file_path)
    except Exception as e:
        print(e)
        print('Failed to anonymize' + file_path + '.')
        failed_dcms_csv_writer.writerow([file_path])
    return line_num


def anonymize_dir(dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer):
    '''
    脱敏一个目录
    :param dir:
    :param anonymize_map:
    :param record_writer:
    :param line_num:
    :return:
    '''
    print('anonymize dir', dir)
    if not os.path.exists(dir):
        print(dir, ' is not existing.')
        return
    for root, _, files in os.walk(dir):
        for file in files:
            try:
                file_path = osp.join(root, file)
                case_num = parse_case_num(root)
                # print(file_path)
                # if link_file(file_path):
                #     print(file_path, ' is link file')
                #     link_files_csv_writer.writerow([file_path])
                #     continue
                if file.endswith('.dcm'):
                    line_num = anonymize_dcm(root, osp.join(root, file), anonymize_map, record_writer, case_num,
                                             line_num, failed_dcms_csv_writer)
            except Exception as e:
                continue


def anonymize_product(data_dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer):
    '''
    脱敏产品的整个data目录下面的source， output， original
    :param dir:
    :param anonymize_map:
    :param record_writer:
    :param line_num:
    :return:
    '''
    source_data_dir = os.path.join(data_dir, 'source')
    output_data_dir = os.path.join(data_dir, 'output')
    original_data_dir = os.path.join(data_dir, 'original')

    print('original dir:', original_data_dir)
    print('source dir:', source_data_dir)
    print('output dir:', output_data_dir)

    anonymize_dir(original_data_dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer)
    anonymize_dir(source_data_dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer)
    anonymize_dir(output_data_dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer)


def anonymize_db(username, pwd, host, port, records):
    '''
    连接数据库，对平台数据库进行脱敏
    1. apply_record:patient_id, condition: series_instance_uid, study_instance_uid, case_num
    2. cases: patient_id, patient_name, accession_number, condition: series_instance_uid, study_instance_uid, case_num
    3. patient: patient_id, patient_name, condition: old_patient_id, old_patient_name
    4. series: patient_id, condition: series_instance_uid, study_instance_uid
    5. study: patient_id, accession_number, condition: study_instance_uid, old_patient_id
    :return:
    '''
    if username is None or pwd is None or host is None or port is None:
        print('db connection info invalid')
    print('start to anonymize platform db:', host, ' ', port, ' ', 'plt_dicom')
    cnx = mysql.connector.connect(user=username, password=pwd, host=host, database="plt_dicom", port=port)
    cur = cnx.cursor()
    print('start to anonymize table apply_record')
    sql = "update apply_record set patient_id=%s WHERE study_instance_uid=%s and  series_instance_uid=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[0]), str(row[1])))
    cur.executemany(sql, val)
    cnx.commit()

    print('start to anonymize table cases')
    sql = "update cases set patient_id=%s, patient_name=%s, accession_number=%s WHERE study_instance_uid=%s and series_instance_uid=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[8]), str(row[7]), str(row[0]), str(row[1])))
    cur.executemany(sql, val)
    cnx.commit()

    print('start to anonymize table patient')
    sql = "update patient set patient_id=%s, patient_name=%s WHERE patient_id=%s and  patient_name=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[8]), str(row[2]), str(row[3])))
    cur.executemany(sql, val)
    cnx.commit()

    print('start to anonymize table series')
    sql = "update series set patient_id=%s WHERE study_instance_uid=%s and  series_instance_uid=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[0]), str(row[1])))
    cur.executemany(sql, val)
    cnx.commit()

    print('start to anonymize table study')
    sql = "update study set patient_id=%s, accession_number=%s WHERE study_instance_uid=%s and patient_id=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[7]), str(row[0]), str(row[2])))
    cur.executemany(sql, val)
    cnx.commit()
    cnx.close()


def anonymize_jupiter(host, records, db_username, db_pwd, db_port, mongo_username, mongo_pwd, mongo_port):
    anonymize_jupiter_db(db_username, db_pwd, host, db_port, records)
    anonymize_jupiter_mongo(mongo_username, mongo_pwd, host, mongo_port, records)
    pass


def anonymize_jupiter_db(username, pwd, host, port, records):
    '''
        连接数据库，对平台数据库进行脱敏
        1. series:patient_id, patient_name, accession_number, condition: series_instance_uid, study_instance_uid
        2. study: patient_id, patient_name, accession_number, condition: study_instance_uid
        :return:
        '''
    if username is None or pwd is None or host is None or port is None:
        print('db connection info invalid')
    print('start to anonymize platform db:', host, ' ', port, ' ', 'plt_jupiter')
    cnx = mysql.connector.connect(user=username, password=pwd, host=host, database="plt_jupiter", port=port)
    cur = cnx.cursor()
    print('start to anonymize table series')
    sql = "update series set patient_id=%s, patient_name=%s, accession_number=%s WHERE study_instance_uid=%s and  series_instance_uid=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[8]), str(row[7]), str(row[0]), str(row[1])))
    cur.executemany(sql, val)
    cnx.commit()

    print('start to anonymize table study')
    sql = "update study set patient_id=%s, patient_name=%s, accession_number=%s WHERE study_instance_uid=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[8]), str(row[7]), str(row[0])))
    cur.executemany(sql, val)
    cnx.commit()
    cnx.close()


def anonymize_jupiter_mongo(username, pwd, host, port, records):
    print('anonymize_jupiter_mongo', username, pwd, host, port)
    mongo_url = "mongodb://{}:{}@{}:{}/{}".format(username, pwd, host, port, 'plt_jupiter')
    client = pymongo.MongoClient(mongo_url, authSource="admin")
    plt_jupiter = client['plt_jupiter']
    seriesMeta = plt_jupiter['seriesMeta']
    for key, row in records.items():
        myquery = {"studyInstanceUid": row[0], "seriesInstanceUid": row[1]}
        newvalues = {
            "$set": {"dicomMeta.patientId": row[7], "dicomMeta.patientName": row[7], "institutionName": "Anonymous"}}
        x = seriesMeta.update_many(myquery, newvalues)
        print(str(x.modified_count), " seriesLesion documents are modified")
    client.close()


def anonymize_jupiter_mark(host, records, db_username, db_pwd, db_port, mongo_username, mongo_pwd, mongo_port):
    anonymize_jupiter_mark_db(db_username, db_pwd, host, db_port, records)
    anonymize_jupiter_mark_mongo(mongo_username, mongo_pwd, host, mongo_port, records)
    pass


def anonymize_jupiter_mark_db(username, pwd, host, port, records):
    '''
        连接数据库，对平台数据库进行脱敏
        1. series:patient_id, patient_name, accession_number, condition: series_instance_uid, study_instance_uid
        2. study: patient_id, patient_name, accession_number, condition: study_instance_uid
        :return:
        '''
    if username is None or pwd is None or host is None or port is None:
        print('db connection info invalid')
    print('start to anonymize jupiter_mark db:', host, ' ', port, ' ', 'plt_jupiter_mark')
    cnx = mysql.connector.connect(user=username, password=pwd, host=host, database="plt_jupiter_mark", port=port)
    cur = cnx.cursor()
    print('start to anonymize table series')
    sql = "update series set patient_id=%s, patient_name=%s, accession_number=%s WHERE study_instance_uid=%s and  series_instance_uid=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[8]), str(row[7]), str(row[0]), str(row[1])))
    cur.executemany(sql, val)
    cnx.commit()

    print('start to anonymize table study')
    sql = "update study set patient_id=%s, patient_name=%s, accession_number=%s WHERE study_instance_uid=%s"
    val = []
    for key, row in records.items():
        val.append((str(row[7]), str(row[8]), str(row[7]), str(row[0])))
    cur.executemany(sql, val)
    cnx.commit()
    cnx.close()


def anonymize_jupiter_mark_mongo(username, pwd, host, port, records):
    print('anonymize_jupiter_mark_mongo', username, pwd, host, port)
    mongo_url = "mongodb://{}:{}@{}:{}/{}".format(username, pwd, host, port, 'plt_jupiter_mark')
    client = pymongo.MongoClient(mongo_url, authSource="admin")
    plt_jupiter = client['plt_jupiter_mark']
    seriesMeta = plt_jupiter['seriesMeta']
    for key, row in records.items():
        myquery = {"studyInstanceUid": row[0], "seriesInstanceUid": row[1]}
        newvalues = {
            "$set": {"patientId": row[7], "patientName": row[7], "institutionName": "Anonymous"}}
        x = seriesMeta.update_many(myquery, newvalues)
        print(str(x.modified_count), " seriesLesion documents are modified")
    client.close()


if __name__ == '__main__':
    args = parse_args()
    data_dir = args.data_dir
    is_product = args.is_product
    if args.anonymize_dcm_only == 'true' and args.anonymize_db_only == 'true':
        print('parameter anonymize_dcm_only and anonymize_db_only should not be true at the same time')
        exit(1)

    # 解析上一次的输出，保持多次运行脱敏结果一致
    if args.last_record_csv is not None:
        last_record_csv = osp.join(osp.dirname(__file__), args.last_record_csv)
        with open(last_record_csv) as last_record_csv_out:
            record_reader = csv.reader(last_record_csv_out)
            anonymize_map, line_num = parse_record_csv(record_reader)
    else:
        anonymize_map = {}
        line_num = 0

    new_record_csv = osp.join(osp.dirname(__file__),
                              'anonymization_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.csv')
    record_csv_out = open(new_record_csv, "w")
    record_writer = csv.writer(record_csv_out)

    failed_dcms_csv = osp.join(osp.dirname(__file__),
                               'failed_dcms_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.csv')
    failed_dcms_csv_out = open(failed_dcms_csv, "w")
    failed_dcms_csv_writer = csv.writer(failed_dcms_csv_out)

    # 把上次断掉的数据写入
    for key, row in anonymize_map.items():
        record_writer.writerow(row)

    # 只脱敏dcm文件
    if args.anonymize_dcm_only == 'true':
        print('只脱敏dcm文件')
        if is_product == 'true':
            anonymize_product(data_dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer)
        else:
            anonymize_dir(data_dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer)
        record_csv_out.close()
        exit(0)

    # 只脱敏数据库（platform db, product db, product mongo）文件
    if args.anonymize_db_only == 'true':
        print('只脱敏数据库:platform db, product db, product mongo')
        anonymize_db(args.username, args.password, args.host, args.port, anonymize_map)
        if 'jupiter' in args.products:
            anonymize_jupiter(args.host, anonymize_map, args.username, args.password, args.port, args.mongo_username,
                              args.mongo_password, args.mongo_port)
        record_csv_out.close()
        failed_dcms_csv_out.close()
        exit(0)

    print('脱敏dcm文件')
    if is_product == 'true':
        anonymize_product(data_dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer)
    else:
        anonymize_dir(data_dir, anonymize_map, record_writer, line_num, failed_dcms_csv_writer)

    print('脱敏数据库:platform db, product db, product mongo')
    # 脱敏平台数据库
    anonymize_db(args.username, args.password, args.host, args.port, anonymize_map)
    # 脱敏jupiter数据库

    products = args.products.split(',')
    if 'jupiter-mark' in products:
        anonymize_jupiter_mark(args.host, anonymize_map, args.username, args.password, args.port, args.mongo_username,
                               args.mongo_password, args.mongo_port)

    if 'jupiter' in products:
        anonymize_jupiter(args.host, anonymize_map, args.username, args.password, args.port, args.mongo_username,
                          args.mongo_password, args.mongo_port)

    record_csv_out.close()
    failed_dcms_csv_out.close()

print('done!')
