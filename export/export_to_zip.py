import psycopg2
import os
import random
import string
import os
import zipfile
import export.query_park_events
import export.query_trips
import export_request
from datetime import datetime

def generate_zip(conn, requestParameters: export_request.ExportRequestParameters):
    letters = string.ascii_letters
    dir_name = "/tmp/export_" + ''.join(random.choice(letters) for i in range(10))
    os.makedirs(dir_name)

    trip_file_name = export.query_trips.generate_trips(conn, requestParameters, dir_name)
    park_events_file_name = export.query_park_events.generate_park_events(conn, requestParameters, dir_name)
    export_file_name = "{}/export_dashboarddeelmobiliteit_{}-{}_{}.zip".format(
        dir_name, requestParameters.start_time, requestParameters.end_time, datetime.now().isoformat().replace(".", "_").replace(":", "_"))
    with zipfile.ZipFile(export_file_name, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(trip_file_name, "trips.csv")
        zip_file.write(park_events_file_name, "park_events.csv")
    return export_file_name, dir_name
