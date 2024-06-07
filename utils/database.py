import sqlite3
import sqlalchemy

def savetoDB(tableName,table):
    # The following function takes tableName and table and saves the data to an sql database
    engine = sqlalchemy.create_engine("sqlite:///databases/database.db",echo=True)
    table.to_sql(tableName,con=engine,if_exists='append',index=True)

