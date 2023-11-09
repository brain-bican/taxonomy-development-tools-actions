import requests
import threading

nanobot_default_tables = ["table", "column", "datatype"]


def export_cas_data(output_folder: str):
    print("INN export_cas_data")
    x = threading.Thread(target=asynch_table_read, args=(1,))
    x.start()
    # response.raise_for_status()
    #
    # table_records = response.json()
    # for table_rec in table_records:
    #     if table_rec["table"] not in table_rec["table"]:
    #         print(table_rec["table"])
    print("OUTTT")


def asynch_table_read(name):
    print("INN asynch_table_read")
    response = requests.get('http://localhost:3000/table.json?limit=20&shape=value_rows')
    print(response.status_code)
    print(response.text)
