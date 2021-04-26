"""

"""

from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
import requests


class BasicSQL2SolrImport:

  def __init__(self, batch_size=20):
        self.conn = MsSqlHook.get_connection(conn_id="mssql_test_db")
        self.batch_size = batch_size

  def extract(self):
    row_count = 0
    while True:
      data = self.get_data(row_count, self.batch_size)
      row_count += self.batch_size
      if data.empty:
        break;
      if row_count > 20:
        break;

  def get_data(self, start, num_rows):
    hook = self.conn.get_hook()
    sql=f"""
    SELECT top 20 *
    FROM drugs
    ORDER BY id
    OFFSET {start} ROWS
    FETCH NEXT {num_rows} ROWS ONLY;
    """
    df = hook.get_pandas_df(sql=sql)
    # print(df)
    return df

  def transform(self, data):
    return data

  def load(self, data):
    return data

    try:
        resp = self.session.post(self.solr_url, data=query_params)
        return resp.json()
    except requests.exceptions.HTTPError as httpErr:
        print("Http Error:", httpErr)
    except requests.exceptions.ConnectionError as connErr:
        print("Error Connecting:", connErr)
    except requests.exceptions.Timeout as timeOutErr:
        print("Timeout Error:", timeOutErr)
    except requests.exceptions.RequestException as reqErr:
        print("Something Else:", reqErr)

if __name__ == '__main__':
    s = BasicSQL2SolrImport()
    s.extract(0, 20)
