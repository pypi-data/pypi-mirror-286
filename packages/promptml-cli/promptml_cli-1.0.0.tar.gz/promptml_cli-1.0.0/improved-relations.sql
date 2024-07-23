        
        WITH mp_relations AS (
            SELECT * FROM origin_osm.relations WHERE relation_type = 'multipolygon'
        )
        
        CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.multipolygon_relations as (
            SELECT 
                mp_relations.osm_id, ST_BuildArea(ST_Collect(origin_osm.ways.geometry)) AS geometry
            FROM 
                mp_relations 
            JOIN 
                origin_osm.relation_members
                ON mp_relations.osm_id = origin_osm.relation_members.parent_id
                AND origin_osm.relation_members.member_type = 1
            JOIN 
                origin_osm.ways
                ON origin_osm.relation_members.osm_id = origin_osm.ways.osm_id
            
            GROUP BY mp_relations.osm_id
        ) WITH NO DATA;
