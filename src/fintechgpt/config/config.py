import yaml

"""
项目配置文件类
"""
class Config:
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path
        self.load_config()

    def load_config(self):
        with open(self.config_file_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)

    # 获取embedding模型相关信息
    def get_embedding_model(self):
        return self.config.get('model').get('embedding', "GanymedeNil/text2vec-large-chinese")

    def get_llm_model(self):
        return self.config.get('model').get('llm', {})

    def get_data_conf(self):
        return self.config.get('data', {})
    
    def validate_config(self):
        required_keys = ['model', 'data']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required key in config: {key}")
            else:
                model_keys = ['embedding', 'llm']
                for key in model_keys:
                    if key not in self.config.get('model'):
                        raise ValueError(f"Missing required key in config: {key}")

            
if __name__ == "__main__":
    config_file_path = "../../../conf/fintechgpt.yaml"
    model_config = Config(config_file_path)

    try:
        model_config.validate_config()
    except ValueError as e:
        print(f"Error in configuration: {e}")
    else:
        print("Configuration is valid.")

        print("embedding Model :", model_config.get_embedding_model())
        print("llm Model :", model_config.get_llm_model())

