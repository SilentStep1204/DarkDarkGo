#! /usr/bin/env python3
"""
    database_manager_test.py - Database Manager Test
    Author:
        - Hoanh An (hoanhan@bennington.edu)
    Date: 12/2/2017
"""

from mgmt.src.database_manager import DatabaseManager
from pprint import pprint

def test_link_operation():
    """
    Test link relation's basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('link')

    # INSERT
    db_manager.operate_on_link_relation('INSERT', link='https://www.example_101.com')
    if db_manager.get_relation('link')[-1]['link'] == 'https://www.example_101.com' and db_manager.get_relation('link')[-1]['state'] == 'pending':
        print('> PASSED | INSERT | Link relation')
    else:
        print('> FAILED | INSERT | Link relation')

    # UPDATE STATE
    db_manager.operate_on_link_relation('UPDATE_STATE', link='https://www.example_101.com', state='crawling')
    if db_manager.get_relation('link')[-1]['state'] == 'crawling':
        print('> PASSED | UPDATE_STATE | Link relation')
    else:
        print('> FAILED | UPDATE_STATE | Link relation')

    # UPDATE CHUNK ID
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    db_manager.operate_on_link_relation('UPDATE_CHUNK_ID', link='https://www.example_101.com', chunk_id='101c')
    if db_manager.get_relation('link')[-1]['chunk_id'] == '101c':
        print('> PASSED | UPDATE_CHUNK_ID | Link relation')
    else:
        print('> FAILED | UPDATE_CHUNK_ID | Link relation')
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')

    # DELETE
    db_manager.operate_on_link_relation('DELETE', link='https://www.example_101.com')
    if db_manager.get_length('link') == start_length:
        print('> PASSED | DELETE | Link relation')
    else:
        print('> FAILED | DELETE | Link relation')

def test_chunk_operation():
    """
    Test chunk relation's basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('chunk')

    # INSERT
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    if db_manager.get_relation('chunk')[-1]['id'] == '101c':
        print('> PASSED | INSERT | Chunk relation')
    else:
        print('> FAILED | INSERT | Chunk relation')

    # DELETE
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')
    if db_manager.get_length('chunk') == start_length:
        print('> PASSED | DELETE | Chunk relation')
    else:
        print('> FAILED | DELETE | Chunk relation')

def test_host_operation():
    """
    Test host relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('host')

    # INSERT
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:101', type='Crawler')
    if db_manager.get_relation('host')[-1]['host'] == '101.101.101.101:101' and db_manager.get_relation('host')[-1]['state'] == 'offline':
        print('> PASSED | INSERT | Host relation')
    else:
        print('> FAILED | INSERT | Host relation')

    # UPDATE STATE
    db_manager.operate_on_host_relation('UPDATE_STATE', host='101.101.101.101:101', state='online')
    if db_manager.get_relation('host')[-1]['state'] == 'online':
        print('> PASSED | UPDATE_STATE | Host relation')
    else:
        print('> FAILED | UPDATE_STATE | Host relation')

    # UPDATE HEALTH
    db_manager.operate_on_host_relation('UPDATE_HEALTH', host='101.101.101.101:101', health='healthy')
    if db_manager.get_relation('host')[-1]['health'] == 'healthy':
        print('> PASSED | UPDATE_HEALTH | Host relation')
    else:
        print('> FAILED | UPDATE_HEALTH | Host relation')

    # DELETE
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:101')
    if db_manager.get_length('host') == start_length:
        print('> PASSED | DELETE | Host relation')
    else:
        print('> FAILED | DELETE | Host relation')

def test_crawler_operation():
    """
    Test crawler relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('crawler')

    # Setup temp chunk and host for testing
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:101', type='Crawler')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:102', type='Crawler')

    # INSERT
    db_manager.operate_on_crawler_relation('INSERT', chunk_id='101c', host='101.101.101.101:101')
    if db_manager.get_relation('crawler')[-1]['chunk_id'] == '101c' and db_manager.get_relation('crawler')[-1]['c_task'] == 'crawling':
        print('> PASSED | INSERT | Crawler relation')
    else:
        print('> FAILED | INSERT | Crawler relation')

    # UPDATE HOST
    db_manager.operate_on_crawler_relation('UPDATE_HOST', chunk_id='101c', host='101.101.101.101:102')
    if db_manager.get_relation('crawler')[-1]['c_host'] == '101.101.101.101:102':
        print('> PASSED | UPDATE_HOST | Crawler relation')
    else:
        print('> FAILED | UPDATE_HOST | Crawler relation')

    # UPDATE TASK
    db_manager.operate_on_crawler_relation('UPDATE_TASK', chunk_id='101c', task='crawled')
    if db_manager.get_relation('crawler')[-1]['c_task'] == 'crawled':
        print('> PASSED | UPDATE_TASK | Crawler relation')
    else:
        print('> FAILED | UPDATE_TASK | Crawler relation')

    # DELETE
    db_manager.operate_on_crawler_relation('DELETE', chunk_id='101c')
    if db_manager.get_length('crawler') == start_length:
        print('> PASSED | DELETE | Crawler relation')
    else:
        print('> FAILED | DELETE | Crawler relation')

    # Delete temp chunk and host when finish testing
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:101')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:102')

def test_index_builder_operation():
    """
    Test index builder relation basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('index_builder')

    # Setup temp chunk and host for testing
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:101', type='Index Builder')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:102', type='Index Builder')

    # INSERT
    db_manager.operate_on_index_builder_relation('INSERT', chunk_id='101c', host='101.101.101.101:101')
    if db_manager.get_relation('index_builder')[-1]['chunk_id'] == '101c' and db_manager.get_relation('index_builder')[-1]['ib_task'] == 'building':
        print('> PASSED | INSERT | Index Builder relation')
    else:
        print('> FAILED | INSERT | Index Builder relation')

    # UPDATE HOST
    db_manager.operate_on_index_builder_relation('UPDATE_HOST', chunk_id='101c', host='101.101.101.101:102')
    if db_manager.get_relation('index_builder')[-1]['ib_host'] == '101.101.101.101:102':
        print('> PASSED | UPDATE_HOST | Index Builder relation')
    else:
        print('> FAILED | UPDATE_HOST | Index Builder relation')

    # UPDATE TASK
    db_manager.operate_on_index_builder_relation('UPDATE_TASK', chunk_id='101c', task='built')
    if db_manager.get_relation('index_builder')[-1]['ib_task'] == 'built':
        print('> PASSED | UPDATE_TASK | Index Builder relation')
    else:
        print('> FAILED | UPDATE_TASK | Index Builder relation')

    # DELETE
    db_manager.operate_on_index_builder_relation('DELETE', chunk_id='101c')
    if db_manager.get_length('index_builder') == start_length:
        print('> PASSED | DELETE | Index Builder relation')
    else:
        print('> FAILED | DELETE | Index Builder relation')

    # Delete temp chunk and host when finish testing
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:101')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:102')

def test_index_server_operation():
    """
    Test index server basic operations.
    :return: None
    """
    db_manager = DatabaseManager()
    start_length = db_manager.get_length('index_server')

    # Setup temp chunk and host for testing
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='101c')
    db_manager.operate_on_chunk_relation('INSERT', chunk_id='102c')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:101', type='Index Server')
    db_manager.operate_on_host_relation('INSERT', host='101.101.101.101:102', type='Index Server')

    # INSERT
    db_manager.operate_on_index_server_relation('INSERT', row=101, chunk_id='101c', host='101.101.101.101:101')
    if db_manager.get_relation('index_server')[-1]['chunk_id'] == '101c' and db_manager.get_relation('index_server')[-1]['row'] == 101:
        print('> PASSED | INSERT | Index Server relation')
    else:
        print('> FAILED | INSERT | Index Server relation')

    # UPDATE ROW
    db_manager.operate_on_index_server_relation('UPDATE_ROW', row=102, chunk_id='101c', host='101.101.101.101:101')
    if db_manager.get_relation('index_server')[-1]['row'] == 102:
        print('> PASSED | UPDATE_ROW | Index Server relation')
    else:
        print('> FAILED | UPDATE_ROW | Index Server relation')

    # UPDATE CHUNK ID
    db_manager.operate_on_index_server_relation('UPDATE_CHUNK_ID', chunk_id='102c', row=102, host='101.101.101.101:101')
    if db_manager.get_relation('index_server')[-1]['chunk_id'] == '102c':
        print('> PASSED | UPDATE_CHUNK_ID | Index Server relation')
    else:
        print('> FAILED | UPDATE_CHUNK_ID | Index Server relation')

    # UPDATE HOST
    db_manager.operate_on_index_server_relation('UPDATE_HOST', host='101.101.101.101:102', row=102, chunk_id='102c')
    if db_manager.get_relation('index_server')[-1]['is_host'] == '101.101.101.101:102':
        print('> PASSED | UPDATE_HOST | Index Server relation')
    else:
        print('> FAILED | UPDATE_HOST | Index Server relation')

    # DELETE
    db_manager.operate_on_index_server_relation('DELETE', row=102, chunk_id='102c', host='101.101.101.101:102')
    if db_manager.get_length('index_server') == start_length:
        print('> PASSED | DELETE | Index Server relation')
    else:
        print('> FAILED | DELETE | Index Server relation')

    # Delete temp chunk and host when finish testing
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='101c')
    db_manager.operate_on_chunk_relation('DELETE', chunk_id='102c')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:101')
    db_manager.operate_on_host_relation('DELETE', host='101.101.101.101:102')

if __name__ == '__main__':
    test_link_operation()
    test_chunk_operation()
    test_host_operation()
    test_crawler_operation()
    test_index_builder_operation()