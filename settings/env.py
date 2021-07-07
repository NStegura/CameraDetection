import environ

__all__ = ("env", "root")

env = environ.Env(
	DEBUG=(bool, False))
root = environ.Path(__file__) - 2  # get root of the project

# read .env file from default location or ENV_FILE_PATH
env.read_env(env.path("ENV_FILE_PATH", default=root.path("settings/.env")())())