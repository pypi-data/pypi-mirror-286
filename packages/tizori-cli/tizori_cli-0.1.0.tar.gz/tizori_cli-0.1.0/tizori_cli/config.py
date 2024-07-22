import yaml

def load_config():
    """Load the config file if it exists, otherwise create it"""
    try:
        with open("config.yaml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {"base_url": ""}

def save_config(config):
    try:
        with open("config.yaml", "w+") as f:
            yaml.safe_dump(config, f)
    except Exception as e:
        print(f"Error saving config: {e}")

def set_config_value(key, value):
    config = load_config()
    config[key] = value
    save_config(config)

def delete_config_value(key):
    config = load_config()
    config.pop(key, None)
    save_config(config)

def get_config_value(key):
    config = load_config()
    return config.get(key)