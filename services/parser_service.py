from obis_mapping import OBIS_MAP

class ParserService:
    @staticmethod
    def parse_value(obis_code, raw_value):
        mapping = OBIS_MAP.get(obis_code)
        if not mapping:
            return raw_value
        
        scale = mapping.get("scale", 1.0)
        return raw_value * scale

    @staticmethod
    def map_to_db_field(obis_code):
        mapping = OBIS_MAP.get(obis_code)
        if not mapping:
            return None
        return mapping.get("field")
