"""

"""

from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
import requests
import json


class BasicSQL2SolrImport:

  def __init__(self, batch_size=20):
    self.conn = MsSqlHook.get_connection(conn_id="mssql_test_db")
    self.batch_size = batch_size

  """
  Get data from the database
  """
  def extract(self):
    hook = self.conn.get_hook()
    sql=f"""
    SELECT top 1000 *
    FROM drugs
    ORDER BY id;
    """
    df = hook.get_pandas_df(sql=sql)
    return df.to_json(date_format='iso', orient="records")

  """
  Transform into SOLR format
  """
  def transform(self, data):
    return data

  """
  Push to SOLR
  """
  def load(self, data):
    try:
      url ='http://solr-86:8983/solr/drug_data/update?commitWithin=1000&overwrite=true&wt=json'
      headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
      session = requests.Session()
      resp = session.post(url, data=data, headers=headers)
      if not resp.ok:
        raise Exception('SOLR ERROR', resp)
      num_rows = len(json.loads(data))
      print(f'Response from SOLR: {resp}')
      # print(f"***Num Records Loaded {num_rows} ")
      return json.dumps({
         "num_rows": num_rows
      })

    except requests.exceptions.HTTPError as httpErr:
      print("Http Error:", httpErr)
    except requests.exceptions.ConnectionError as connErr:
      print("Error Connecting:", connErr)
    except requests.exceptions.Timeout as timeOutErr:
      print("Timeout Error:", timeOutErr)
    except requests.exceptions.RequestException as reqErr:
        print("Something Else:", reqErr)

  """
  Report
  """
  def report(self, data):
    print("Data Import complete")
    print(data)
    return data

if __name__ == '__main__':
    s = BasicSQL2SolrImport()
    s.extract(0, 20)
