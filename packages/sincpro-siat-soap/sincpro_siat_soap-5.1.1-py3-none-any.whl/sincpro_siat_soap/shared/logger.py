import logging

import logzero

from sincpro_siat_soap.shared.settings import settings_soap_siat

logzero.loglevel(logging.INFO)

if settings_soap_siat.debug:
    logzero.loglevel(logging.DEBUG)

    if not settings_soap_siat.exists_config:
        logzero.logger.warning(
            "The configuration file does not exist, using the environment variables or default values"
        )

    logzero.logger.debug("Debug mode is enabled")

    # Print the configuration file
    for section in settings_soap_siat.conf_file.sections():
        logzero.logger.debug(f"[{section}]")
        for key, value in settings_soap_siat.conf_file.items(section):
            logzero.logger.debug(f"{key} = {value}")

logzero.logfile("/tmp/sp_siat.log")
logger = logzero.logger
