import logging
import json

from tb_rest_client.rest_client_pe import RestClientPE
from tb_rest_client.rest import ApiException


logger = logging.getLogger("scheduler_logger")


class CubaRestClient:

    def __init__(self, url, username, password, config_path="config.json"):
        self._url = url
        self._username = username
        self._password = password
        self._config_path = config_path

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
                    with open(self._config_path, "w") as config_file:
                        shared_attrs = attributes["shared"]
                        for k, v in shared_attrs.items():
                            config[k] = v
                        json.dump(config, config_file, indent=2)

                except ApiException as e:
                    logger.exception(e)
