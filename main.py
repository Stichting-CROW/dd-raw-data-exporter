from redis_helper import redis_helper
import redis
import export_request
from export import export_to_zip
import db_helper
import upload_to_spaces
import mail_user
import shutil

pg_pool = db_helper.get_pg_pool()

def process_export_task(data):
    conn = pg_pool.getconn()
    request = export_request.ExportRequest.parse_raw(data)
    print("Received request: ", request)

    zip_file_location, dir_export = export_to_zip.generate_zip(conn, request.query_parameters)
    pg_pool.putconn(conn)
    
    download_url = upload_to_spaces.upload_to_spaces(zip_file_location)
    mail_user.mail_download_link(request.email, download_url)
    print("Finished request")
    # clean up files.
    shutil.rmtree(dir_export)

def wait_on_export_task(r: redis.Redis):
    while True:
        message = r.blpop("export_raw_data_tasks", 30)
        if message:
            data = message[1]
            process_export_task(data)

while True:
    with redis_helper.get_resource() as r:
        wait_on_export_task(r)