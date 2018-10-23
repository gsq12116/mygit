import pymysql


class Conn:
    def __init__(self, host, port, user, password, db, charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.database = pymysql.connect(host=self.host, port=self.port,
                                        user=self.user, password=self.password,
                                        db=self.db, charset=self.charset)
        self.cursor = self.database.cursor(cursor=pymysql.cursors.DictCursor)

    def select(self, sql):
        info_list = []
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        while result:
            info_list.append(result)
            result = self.cursor.fetchone()
        return info_list

    def exec_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.database.commit()
            print('success')
        except Exception as e:
            print(e)

    def conn_close(self):
        self.cursor.close()
        self.database.close()
        print('connection closed successful')
