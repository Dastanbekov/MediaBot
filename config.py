from dotenv import load_dotenv

load_dotenv()

import os
TOKEN = os.getenv('TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
 