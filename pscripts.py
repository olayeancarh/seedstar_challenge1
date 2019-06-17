import jenkinsapi
import sqlite3
from jenkinsapi.jenkins import Jenkins
from datetime import datetime

url = 'http://localhost:8081'
username = 'olayeancarh'
password = '12345'

# # Coonect to jenkins server with jenkins url, username, and password.
server = Jenkins(url, username=username, password=password)

# # Connecting to the database file
conn = sqlite3.connect('dbsqlite.db')
c = conn.cursor()

# Get jobs that are available
jobs = server.get_jobs()

for job in jobs:
  job_name = job[0]
  job_instance = job[1]
  if job_instance.is_running():
    job_status = 'Running'
  elif job_instance.get_last_build_or_none() == None:
    job_status = 'Not running'
  else:
    server_job = server.get_job(job_instance.name)
    build = server_job.get_last_build()
    job_status = build.get_status()

  i = datetime.now()
  checked_time = i.strftime('%Y/%m/%d %H:%M:%S')

  unsaved_jobs = (job_instance.name, job_status, checked_time)

  c.execute('SELECT id FROM jenkins WHERE job_name = ?', (unsaved_jobs[0],))
  data = c.fetchone()

  if data is None:
    c.execute('INSERT INTO jenkins (job_name, job_status, date_created) VALUES(?,?,?)', unsaved_jobs)
  else:
    save_job = (job_status, checked_time, job_instance.name)
    c.execute('UPDATE jenkins SET job_status=?, date_created=? WHERE job_name=?', save_job)

# Save (commit) the changes
conn.commit()

# We can close the connection 
conn.close()
