import time
import json
from functools import reduce

import pandas as pd

from notion_client import Client, APIErrorCode, APIResponseError
from notion_client.errors import HTTPResponseError, RequestTimeoutError
from notion_client.helpers import collect_paginated_api

from . import n2p_read_write

class NotionMaxAttempsException(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class Notion2PandasClient(Client):
    """Extension of Client from notion_client.

    Attributes:
        secondsToRetry: .
        callsLimitThreshold: .
        maxAttempsExecutoner: .
    """

    _ROW_HASH_KEY = 'Row_Hash'
    _ROW_PAGEID_KEY = 'PageID'

    # It's not in the official documentation, but it seems there is a limit of 2700 API calls in 15 minutes.
    # https://notionmastery.com/pushing-notion-to-the-limits/#rate-limits
    # WIP
    _RATE_LIMIT_THRESHOLD = 900 #60 * 15
    _CALLS_LIMIT_THRESHOLD = 2700

    def __init__(self, **kwargs):
        self.__set_n2p_arg(kwargs, 'secondsToRetry', 30)
        self.__set_n2p_arg(kwargs, 'maxAttempsExecutioner', 3)

        super().__init__(**kwargs)

        self.read_only_columns = {"last_edited_time", "last_edited_time",
                                  "files", "created_time", "rollup", "unique_id", "last_edited_by",
                                  "button", "formula", "created_by"}

        self.title_read_write_lambdas = (n2p_read_write.title_read, n2p_read_write.title_write)
        self.rich_text_read_write_lambdas = (n2p_read_write.rich_text_read, n2p_read_write.rich_text_write)
        self.checkbox_read_write_lambdas = (n2p_read_write.checkbox_read, n2p_read_write.checkbox_write)
        self.created_time_read_write_lambdas = (n2p_read_write.created_time_read, n2p_read_write.created_time_write)
        self.number_read_write_lambdas = (n2p_read_write.number_read, n2p_read_write.number_write)
        self.email_read_write_lambdas = (n2p_read_write.email_read, n2p_read_write.email_write)
        self.url_read_write_lambdas = (n2p_read_write.url_read, n2p_read_write.url_write)
        self.multi_select_read_write_lambdas = (n2p_read_write.multi_select_read, n2p_read_write.multi_select_write)
        self.select_read_write_lambdas = (n2p_read_write.select_read, n2p_read_write.select_write)
        self.date_read_write_lambdas = (n2p_read_write.date_read, n2p_read_write.date_write)
        self.files_read_write_lambdas = (n2p_read_write.files_read, n2p_read_write.files_write)
        self.formula_read_write_lambdas = (lambda notion_property:self.__readValueFromNotion(n2p_read_write.formula_read(notion_property)),
                                           n2p_read_write.formula_write)
        self.phone_number_read_write_lambdas = (n2p_read_write.phone_number_read, n2p_read_write.phone_number_write)
        self.status_read_write_lambdas = (n2p_read_write.status_read, n2p_read_write.status_write)
        self.unique_id_read_write_lambdas = (n2p_read_write.unique_id_read, n2p_read_write.unique_id_write)
        self.created_by_read_write_lambdas = (n2p_read_write.created_by_read, n2p_read_write.created_by_write)
        self.last_edited_time_read_write_lambdas = (n2p_read_write.last_edited_time_read, n2p_read_write.last_edited_time_write)
        self.string_read_write_lambdas = (n2p_read_write.string_read, n2p_read_write.string_write)
        self.last_edited_by_read_write_lambdas = (n2p_read_write.last_edited_by_read, n2p_read_write.last_edited_by_write)
        self.button_read_write_lambdas = (n2p_read_write.button_read, n2p_read_write.button_write)
        self.relation_read_write_lambdas = (n2p_read_write.relation_read, n2p_read_write.relation_write)
        self.rollup_read_write_lambdas = (lambda notion_property:str(list(map(lambda notion_rollup: self.__readValueFromNotion(
                                              notion_rollup), n2p_read_write.rollup_read(notion_property)))),
                                          n2p_read_write.rollup_write)
        self.people_read_write_lambdas = (n2p_read_write.people_read, n2p_read_write.people_write)
        
    """Since Notion has introduced limits on requests to their APIs (https://developers.notion.com/reference/request-limits), 
       this method can repeat the request to the Notion APIs at predefined time intervals
       until a result is obtained or if the maximum limit of attempts is reached."""
    def _notionExecutor(self, api_to_call, **kwargs):
        attempts = self.maxAttempsExecutioner
        current_calls = 0
        while (attempts > 0):
            try:
                result = api_to_call(**kwargs)
                current_calls += 1
                return result
            except HTTPResponseError as error:
                print('Catched exception: ' + str(error))
                attempts -= 1
                if isinstance(error, APIResponseError):
                    print('Error code: ' + error.code)
                    if error.code != APIErrorCode.InternalServerError and error.code != APIErrorCode.ServiceUnavailable:
                        print(error)
                        print(APIResponseError)
                        # raise APIErrorCode.ObjectNotFound
                else:
                    # Other error handling code
                    print(error)
                # Wait secondsToRetry before retry
                time.sleep(self.secondsToRetry)
            except RequestTimeoutError as error:
                print('Catched exception: ' + str(error))
                attempts -= 1
            if attempts == 0:
                raise NotionMaxAttempsException(
                    "NotionMaxAttempsException") from None
            print('[_notionExecutor] Remaining attemps: ' + str(attempts))
        return result

    def get_database_columns(self, database_ID):
        return self._notionExecutor(
            self.databases.retrieve, **{'database_id': database_ID})

    def create_page(self, parent_id, properties = None):
        created_page = self._notionExecutor(self.pages.create, **{'parent' : {"database_id": parent_id},
         'properties' : properties})
        return created_page.get('id')

    def update_page(self, page_ID, properties = None):
        created_page = self._notionExecutor(self.pages.update,**{'page_id': page_ID,
                       'properties': properties})
        return created_page.get('id')

    def retrieve_page(self, page_ID):
        return self._notionExecutor(
            self.pages.retrieve, **{'page_id': page_ID})

    def delete_page(self, page_ID):
        self._notionExecutor(
            self.blocks.delete, **{'block_id': page_ID})

    def retrieve_block(self, block_ID):
        return self._notionExecutor(
            self.blocks.retrieve, **{'block_id': block_ID})

    def retrieve_block_children_list(self, page_ID):
        return self._notionExecutor(
            self.blocks.children.list, **{'block_id': page_ID})

    def update_block(self, block_ID, field, field_value_updated):
        return self._notionExecutor(
            self.blocks.update, **{'block_id': block_ID, field: field_value_updated})

    def __row_hash(self, row):
        row_dict = row.to_dict()
        if self._ROW_HASH_KEY in row_dict:
            del row_dict[self._ROW_HASH_KEY]
        return self.__calculate_dict_hash(row_dict)

    def __calculate_dict_hash(self, d):
        serialized_dict = json.dumps(d, sort_keys=True)
        return hash(serialized_dict)

    def __get_database_columnsAndTypes(self, database_ID):
        columns = self.get_database_columns(database_ID)
        if columns is None:
            return None
        return list(map(lambda notion_property:
                        (columns.get('properties').get(notion_property).get('name'),
                         columns.get('properties').get(notion_property).get('type')),
                        columns.get('properties')))

    def from_notion_DB_to_dataframe(self, database_ID, filter_params={}):
        results = self._notionExecutor(
            collect_paginated_api,
            **{'function': self.databases.query, **filter_params, "database_id": database_ID})
        database_data = []
        for result in results:
            prop_dict = {}
            for notion_property in result.get("properties"):
                prop_dict[str(notion_property)] = self.__readValueFromNotion(
                    result.get("properties").get(notion_property))
            prop_dict[self._ROW_PAGEID_KEY] = result.get("id")
            database_data.append(prop_dict)
        df = pd.DataFrame(database_data)
        df[self._ROW_HASH_KEY] = df.apply(
            lambda row: self.__row_hash(row), axis=1)
        return df

    def update_notion_DB_from_dataframe(self, database_ID, df):
        columns = self.__get_database_columnsAndTypes(database_ID)
        for index, row in df.iterrows():
            if self.__row_hash(row) != row['Row_Hash']:
                prop_dict = {}
                for column in columns:
                    columnName = column[0]
                    columnType = column[1]
                    if (columnType in self.read_only_columns):
                        continue
                    prop_dict[columnName] = self.__writeValueToNotion(
                        row[columnName], columnType)
                if row[self._ROW_PAGEID_KEY] != '':
                    self.update_page(row[self._ROW_PAGEID_KEY], prop_dict)
                else:
                    self.create_page(database_ID, prop_dict)

    def __readValueFromNotion(self, notion_property):
        return self.__get_value_from_lambda(
            notion_property, notion_property.get("type"), 0)

    def __writeValueToNotion(self, row_value, notion_type):
        return self.__get_value_from_lambda(
            row_value, notion_type, 1)

    def __get_value_from_lambda(self, input_value, notion_type, lambda_index):
        switcher = {
            'title': self.title_read_write_lambdas[lambda_index],
            'rich_text': self.rich_text_read_write_lambdas[lambda_index],
            'checkbox': self.checkbox_read_write_lambdas[lambda_index],
            'created_time': self.created_time_read_write_lambdas[lambda_index],
            'number': self.number_read_write_lambdas[lambda_index],
            'email': self.email_read_write_lambdas[lambda_index],
            'url': self.url_read_write_lambdas[lambda_index],
            'multi_select': self.multi_select_read_write_lambdas[lambda_index],
            'select': self.select_read_write_lambdas[lambda_index],
            'date': self.date_read_write_lambdas[lambda_index],
            'files': self.files_read_write_lambdas[lambda_index],
            'formula': self.formula_read_write_lambdas[lambda_index],
            'phone_number': self.phone_number_read_write_lambdas[lambda_index],
            'status': self.status_read_write_lambdas[lambda_index],
            'unique_id': self.unique_id_read_write_lambdas[lambda_index],
            'created_by': self.created_by_read_write_lambdas[lambda_index],
            'last_edited_time': self.last_edited_time_read_write_lambdas[lambda_index],
            'string': self.string_read_write_lambdas[lambda_index],
            'last_edited_by': self.last_edited_by_read_write_lambdas[lambda_index],
            'button': self.button_read_write_lambdas[lambda_index],
            'relation': self.relation_read_write_lambdas[lambda_index],
            'rollup': self.rollup_read_write_lambdas[lambda_index],
            'people': self.people_read_write_lambdas[lambda_index]
        }

        return switcher.get(notion_type, lambda: "Invalid: " + input_value)(input_value)

    def __set_n2p_arg(self, kwargs, field_name, defaultValue):
        if field_name in kwargs:
            setattr(self, field_name, kwargs[field_name])
            del kwargs[field_name]
        else:
            setattr(self, field_name, defaultValue)
   