import os


def env_var(var_name, default_value=None):
    if var_name in os.environ:
        value = os.environ[var_name]
    elif default_value is not None:
        value = default_value
    else:
        raise EnvironmentError(f"{var_name} not found!")
    if var_name not in ["INPUT_GITHUBTOKEN", "INPUT_NOTIFY_PASS", "INPUT_NOTIFY_USER", "INPUT_NOTIFY_URL"]:
        print(f"{var_name}={value}")
    return value
