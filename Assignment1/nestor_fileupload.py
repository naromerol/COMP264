### COMP264 - Cloud Machine Learning
### Nestor Romero   301133331
### Assignment 1

import boto3
import pathlib
import logging
from datetime import datetime

# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#create service client
s3 = boto3.resource('s3')
bucket_name = 'content301133331'

try:

    # locate path where code is executing
    local_path = pathlib.Path(__file__).parent.resolve()
    logger.info(f'Folder to lookup files >> {local_path}\n')

    for id in range(1,4):
        # create filenames dynamically
        filename = f'test_text{id}.txt'
        logger.info(f'{filename} started uploading... (start: {datetime.now()})')

        result = s3.meta.client.upload_file(f'{local_path}/{filename}', bucket_name, filename)

        logger.info(f'{filename} is uploaded... (end: {datetime.now()})\n')
        
        
    logger.info('End of process\n')

except s3.meta.client.exceptions.NoSuchBucket as no_such_bucket:
    logging.error(no_such_bucket.response)

except Exception as ex: 
    logging.error(ex)

