#%%
#Packages
import os
#Import logging
from logger import configure_logging

logger = configure_logging(os.environ.get('LOGFILE_PATH'))

try:
    import pandas as pd
    from sqlalchemy import create_engine
except Exception as e:
    logger.error(f"Missing Package: {e}")
    raise SystemExit("Exiting...")

#%%
#Functions

#MYSQL
def connect_to_mysql_db(host, username, password, db, driver):


    try:
        MYSQL_engine = create_engine(f"{driver}://{username}:{password}@{host}/{db}")
        logger.info(f"Connection to the database {host}/{db} established successfully")  
        return MYSQL_engine
    except Exception as e:
        logger.error("Error connecting to the database: "+str(e))
        logger.error("Stopping the script...")
        raise SystemExit("Exiting...")
    
def query_mysql_table(engine, query):
    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, con=conn.connection)
            logger.info(f"Table queried successfully with the following number of lines returned: {df.iloc[0,0]}")
            return df
    except Exception as e:
        logger.error("Error executing the query: "+str(e))
        logger.error("Stopping the script...")
        raise SystemExit("Exiting...")