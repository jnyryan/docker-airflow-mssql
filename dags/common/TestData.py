"""

"""

from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook

class TestData:

  def __init__(self, batch_size = 20):
        self.conn = MsSqlHook.get_connection(conn_id="mssql_test_db")
        self.batch_size = batch_size

  def get_batched_data(self):
    self.get_data(10)
    self.get_data(20)
    self.get_data(30)

  def get_data(self, start):
    # conn = MsSqlHook.get_connection(conn_id="mssql_test_db")
    hook = self.conn.get_hook()
    sql=f"""
    SELECT *
    FROM drugs
    ORDER BY id
    OFFSET {start} ROWS
    FETCH NEXT {self.batch_size} ROWS ONLY;
    """
    print(sql)
    df = hook.get_pandas_df(sql=sql)
    return df.to_dict()
