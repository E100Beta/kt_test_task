#!/usr/bin/env python3

import os

from btc_api.db import create_tables

db_url = os.environ.get('DATABASE_URL')
create_tables(db_url)
