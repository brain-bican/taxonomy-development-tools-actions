import os
import sqlite3
import requests
import threading
import ast
import time
from contextlib import closing
from ctat.cell_type_annotation import CellTypeAnnotation, Annotation, Labelset, AnnotationTransfer, UserAnnotation

cas_table_postfixes = ["_annotation", "_labelset", "_metadata", "_annotation_transfer"]


def export_cas_data(sqlite_db: str, output_file: str):
    """
    Reads all data from TDT tables and generates CAS json.
    :param sqlite_db: db file path
    :param output_file: output json path
    """
    print("INN export_cas_data")
    cta = CellTypeAnnotation("", list())

    cas_tables = get_table_names(sqlite_db)
    for table_name in cas_tables:
        if table_name.endswith("_metadata"):
            parse_metadata_data(cta, sqlite_db, table_name)
        if table_name.endswith("_annotation"):
            parse_annotation_data(cta, sqlite_db, table_name)
        if table_name.endswith("_labelset"):
            parse_labelset_data(cta, sqlite_db, table_name)
        if table_name.endswith("_annotation_transfer"):
            parse__annotation_transfer_data(cta, sqlite_db, table_name)
    print("OUTTT")

    return cta


def parse_metadata_data(cta, sqlite_db, table_name):
    """
    Reads 'Metadata' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    """
    pass


def parse_annotation_data(cta, sqlite_db, table_name):
    """
    Reads 'Annotation' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    """
    with closing(sqlite3.connect(sqlite_db)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM {}".format(table_name)).fetchall()
            columns = list(map(lambda x: x[0], cursor.description))
            print(columns)
            print(rows[0])

            if len(rows) > 0:
                annotations = list()
                for row in rows:
                    annotation = Annotation("", "")
                    auto_fill_object_from_row(annotation, columns, row)
                    # handle user_annotations
                    user_annotations = list()
                    obj_fields = vars(annotation)
                    for column in columns:
                        if column not in obj_fields and column not in ["row_number"]:
                            user_annotations.append(UserAnnotation(column, str(row[columns.index(column)])))
                    annotation.user_annotations = user_annotations
                    # handle outlier columns

                    annotations.append(annotation)
                cta.annotations = annotations


def parse_labelset_data(cta, sqlite_db, table_name):
    """
    Reads 'Labelset' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    """
    pass


def parse__annotation_transfer_data(cta, sqlite_db, table_name):
    """
    Reads 'Annotation Transfer' table data into the CAS object
    :param cta: cell type annotation schema object.
    :param sqlite_db: db file path
    :param table_name: name of the metadata table
    """
    pass


def get_table_names(sqlite_db):
    """
    Queries 'table' table to get all CAS related table names
    :param sqlite_db: db file path
    :return: list of CAS related table names
    """
    cas_tables = list()
    with closing(sqlite3.connect(sqlite_db)) as connection:
        with closing(connection.cursor()) as cursor:
            rows = cursor.execute("SELECT * FROM 'table'").fetchall()
            columns = list(map(lambda x: x[0], cursor.description))
            print(columns)
            print(rows)
            table_column_index = columns.index('table')
            for row in rows:
                if str(row[table_column_index]).endswith(tuple(cas_table_postfixes)):
                    cas_tables.append(str(row[table_column_index]))
    return cas_tables


def auto_fill_object_from_row(obj, columns, row):
    """
    Automatically sets attribute values of the obj from the given db table row.
    :param obj: object to fill
    :param columns: list of the db table columns
    :param row: db record
    """
    for column in columns:
        if hasattr(obj, column):
            value = str(row[columns.index(column)])
            if value.startswith("[") and value.endswith("]"):
                value = ast.literal_eval(value)
            setattr(obj, column, value)
