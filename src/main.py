import argparse
import mysql.connector
from mysql.connector import Error


def apply(
        host: str,
        port: (int | str),
        database: str,
        user: str,
        password: str,
        **kwargs,
) -> None:
    # try:
    #     connection = mysql.connector.connect(
    #         host=host,
    #         port=port,
    #         database=database,
    #         user=user,
    #         password=password,
    #     )
        
    #     if connection.is_connected():
    #         db_Info = connection.get_server_info()
    #         print("Connected to MySQL Server version ", db_Info)
    #         cursor = connection.cursor()
    #         cursor.execute("select database();")
    #         record = cursor.fetchone()
    #         print("You're connected to database: ", record)

    # except Error as e:
    #     print("Error while connecting to MySQL", e)
    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()
    #         print("MySQL connection is closed")

    connection = mysql.connector.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
    )
    if connection.is_connected():
        cursor = connection.cursor()

        # Define the SQL query to select data from the "acore_world" table
        query = "SELECT * FROM creature; "

        # Execute the query
        cursor.execute(query)

        # Fetch all the rows
        rows = cursor.fetchall()

        # Process and print the results
        for row in rows:
            print(row)



def main():
    parser = argparse.ArgumentParser(description="A declarative way to manage your WoW database")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subparser for the 'apply' command
    apply_parser = subparsers.add_parser(
        "apply", 
        help="Apply the blob to the database", 
    )
    apply_parser.add_argument(
        "file", 
        help="Filesystem blob string (required)",
    )
    apply_parser.add_argument(
        "--host", 
        help="Database hostname (default=localhost)", 
        default="127.0.0.1",
    )
    apply_parser.add_argument(
        "--port",
        type=int, 
        help="Database port (required)", 
        default="3306",
    )
    apply_parser.add_argument(
        "--user", 
        help="Database username (required)", 
        default="acore",
    )
    apply_parser.add_argument(
        "--pass", 
        dest="password", 
        help="Database password (optional)", 
        default="acore",
    )
    apply_parser.add_argument(
        "--database", 
        help="Database name (required)",
        default="acore_world"
    )

    args = parser.parse_args()
    if args.command == "apply":
        apply(**vars(args))
    elif args.command == "destroy":
        pass
    else:
        parser.print_help()