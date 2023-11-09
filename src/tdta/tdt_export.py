import os
import requests
import threading
import json
import time

nanobot_default_tables = ["table", "column", "datatype"]


def export_cas_data(output_folder: str):
    print("INN export_cas_data")
    x = threading.Thread(target=asynch_table_read, args=(output_folder,))
    x.start()
    # response.raise_for_status()
    #
    # table_records = response.json()
    # for table_rec in table_records:
    #     if table_rec["table"] not in table_rec["table"]:
    #         print(table_rec["table"])
    print("OUTTT")


def asynch_table_read(output_folder):
    print("INN asynch_table_read")
    time.sleep(5)
    print("sleep done")
    work_dir = os.path.abspath(output_folder)
    print(work_dir)
    # response = requests.get('http://localhost:3000/table.json?limit=20&shape=value_rows')
    response = requests.get('https://raw.githubusercontent.com/hkir-dev/cell-type-annotation-tools/main/src/test/test_data/hierarchy.json')
    data = response.json()

    with open(os.path.join(work_dir, "out.json"), "w") as stream:
        json.dump(data, stream, indent=2)

    print(response.status_code)
    print(response.text)
