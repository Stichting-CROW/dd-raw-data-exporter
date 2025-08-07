import psycopg2
import psycopg2.extras
import psycopg2.sql
import export_request

def generate_trips(conn, requestParameters: export_request.ExportRequestParameters, dir_name: str):
    cur = conn.cursor()
    file_name = dir_name + "/trips.csv"
    f = open(file_name, "w")
    stmt = psycopg2.sql.SQL("""
    COPY 
        (
        WITH temp_a (filter_area) AS
            (
            SELECT st_union(ST_makeValid(area)) 
	            FROM zones WHERE zone_id IN {zone_ids}
        )    
            
        SELECT trips.system_id, bike_id, st_y(start_location) as lat_start_location, 
        st_x(start_location) as lng_start_location, st_y(end_location) as lat_end_location, 
        st_x(end_location) as lng_end_location, start_time, end_time, 
        st_distancesphere(start_location, end_location) as distance, EXTRACT(EPOCH FROM (end_time - start_time)) as duration_in_seconds,
        form_factor, propulsion_type
        FROM trips
        CROSS JOIN temp_a
        LEFT JOIN vehicle_type
        ON trips.vehicle_type_id = vehicle_type.vehicle_type_id
        WHERE start_time >= {start_time}
        AND start_time < {end_time}
        AND (
                false = {filter_on_zones} or (
                    ST_Within(start_location, temp_a.filter_area) OR
                    ST_Within(end_location, temp_a.filter_area)
                )
            )
            AND (
                false = {filter_on_system_id} or 
                trips.system_id IN {system_ids}
            )
        )
        TO STDOUT With CSV HEADER DELIMITER ','
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