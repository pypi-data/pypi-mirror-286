import json
from abc import abstractmethod
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from confluent_kafka.cimpl import KafkaError, KafkaException, Consumer
from sonyflake import SonyFlake

from mobio.libs.kafka_lib import RequeueStatus, KAFKA_BOOTSTRAP
from mobio.libs.kafka_lib.helpers import consumer_warning_slack
from mobio.libs.kafka_lib.models.mongo.requeue_consumer_model import (
    RequeueConsumerModel,
)
from time import time, sleep
from uuid import uuid4
import os
import pathlib

try:
    from mobio.libs.logging import MobioLogging

    m_log = MobioLogging()
except:
    import logging as MobioLogging

    m_log = MobioLogging


def commit_completed(err, partitions):
    if err:
        m_log.error(str(err))
    else:
        m_log.info("Committed partition offsets: " + str(partitions))


class BaseKafkaConsumer:
    sf = SonyFlake(
        start_time=datetime(
            year=2017,
            month=6,
            day=29,
            hour=0,
            minute=0,
            second=0,
            tzinfo=timezone.utc,
        )
    )
    TOPIC = "topic"
    GROUP = "group"
    PARTITION = "partition"
    OFFSET = "offset"

    def __init__(
        self,
        topic_name: object,
        group_id: object,
        client_mongo=None,
        retryable=True,
        session_timeout_ms=15000,
        bootstrap_server=None,
        consumer_config=None,
        lst_subscribe_topic=None,
        retry_topic=None,
        enable_bloom=False,
        auto_commit=True,
        redis_client=None,
    ):
        self.client_id = str(uuid4())
        self.group_id = group_id
        self.lst_subscribe_topic = (
            lst_subscribe_topic if lst_subscribe_topic else [topic_name]
        )
        self.retry_topic = retry_topic if retry_topic else self.lst_subscribe_topic[0]
        self.enable_bloom = enable_bloom
        if self.enable_bloom:
            # Nếu kafka-bloom được thiết lập, consumer cần phải truyền redis-client vào để tái sử dụng
            # Khi kafka-bloom được thiết lập, hệ thống sẽ tự động chuyển config của auto-commit = False
            if not redis_client:
                raise Exception("enable bloom should be set redis_client")
            m_log.info("enable kafka-bloom, auto set auto.commit=false")
            self.auto_commit = False
        else:
            self.auto_commit = auto_commit
        config = {
            "bootstrap.servers": KAFKA_BOOTSTRAP
            if not bootstrap_server
            else bootstrap_server,
            "group.id": group_id,
            "auto.offset.reset": "latest",
            "session.timeout.ms": session_timeout_ms,
            "client.id": self.client_id,
            "error_cb": self.error_cb,
            "enable.auto.commit": "false" if not self.auto_commit else "true",
        }
        if not self.auto_commit:
            config["on_commit"] = commit_completed

        if consumer_config:
            config.update(consumer_config)
        self.c = Consumer(config)
        self.client_mongo = client_mongo
        self.retryable = retryable
        self.lst_processed_msg = []
        self.last_time_commit = time()
        self.st_mtime = None
        self.default_commit_time = 5

        if self.retryable and not self.client_mongo:
            raise Exception(
                "client_mongo must present if set retryable: {}".format(self.retryable)
            )

        try:
            self.c.subscribe(self.lst_subscribe_topic)
            m_log.info("start consumer with config: {}".format(config))

            self.__init_self_check__()

            if self.enable_bloom:
                from mobio.libs.kafka_lib.helpers.redisbloom_client import (
                    RedisBloomClient,
                )

                self.redis_bloom = RedisBloomClient(redis_client=redis_client)
                for t in self.lst_subscribe_topic:
                    self.redis_bloom.init_cuckoo_filter(
                        topic=t, group=str(self.group_id), capacity=65536
                    )
            while True:
                if self.is_maintain():
                    if not self.auto_commit and self.lst_processed_msg:
                        self.check_period_and_manual_commit()
                    sleep(self.default_commit_time)
                    m_log.warning(
                        "System is Maintenance !!! Feel free and drink some tea. :)"
                    )
                    continue
                msg = self.c.poll(1.0)
                if msg is None:
                    if not self.auto_commit and self.lst_processed_msg:
                        self.check_period_and_manual_commit()
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        m_log.warning(
                            "%% %s [%d] reached end at offset %d\n"
                            % (msg.topic(), msg.partition(), msg.offset())
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    try:
                        start_time = time()
                        self.pre_process_message(msg=msg)

                        end_time = time()
                        m_log.info(
                            "end: {} with total time: '[{:.3f}s]".format(
                                self.lst_subscribe_topic, end_time - start_time
                            )
                        )
                    except Exception as e:
                        m_log.error(
                            "MessageQueue::run - topic: {} ERR: {}".format(
                                self.lst_subscribe_topic, e
                            )
                        )
        except RuntimeError as e:
            m_log.error(
                "something unexpected happened: {}: {}".format(
                    self.lst_subscribe_topic, e
                )
            )
        except KafkaException as e:
            m_log.error("KafkaException: {}: {}".format(self.lst_subscribe_topic, e))
        finally:
            m_log.error("consumer is stopped")
            self.c.close()
            consumer_warning_slack(
                pod_name=os.environ.get("HOSTNAME"),
                group_id=self.group_id,
                pretext="Consumer closed",
            )
            # sleep(30)
            raise Exception("Consumer closed")

    def __init_self_check__(self):
        """
        desc: function init some configs for health check and collaboration with Devops team
        """
        # Add mapping client-id kafka and pod name
        # Lưu file consumer theo group
        DATA_DIR = os.environ.get("APPLICATION_DATA_DIR")
        folder_path = "{}/{}/{}".format(
            DATA_DIR, "kafka-liveness-consumer", self.group_id
        )
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # Add mapping client-id kafka and pod name
        file_path = "{folder_path}/{client_id}".format(
            folder_path=folder_path, client_id=self.client_id
        )
        # Save relationship pods and topic
        host_name = os.environ.get("HOSTNAME")
        f = open(file_path, "w")
        pod_data_info = "{host_name}".format(host_name=host_name)
        f.write(pod_data_info)
        f.close()

        # PATHLIB for control pod maintain
        pull_message_status_path = "/tmp/consumer_pull_message_status"
        if not os.path.exists(pull_message_status_path):
            fs = open(pull_message_status_path, "w")
            fs.write("")
            fs.close()
        self.pl = pathlib.Path(pull_message_status_path)

    def pre_process_message(self, msg):
        key = msg.key()
        message = msg.value().decode("utf-8")
        payload = json.loads(message)
        if self.enable_bloom:
            if not self.redis_bloom.check_cuckoo_filter(
                topic=msg.topic(),
                group=str(self.group_id),
                value=int(f"1{msg.partition()}{msg.offset()}"),
            ):
                self.process(payload, key)
                self.__add_msg_to_bloom__(msg=msg)
            else:
                # Nếu bloom báo not exists thì chắc chắn not exists,
                # đôi khi báo exists nhưng chỉ là false positive và cần phải check lại
                # PS: với case này, vì msg đã tồn tại trong bloom, nên không cần thiết phải add vào bloom 1 lần nữa
                if self.check_msg_is_processed(payload=payload) is True:
                    m_log.error(
                        "topic: {}, partition: {}, offset: {}, msg: {} already processed".format(
                            msg.topic(), msg.partition(), msg.offset(), payload
                        )
                    )
                else:
                    self.process(payload, key)
        else:
            self.process(payload, key)
        if not self.auto_commit:
            self.__add_message_to_list_processed__(msg=msg)
            self.check_period_and_manual_commit()

    def check_msg_is_processed(self, payload: dict) -> bool:
        """
        Function cần overwrite lại nếu sử dụng bloom_filter,
        ở đây các pod xử lý logic code để check db xem message này đã được xử lý hay chưa.
        Vì Bloom Filter chỉ có thể đảm bảo được rằng message thật sự chưa tồn tại,
        còn với tình huống báo là tồn tại thì rất có thể là cảnh báo sai.
        Lúc này cần check các case cảnh báo sai, còn các case báo là chưa tồn tại thì có thể yên tâm là thật sự chưa tồn tại.

        :param payload: kafka message cần check xem đã được xử lý chưa.
        :return: True nếu muốn bỏ qua không xử lý lại message, False thì message sẽ được đưa vào function process để xử lý
        """
        return True

    def __delete_msg_from_bloom__(self, dict_msg):
        result_delete = self.redis_bloom.del_cuckoo_filter_value(
            topic=dict_msg.get(self.TOPIC),
            group=str(dict_msg.get(self.GROUP)),
            value=int(f"1{dict_msg.get(self.PARTITION)}{dict_msg.get(self.OFFSET)}"),
        )
        m_log.info(
            f"delete bloom topic: {dict_msg.get(self.TOPIC)}, partition: {dict_msg.get(self.PARTITION)}, offset: {dict_msg.get(self.OFFSET)} {'true' if result_delete else 'false'}"
        )

    def __add_msg_to_bloom__(self, msg):
        self.redis_bloom.add_cuckoo_filter(
            topic=msg.topic(),
            group=str(self.group_id),
            value=int(f"1{msg.partition()}{msg.offset()}"),
        )

    def __add_message_to_list_processed__(self, msg):
        self.lst_processed_msg.append(
            {
                self.TOPIC: msg.topic(),
                self.GROUP: self.group_id,
                self.PARTITION: msg.partition(),
                self.OFFSET: msg.offset(),
            }
        )

    def check_period_and_manual_commit(self):
        """
        description: Function kiểm tra xem và xử lý việc manual commit message.
        Nếu message đạt ngưỡng 150 msg hoặc
        đã đạt period 5 seconds và có message đã xử lý thì sẽ async commit tới brokers
        """
        now = time()
        if (
            now - self.last_time_commit >= self.default_commit_time
            and self.lst_processed_msg
        ) or len(self.lst_processed_msg) == 150:
            self.c.commit(asynchronous=True)
            m_log.info(
                f"commit success: [{','.join([str.format('{}:{}:{}', x.get(self.TOPIC), x.get(self.PARTITION), x.get(self.OFFSET)) for x in self.lst_processed_msg ])}]"
            )
            self.last_time_commit = now
            if self.enable_bloom:
                for processed_msg in self.lst_processed_msg:
                    self.__delete_msg_from_bloom__(dict_msg=processed_msg)
            del self.lst_processed_msg
            self.lst_processed_msg = []

    def is_maintain(self):
        """
        description: function kiểm tra hệ thống có đang trong quá trình maintain hay không?
        Nếu hệ thống đang trong quá trình maintain thì sẽ không poll message mới.
        """
        stat = self.pl.stat()
        st_mtime = stat.st_mtime
        if self.st_mtime != st_mtime:
            print(f"stat: {stat}")
            self.st_mtime = float(st_mtime)
            # return True if self.pl.read_text().strip() == '1' else False
            return True if stat.st_size == 2 else False
        return False

    def error_cb(self, err):
        m_log.error("Client error: {}".format(err))
        consumer_warning_slack(
            pod_name=os.getenv("HOSTNAME"),
            group_id=self.group_id,
            pretext="client error: {}".format(err),
        )

    def process(self, data, key=None):
        count_err = 0
        if self.retryable:
            recall_data = deepcopy(data)
        else:
            recall_data = None
        try:
            if "count_err" in data:
                try:
                    count_err = int(data.pop("count_err"))
                except:
                    count_err = 0
            self.message_handle(data=data)
        except Exception as e:
            m_log.error(
                "consumer::run - topic: {} ERR: {}".format(self.lst_subscribe_topic, e)
            )
            if recall_data and self.retryable:
                count_err += 1
                if count_err <= 10:
                    data_error = {
                        RequeueConsumerModel.TOPIC: self.retry_topic,
                        RequeueConsumerModel.KEY: key.decode("ascii")
                        if key
                        else str(uuid4()),
                        RequeueConsumerModel.DATA: recall_data,
                        RequeueConsumerModel.ERROR: str(e),
                        RequeueConsumerModel.COUNT_ERR: count_err,
                        RequeueConsumerModel.SEQUENCE: self.sf.next_id(),
                        RequeueConsumerModel.NEXT_RUN: datetime.utcnow()
                        + timedelta(minutes=5 + count_err),
                        RequeueConsumerModel.EXPIRY_TIME: datetime.utcnow()
                        + timedelta(days=7),
                        RequeueConsumerModel.STATUS: RequeueStatus.ENABLE,
                    }
                    result = RequeueConsumerModel(self.client_mongo).insert(
                        data=data_error
                    )
                    m_log.info("RequeueConsumerModel result: {}".format(result))
            else:
                m_log.info(
                    "RequeueConsumerModel maximum error retry. retry count: {}".format(
                        count_err
                    )
                )

    @abstractmethod
    def message_handle(self, data):
        pass
