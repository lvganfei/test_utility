import sys
from sqlalchemy import create_engine


host = sys.argv[1]


table_index_map = {
    "t_apply_record":["series_id"],
    "t_apply_rule_ae":["apply_rule_id","ae_id","id"],
    "t_apply_rule_workflow":["apply_rule_id","id"],
    "t_case":["series_id","study_id","sub_state","exam_id","org_id","id","workflow_id"],
    "t_case_diagnosis":["case_id","diagnosis_code"],
    "t_case_ext":["workflow_id","case_id","key","value","id"],
    "t_diagnosis_rule":["org_id","enable","id"],
    "t_dump_image":["image_num","status","task_id","case_num","ctime","id","product"],
    "t_print_queue":["ae_id","ae_name","ae_title", "ae_type","color", "id", "operator_id","operator_name","patient_number","state"],
    "t_push_queue":["ae_id","ae_name","ae_title", "ae_type", "id", "operator_id","operator_name","patient_number","state"],
    "t_retrieve_rule_ae":["retrieve_rule_id","ae_id","id"],
    "t_role_permission":["role_id","permission_id","id"],
    "t_series":["series_date","series_instance_uid","study_id","modality","id"],
    "t_series_tag":["tag_id","series_id","id"],
    "t_settings":["type","key","biz","type","id"],
    "t_study":["study_date","patient_number","study_instance_uid","accession_number","id","patient_id"],
    "t_user":["username","id"],
    "t_user_role":["user_id","role_id","id"],
    "t_collection_data":["study_instance_uid","series_instance_uid","patient_id","task_key","id"],
    "t_sync_dump_image":["image_num","status","task_id","case_num","ctime","id","product"],
    "t_task_queue":["case_id","order_num","priority_time","status", "case_type","node_name","need_gpu", "gpu_sn","id"],
    "t_task_queue_history":["case_id","task_queue_id","created_at","id"],
    "t_sys_record":["workflow"],
    "t_exam":["exam_num","id","org_id"],
    "t_exam_body":["key","id"],
    "t_exam_item":["id","key"]
}
def index_filter(sql_tuple):
    return sql_tuple.Column_name

def check_sql_index(host):
    sql_uri = 'mysql+pymysql://root:qY1WBZ30vjsriiHiEgK2ZkE8osjYNsj@'+host+':13306/plt_universe?charset=utf8mb4'
    # sql_uri = 'mysql+pymysql://root:mysql@'+host+':3306/plt_universe?charset=utf8mb4'

    
    engine = create_engine(sql_uri)
    for table_name, expect_indexes  in table_index_map.items():
        
        try:
            get_index_statement = f'show index from {table_name}'
            
            cur = engine.execute(get_index_statement)
            sql_result = cur.fetchall()
            result_list = list(map(index_filter, sql_result))
            # print(result_list)
            expected_diffence = list(set(expect_indexes) - set(result_list))
            unexpected_diffence = list(set(result_list) - set(expect_indexes))

            # diffence = list(set(result_list).symmetric_difference(set(expect_indexes)))
            if len(expected_diffence) != 0:
                print(f'表{table_name} 的index与预期不符, 少了column: {expected_diffence}')
                
            if len(unexpected_diffence) != 0:
                print(f'表{table_name} 的index与预期不符, 多了column: {unexpected_diffence}')
        except Exception as e:
            print(f'table {table_name} not exist')

if __name__ == '__main__':
    check_sql_index(host)