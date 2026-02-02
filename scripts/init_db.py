import argparse 
import sqlite3 
from pathlib import Path 
import time 
import sys 
import os 



def main ():
    parser =argparse .ArgumentParser (
    description ="Initialize backend/db.sqlite3 from SQL files."
    )
    parser .add_argument ("--reset",action ="store_true",help ="Delete existing db.sqlite3 and recreate it.")
    parser .add_argument ("--seed",action ="store_true",help ="Load complete_seed_2024_2026.sql.")
    args =parser .parse_args ()







    current_file =Path (__file__ ).resolve ()
    if current_file .parent .name =='scripts':
        base_dir =current_file .parent .parent 
    else :

        base_dir =current_file .parent 

    db_path =base_dir /"backend"/"db.sqlite3"
    schema_path =base_dir /"db"/"schema.sql"
    data_path =base_dir /"db"/"data.sql"
    seed_path =base_dir /"db"/"complete_seed_2024_2026.sql"

    print (f"Project root detected at: {base_dir }")
    print (f"Target Database: {db_path }")


    for p in (schema_path ,data_path ):
        if not p .exists ():
            print (f"Error: Missing SQL file: {p }")
            sys .exit (1 )

    if args .reset and db_path .exists ():
        print ("Resetting database...")
        try :
            db_path .unlink ()
        except OSError as e :
            print (f"Error deleting database: {e }")
            sys .exit (1 )


    con =sqlite3 .connect (db_path )
    cur =con .cursor ()

    try :

        print (f"Loading schema from {schema_path .name }...")
        schema_sql =schema_path .read_text (encoding ='utf-8',errors ='replace')

        schema_sql ="PRAGMA foreign_keys = OFF;\n"+schema_sql 
        cur .executescript (schema_sql )


        if args .seed :

            if seed_path .exists ():
                print (f"Loading seed from {seed_path .name }...")
                seed_sql =seed_path .read_text (encoding ='utf-8',errors ='replace')
                seed_sql ="PRAGMA foreign_keys = OFF;\n"+seed_sql 
                cur .executescript (seed_sql )
            else :
                print (f"Warning: Seed file {seed_path } not found.")
        else :

            print (f"Loading data from {data_path .name }...")
            data_sql =data_path .read_text (encoding ='utf-8',errors ='replace')
            data_sql ="PRAGMA foreign_keys = OFF;\n"+data_sql 
            cur .executescript (data_sql )

        con .commit ()
        print ("Database initialized successfully.")

    except Exception as e :
        print (f"Database initialization failed: {e }")
        sys .exit (1 )
    finally :
        con .close ()

if __name__ =="__main__":
    main ()
