from tizori_cli.config import get_config_value
from tizori_cli.wrapper.base import BaseRequestWrapper

base_wrapper = BaseRequestWrapper(base_url=get_config_value("base_url"), 
                                  bearer_token=get_config_value("token"))