import pymysql


class Dbtool(object):
    # ==fc== init sql client
    def __init__(self):
        self.connect = pymysql.connect(
            host='192.168.***',
            port=3366,
            db='***',
            user='**',
            passwd='***',
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.close()

    def insertNlg(self, intent, line, projectId, level):
        try:
            self.cursor.execute(
                """insert into ***table***(
                   intention,
                   answer,
                   chat_project_id,
                   level)
                  value (%s,%s,%s,%s)""",
                (
                  intent,
                  line,
                  projectId,
                  level
                )
            )
        except Exception as error:
            print(error.__str__())
        # this commit for dev/test time only
        self.connect.commit()
