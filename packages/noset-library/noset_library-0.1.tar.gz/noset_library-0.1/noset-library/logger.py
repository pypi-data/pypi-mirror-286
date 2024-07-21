#Prepare generic logging function
import logging as log


def configure_logging(log_filename):
    log.basicConfig(
        level=log.INFO
        ,format='%(asctime)s - %(levelname)s - %(message)s'
        ,filename=f'{log_filename}.log'
        ,filemode='a'
    )

    #Logger
    logger = log.getLogger()

    return logger