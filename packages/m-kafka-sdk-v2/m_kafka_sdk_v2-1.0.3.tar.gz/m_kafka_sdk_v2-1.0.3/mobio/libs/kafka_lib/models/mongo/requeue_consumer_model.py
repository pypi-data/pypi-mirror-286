#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: locnh
    Company: MobioVN
    Date created: 27/05/2019
"""
from mobio.libs.kafka_lib.models.mongo.base_model import BaseModel
from pymongo import ReadPreference
from mobio.libs.kafka_lib import RequeueStatus
from datetime import datetime, timedelta


class RequeueConsumerModel(BaseModel):
    TOPIC = "topic"
    KEY = "key"
    DATA = "data"
    SEQUENCE = "sequence"
    PARTITION = "partition"
    ERROR = "error"
    COUNT_ERR = "count_err"
    NEXT_RUN = "next_run"
    STATUS = "status"
    CREATED_TIME = "created_time"
    UPDATED_TIME = "updated_time"
    EXPIRY_TIME = "expire_time"

    def __init__(self, client_mongo):
        super().__init__()
        self.client_mongo = client_mongo
        self.db_name = self.client_mongo.get_default_database().name
        self.collection = "requeue_consumer"

    def get_messages(self, partitions, sequence=0, limit=1000):
        return (
            self.get_db(read_preference=ReadPreference.SECONDARY_PREFERRED)
            .find(
                {
                    self.PARTITION: {"$in": partitions},
                    self.STATUS: RequeueStatus.ENABLE,
                    self.NEXT_RUN: {"$lte": datetime.utcnow()},
                    self.SEQUENCE: {"$gt": sequence},
                }
            )
            .sort(self.SEQUENCE, 1)
            .limit(limit)
        )

    def update_status_lst_msg(self, lst_ids):
        return self.update_many(
            query={"_id": {"$in": lst_ids}},
            data={
                self.STATUS: RequeueStatus.DISABLE,
                self.EXPIRY_TIME: datetime.utcnow() + timedelta(days=3),
            },
        )
