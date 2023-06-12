from pymilvus import connections

from conf.config import config


class MilvusClient(object):
    def __init__(self, alias: str, *args, **kwargs):
        self.alias = alias
        self.host = config.get("milvus").get("debug").get("host")
        self.port = config.get("milvus").get("debug").get("port")
        self.user = config.get("milvus").get("debug").get("user")
        self.password = config.get("milvus").get("debug").get("passwd")
        self._create_conn()
        super(MilvusClient, self).__init__(*args, **kwargs)

    def _create_conn(self):
        connections.connect(
            alias=self.alias,
            host=self.host, port=self.port,
            user=self.user, password=self.password
        )

    def disconnect(self):
        connections.disconnect(self.alias)


def main():
    pass


if __name__ == '__main__':
    main()
