import pandas as pd
from functools import reduce


def title_read(notion_property: dict):
        return notion_property.get('title')[0].get("plain_text") if len(notion_property.get('title')) > 0 else ''

def title_write(row_value: str):
        return { "title": [{"type": "text", "text": {"content": row_value}}]} if row_value != '' else {"title": []}

def rich_text_read(notion_property: dict):
        return notion_property.get('rich_text')[0].get("plain_text") if len(notion_property.get('rich_text')) > 0 else ''

def rich_text_write(row_value: str):
        return {"rich_text": [{"type": "text", "text": {"content": row_value}}]} if row_value != '' else {"rich_text": []}

def checkbox_read(notion_property: dict):
        return notion_property.get('checkbox')

def checkbox_write(row_value: bool):
        return {'checkbox': row_value}

def created_time_read(notion_property: dict):
        return notion_property.get('created_time')

def created_time_write(row_value):
        return 'Not supported from API'

def number_read(notion_property: dict):
        return notion_property.get('number')

def number_write(row_value: float):
        return {'number': row_value} if pd.notna(row_value) else {'number': None}

def email_read(notion_property: dict):
        return notion_property.get('email') if notion_property.get('email') is not None else ''

def email_write(row_value: str):
        return {'email': row_value} if row_value != '' else {'email': None}

def url_read(notion_property: dict):
        return notion_property.get('url') if notion_property.get('url') is not None else ''

def url_write(row_value: str):
        return {'url': row_value} if row_value != '' else {'url': None}

def multi_select_read(notion_property: dict):
        return str(list(map(lambda notion_select: notion_select.get('name'), notion_property.get('multi_select'))))

def multi_select_write(row_value: str):
        return {"multi_select": list(map(lambda notion_select: {"name": notion_select}, eval(row_value))) if row_value != '' else []}

def select_read(notion_property: dict):
        return notion_property.get('select').get('name') if notion_property.get('select') is not None else ''

def select_write(row_value: str):
        return {'select': {'name': row_value}} if row_value != '' else {'select': None}

def date_read(notion_property: dict):
        return notion_property.get('date') if notion_property.get('date') is not None else ''

def date_write(row_value: str):
        return {"date": row_value if row_value != '' else None}

def files_read(notion_property: dict):
        return reduce(lambda x, y: 
                x + ';' + y, list(map(lambda notion_file: 
                        notion_file.get('file').get('url'), notion_property.get('files')))) if notion_property.get('files') else ''

def files_write(row_value):
        return 'Not supported from API'

def formula_read(notion_property: dict):
        return notion_property.get('formula')

def formula_write(row_value):
        return 'Not supported from API'

def phone_number_read(notion_property: dict):
        return notion_property.get('phone_number') if notion_property.get('phone_number') is not None else ''

def phone_number_write(row_value: str):
        return {'phone_number': row_value} if row_value != '' else {'phone_number': None}

def status_read(notion_property: dict):
        return notion_property.get('status').get('name')

def status_write(row_value: str):
        return {'status': {"name": row_value}}

def unique_id_read(notion_property: dict):
        if notion_property.get('unique_id').get('prefix') is not None:
                return notion_property.get('unique_id').get('prefix') + notion_property.get('unique_id').get('number')
        else:
                return notion_property.get('unique_id').get('number')

def unique_id_write(row_value):
        return 'Not supported from API'

def created_by_read(notion_property: dict):
        return notion_property.get('created_by').get('id')

def created_by_write(row_value):
        return 'Not supported from API'

def last_edited_time_read(notion_property: dict):
        return notion_property.get('last_edited_time')

def last_edited_time_write(row_value):
        return 'Not supported from API'

def string_read(notion_property: dict):
        return notion_property.get('string')

def string_write(row_value):
        return {'string': row_value} if row_value != '' else {'string': None}

def last_edited_by_read(notion_property: dict):
        return notion_property.get('last_edited_by').get('id')

def last_edited_by_write(row_value):
        return 'Not supported from API'

def button_read(notion_property: dict):
        return 'Not supported from API'

def button_write(row_value):
        return 'Not supported from API'

def relation_read(notion_property: dict):
        return str(list(map(lambda notion_relation: notion_relation.get('id'), notion_property.get('relation'))))

def relation_write(row_value: str):
        return {"relation": list(map(lambda notion_relation: {"id": notion_relation}, eval(row_value))) if row_value != '' else []}

def rollup_read(notion_property: dict):
        return notion_property.get('rollup').get('array')

def rollup_write(row_value):
        return 'Not supported from API'

def people_read(notion_property: dict):
        return str(list(map(lambda notion_person: notion_person.get('id'), notion_property.get('people'))))

def people_write(row_value: str):
        return {"people": list(map(lambda notion_people: {"id": notion_people, 'object': 'user'}, eval(row_value))) if row_value != '' else []}