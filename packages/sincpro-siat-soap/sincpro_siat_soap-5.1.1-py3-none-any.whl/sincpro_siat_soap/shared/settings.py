import importlib
import os
import traceback
from configparser import ConfigParser

PROVIDED_CONFIG_FILE_PATH = os.getenv("SOAP_SIAT_CONFIG_FILE", None)
DEFAULT_PRODUCTION_FILE_PATH = "/home/odoo/soap_siat.ini"
DEV_CONFIG_FILE = str(
    importlib.resources.files("sincpro_siat_soap.conf").joinpath("soap_siat.ini")
)


class SettingsSoapSIAT:
    exists_config = False
    used_config_file = None

    # Properties
    token = None
    environment = None
    modality = None
    digital_sign_password = None
    debug = None
    sync_obj_timeout = None

    def __init__(self):
        self._load_config_file()
        self._setup_properties()

    def _load_config_file(self):
        """
        Define which config file will be loaded
        the priority order is the following:
        1. Provided config file through the environment variable SOAP_SIAT_CONFIG_FILE
        2. Production default config file
        3. Development default config file if the production file does not exist
        4. Variables from environment based if the config file does not exist
        """
        default_config_file = DEV_CONFIG_FILE
        if os.path.isfile(DEFAULT_PRODUCTION_FILE_PATH):
            default_config_file = DEFAULT_PRODUCTION_FILE_PATH
        self.used_config_file = PROVIDED_CONFIG_FILE_PATH or default_config_file
        try:
            self.conf_file = ConfigParser()
            self.conf_file.read(self.used_config_file)
            if not self.conf_file:
                raise Exception("Config file is empty")

            print(f"Config file loaded: {self.used_config_file}")
            self.exists_config = True

        except Exception as error:
            trace = traceback.format_exc()
            print(
                f"The config file was not loaded {self.used_config_file}: \n{error} \n \n {trace}"
            )
            self.exists_config = False

    def _setup_properties(self):
        self.token = (
            self.conf_file.get("siat", "token")
            or os.getenv("SIAT_TOKEN", None)
            or os.getenv("SOAP_SIAT_TOKEN", None)
        )

        self.environment = (
            self.conf_file.get("siat", "environment")
            or os.getenv("SIAT_ENVIRONMENT", None)
            or os.getenv("SOAP_SIAT_ENVIRONMENT", None)
        )

        self.modality = (
            self.conf_file.get("siat", "modality")
            or os.getenv("SIAT_MODALITY", None)
            or os.getenv("SOAP_SIAT_MODALITY", None)
        )

        self.digital_sign_password = (
            self.conf_file.get("siat", "digital_sign_password")
            or os.getenv("SIAT_KEY_PASSWORD", None)
            or os.getenv("SOAP_SIAT_KEY_PASSWORD", None)
        )
        self.debug = (
            self.conf_file.get("siat", "debug")
            or os.getenv("SP_SIAT_LOG_LEVEL", None)
            or os.getenv("SOAP_SIAT_LOG_LEVEL", None)
        )

        self.sync_obj_timeout = (
            self.conf_file.get("siat", "sync_obj_timeout")
            or os.getenv("SIAT_SYNC_OBJ_TIMEOUT", None)
            or os.getenv("SOAP_SIAT_SYNC_OBJ_TIMEOUT", None)
        )


settings_soap_siat = SettingsSoapSIAT()
