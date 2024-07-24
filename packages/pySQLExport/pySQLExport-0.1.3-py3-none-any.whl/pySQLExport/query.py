class Query:
    def __init__(self, database):
        self.database = database

    def execute(self, query_text):
        return self.database.execute(query_text)