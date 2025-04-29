import logging
import json
import redis

from tb_rest_client.rest_client_pe import RestClientPE
from tb_rest_client.rest import ApiException


logger = logging.getLogger("scheduler_logger")


class CubaRestClient:

    def __init__(self, url, username, password, config_path="config.json"):
        self._url = url
        self._username = username
        self._password = password
        self._config_path = config_path
        self._redis = redis.Redis(db=0)

    def get_device_attributes(self, device):
        attrs = ""
        with open(self._config_path, "r") as config_file:
            logger.info(config_file)
            logger.info(self._config_path)
            config = json.loads(config_file.read())

            # attrs = ",".join(list(config.keys()))

            # logger.info(f"ATTRIB: {attrs}")
            with RestClientPE(base_url=self._url) as rest_client:
                try:
                    # Auth with credentials
                    rest_client.login(username=self._username, password=self._password)

                    attrs = "offTill,shift1LessonsNum,test,shift2LessonsNum,alarm,isOff,days,fire,onTill,ambulance,offFor,onFor"  # ,alarmAudio"  # ,fireAudio,testAudio,endLessonAudio,startLessonAudio"
                    attributes = rest_client.get_device_attributes(
                        device, shared_keys=attrs, client_keys=""
                    )
                    if not attributes.get("shared"):
                        return
                    shared_attrs = attributes.get("shared")
                    test, alarm, fire, ambulance = shared_attrs.get("test", False), shared_attrs.get("alarm", False), shared_attrs.get("fire", False), shared_attrs.get("ambulance", False)
                    self._redis.set("test", "1" if test else "0")
                    self._redis.set("alarm", "1" if alarm else "0")
                    self._redis.set("fire", "1" if fire else "0")
                    self._redis.set("ambulance", "1" if ambulance else "0")
                    with open(self._config_path, "w") as config_file:
                        shared_attrs = attributes.get("shared")
                        if shared_attrs:
                            for k, v in shared_attrs.items():
                                config[k] = v
                            json.dump(config, config_file, indent=2)

                except ApiException as e:
                    logger.exception(e)
