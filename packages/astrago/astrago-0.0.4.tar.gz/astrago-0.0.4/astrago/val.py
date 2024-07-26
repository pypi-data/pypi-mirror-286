import os
import time
import uuid

uuid = str(uuid.uuid4())
workload_name = os.environ.get('ASTRAGO_WORKLOAD_NAME')
url = os.environ.get('ASTRAGO_URL')
user_id = os.environ.get('ASTRAGO_USER_ID')
step = 0
start_time = time.time()
