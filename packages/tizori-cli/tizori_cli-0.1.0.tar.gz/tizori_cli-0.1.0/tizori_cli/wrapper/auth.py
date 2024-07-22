from tizori_cli.config import set_config_value

def login(req_wrap, username, password):
    endpoint = "/auth/login"
    response, status = req_wrap.post(endpoint, data={"username": username, "password": password})
    if status == 200:
        token = response.get("token")
        set_config_value("token", token)
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")

def logout():
    set_config_value("token", "")
    return

def reset_password(req_wrap, username):
    endpoint = "/auth/reset-password"
    response, status = req_wrap.post(endpoint, data={"username": username})
    if status == 200:
        return True, response.get("password")
    else:
        return False, response.get("detail", "Unknown Error")