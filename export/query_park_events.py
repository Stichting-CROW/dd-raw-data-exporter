import psycopg2
import psycopg2.extras
import psycopg2.sql
import export_request

def generate_park_events(conn, requestParameters: export_request.ExportRequestParameters, dir_name: str):
    cur = conn.cursor()
    file_name = dir_name + "/park_events.csv"
    f = open(file_name, "w")
    stmt = psycopg2.sql.SQL("""COPY 
    (SELECT park_events.system_id, bike_id,
    ST_Y(location) as lat, ST_X(location) as lon,
    start_time, end_time, form_factor, propulsion_type
    FROM park_events 
    LEFT JOIN vehicle_type
    ON vehicle_type.vehicle_type_id = park_events.vehicle_type_id
    WHERE (start_time >= {start_time} and start_time < {end_time})
    AND (
            false = {filter_on_zones} 
            or ST_WITHIN(location, (
                SELECT st_union(ST_makeValid(area))
	            FROM zones WHERE zone_id IN {zone_ids}
            ))
        )
        AND (false = {filter_on_system_id} or park_events.system_id IN {system_ids})
    ) To STDOUT With CSV HEADER DELIMITER ','
    """).format(
        start_time=psycopg2.sql.Literal(requestParameters.start_time),
        end_time=psycopg2.sql.Literal(requestParameters.end_time),
        filter_on_zones=psycopg2.sql.Literal(requestParameters.filter_on_zones),
        zone_ids=psycopg2.sql.Literal(tuple(requestParameters.zones)),
        filter_on_system_id=psycopg2.sql.Literal(requestParameters.filter_on_operator),
        system_ids=psycopg2.sql.Literal(tuple(requestParameters.operators))
    )
    cur.copy_expert(stmt, f)
    f.close()

    return file_name