import logging
import logging.config

from configparser import ConfigParser

from util.FileUtil import FileUtil

class LoggerUtil:
    """
    LoggerUtil is a utility class that provides static methods for loading logging configurations.
    It is designed to initialize logging settings from a configuration file, allowing for a
    centralized and standardized logging setup across the application.
    """
    @staticmethod
    def loadLogger(logging_config_file_path):
        """
        Load logging configuration from the specified file path.

        This method uses the `fileConfig` function from the `logging.config` module to load
        the logging configuration. It ensures that existing loggers are not disabled unless
        otherwise specified in the configuration file.

        Parameters:
        logging_config_file_path (str): The file path to the logging configuration file.

        Returns:
        None
        """
        logging.config.fileConfig(logging_config_file_path,disable_existing_loggers=False)

    @staticmethod
    def loadLogger_defaults():
        """
        Load default logging configuration.

        This method determines the default logging configuration file path by using the project's
        root path obtained from the FileUtil utility class. It then calls the `loadLogger` method
        to actually load the logging configurations from the default file.

        The default logging configuration file is assumed to be located in the `/config/logging.conf`
        directory relative to the project root.

        Parameters:
        None

        Returns:
        None
        """
        default_logging_config_file_path = FileUtil.getProjectRootPath() + '/config/logging.conf'
        LoggerUtil.loadLogger(default_logging_config_file_path)

class PropertiesUtil:
    """
    The PropertiesUtil class offers utility methods for reading properties from
    a properties configuration file. It provides functionality to read configurations
    both from a specified path and from a default configuration file.

    Static methods:
        - read_properties_file: Reads properties from a specified configuration file.
        - read_properties_file_defaults: Reads properties from the default configuration file.
    """
    @staticmethod
    def read_properties_file(config_path):
        """
        Reads a properties file from the given path and returns a dictionary of
        configuration properties.

        The method reads the default section of the configuration file and returns
        the properties as key-value pairs. Sections within the file are ignored.
        The method assumes the configuration file format is similar to the INI format,
        where properties are not explicitly assigned to any section.

        :param config_path: The path to the configuration file.
        :type config_path: str
        :return: A dictionary containing the configuration properties.
        :rtype: dict
        """
        # Create a ConfigParser object
        config = ConfigParser()

        # Read the properties file
        config.read(config_path)

        # Fetch all the properties
        properties = {}
        if config.defaults():
            for key in config.defaults():
                properties[key] = config.defaults()[key]

        return properties

    @staticmethod
    def read_properties_file_defaults():
        """
        Reads the default properties file from the predefined path and returns a
        dictionary of configuration properties.

        This method utilizes read_properties_file internally, pointing it to the
        default configuration file located in the 'config' directory of the project's
        root. It assumes the configuration file is named 'config.properties'.

        :return: A dictionary containing the configuration properties from the default file.
        :rtype: dict
        """
        # Define the path to the default configuration file
        default_config_path = FileUtil.getProjectRootPath() + '/config/config.properties'

        # Read properties from the default configuration file
        return PropertiesUtil.read_properties_file(default_config_path)
