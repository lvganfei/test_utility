import datetime
from elasticsearch import Elasticsearch


def extract_es_index(hit):
    return f'-- log_name: {hit["_source"]["log"]["file"]["path"]}, -- content: {hit["_source"]["message"]}'
def get_error_from_elasticsearch():

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    es = Elasticsearch([{'host':'opses01.democompany.net','port':9200}], timeout=3600)

    query = {
        "query": {
            "bool":{
                "must":[
                    {"term":{
                        "fields.type.keyword": "universe-log"
                    }},
                    {"range": {
                        "@timestamp": {
                            "gte": "now-30m",
                            "lte": "now",
                            "format": "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
                        }
                    }}
                ]
            }
            
        },
        "sort": {"@timestamp": {"order": "desc"}},
        "size": "5000"
    }

    result = es.search(index=f"10.15.10.216-longrun-monitor-universe-{today}", body=query)
    exception_count = result['hits']['total']['value']
    hits = result['hits']['hits']
    print(len(hits))

    final_result = list(map(extract_es_index, hits))


    print(f'日志条数：{exception_count}')
    print('\n'.join(final_result))


if __name__ == "__main__":
    get_error_from_elasticsearch()