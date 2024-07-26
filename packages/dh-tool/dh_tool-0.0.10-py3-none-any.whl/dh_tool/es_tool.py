from elasticsearch import Elasticsearch
import urllib3, logging

urllib3.disable_warnings()
logging.captureWarnings(True)


class ESTool:
    def __init__(self, url, id, pwd) -> None:
        self.es = Elasticsearch(
            url,
            http_auth=(id, pwd),
            verify_certs=False,
            timeout=10,
            ssl_show_warn=False,
        )
        self.env = None
        self.index_pattern = None

    def setup_env(self, env):
        self.env = env
        if env == "dev":
            self.index_pattern = "{index_sort}-2024"
        elif env == "test":
            self.index_pattern = "apply-ai-test-evalbygpt-{index_sort}-2024"
        elif env == "prod":
            self.index_pattern = "apply-ai-prod-evalbygpt-{index_sort}-2024"
        print("Now Elastic Search Env :", self.env)

    def make_body(self, **kwargs):
        must_clauses = []
        for key, value in kwargs.items():
            must_clauses.append({"match": {key: value}})
        body = {
            "_source": [],
            "query": {
                "bool": {
                    "must": must_clauses,
                }
            },
            "size": 10000,
            # "sort": [{"UpdateTime": {"order": "desc"}}],
        }
        return body

    def search(self, index_sort, return_all=False, verbose=True, **kwargs):
        if not self.env:
            raise ValueError(
                "환경이 설정되지 않았습니다. setup_env를 먼저 실행해주세요."
            )
        index_name = self.index_pattern.format(index_sort=index_sort)
        body = self.make_body(kwargs)
        res = self.es.search(index=index_name, body=body)
        hits = res["hits"]["hits"]
        if hits:
            if verbose:
                print("Data Num :", len(hits))
            if return_all:
                return hits
            return hits[0]
        else:
            print(f"{kwargs} Nodata")

    def index(self, index_sort, data, id):
        index_name = self.index_pattern.format(index_sort=index_sort)
        response = self.es.index(index=index_name, body=data, id=id)
        return response
