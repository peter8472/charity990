from google.cloud import bigquery
import google.auth
import pdb
import json
import util


irsquery = """
SELECT
  irsein.name AS name,
  irsein.state AS state,
  irsein.city AS city,
  irs990.totrevenue AS revenue,
  irs990.noemplyeesw3cnt AS employees,
  irs990.noindiv100kcnt AS employees_over_100k,
  irs990.compnsatncurrofcr AS officers_comp
FROM
    `bigquery-public-data.irs_990.irs_990_ein` AS irsein
JOIN
    `bigquery-public-data.irs_990.irs_990_2015` AS irs990
USING (ein)
ORDER BY
  revenue DESC
LIMIT 5
"""

irs2 = """
select * from bigquery-public-data.irs_990.irs_990_ein where name like "%UNITED%S%CHESS%" limit 100;
"""

credentials, project = google.auth.default( 
  scopes = [
   "https://www.googleapis.com/auth/drive.readonly",
  "https://www.googleapis.com/auth/bigquery"
  ])

if __name__ == "__main__":
  client = bigquery.Client(credentials=credentials, project=project)

  for i in client.get_table( "bigquery-public-data.irs_990.irs_990_ein").schema:
    #print(i.to_api_repr())
     pass
  for i in client.get_table( "bigquery-public-data.irs_990.irs_990_2015").schema:
      if i.name.find("website") != -1:
         print(i.name) 

#  query_job = client.query( irs2 )
 # results = query_job.result()  # Waits for job to complete.
#  util.print_results(results)      



