#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import uuid

logger = logging.getLogger(__name__)


JOB_ID = os.environ.get('SCRAPY_JOB', str(uuid.uuid4()))
logger.info("Running JOB: %s", JOB_ID)
