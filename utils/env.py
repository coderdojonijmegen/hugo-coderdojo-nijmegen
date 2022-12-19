import os


def env_var(var_name, default_value=None):
    if var_name in os.environ:
        value = os.environ[var_name]
    elif default_value is not None:
        value = default_value
    else:
        raise EnvironmentError(f"{var_name} not found!")
    if var_name != "INPUT_GITHUBTOKEN":
        print(f"{var_name}={value}")
    return value
