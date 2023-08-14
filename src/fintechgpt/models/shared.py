import sys
from typing import Any
from models.loader import LoaderCheckPoint
from models.base import BaseAnswer


def loaderLLM(loaderCheckPoint: LoaderCheckPoint = None, model_config: dict = {}) -> Any:
    """
    init llm_model_ins LLM
    :param llm_model: model_name
    :param model_config:  model_config
    :return:
    """

    provides_class = getattr(sys.modules['models'], model_config['provides'])
    modelInsLLM = provides_class(checkPoint=loaderCheckPoint)
    if 'FastChatOpenAILLM' in model_config["provides"]:
        modelInsLLM.set_api_base_url(model_config['api_base_url'])
        modelInsLLM.call_model_name(model_config['name'])
        modelInsLLM.set_api_key(model_config['api_key'])
    return modelInsLLM
