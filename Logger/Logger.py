import logging
import os


class LoggerSetup:
    """
    A class to set up logging configuration for both file and console output.
    """

    def __init__(self, log_file='log_info.log'):
        """
        Initialize the LoggerSetup with a log file name.

        Args:
            log_file (str): The filename of the log file. Default is 'log_info.log'.
        """
        self.log_file = log_file

    def setup_logging(self):
        """
        Sets up logging configuration for both file and console output.
        """
        # Configure logging to file with DEBUG level for detailed logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG,
            format='<\nTime: %(asctime)s \nFileName: %(filename)s \nName:%(name)s \nLevel:%(levelname)s \nLine:%(lineno)d \nMessages:\n%(message)s\n>\n'
        )

        # Configure logging to console for ERROR level messages and above
        console = logging.StreamHandler()
        console.setLevel(logging.ERROR)  # Console will only show errors
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)

        # Add the console handler to the root logger
        logging.getLogger(__name__).addHandler(console)

        # Log an initial message to ensure the log file is created immediately
        logging.info("Logging setup complete. Log file initialized.")

    def create_log(self):
        """
        Prints the absolute path of the log file and checks if it was successfully created.
        """
        # Get absolute path of the log file
        log_file_path = os.path.abspath(self.log_file)

        # Print where the log file is located
        print(f"Log file will be created at: {log_file_path}")

        # Check if the log file exists and print appropriate message
        if os.path.exists(log_file_path):
            print(f"Log file '{log_file_path}' created successfully.")
        else:
            print(f"Failed to create log file '{log_file_path}'.")

    def log_test_message(self):
        """
        Logs a test message to confirm that logging is working.
        """
        logging.debug('Test message logged.')

    def initialize(self):
        """
        Initialize all necessary steps for logging setup.
        This method serves as a single entry point for setting up logging.
        """
        self.setup_logging()  # Configure logging
        self.create_log()     # Verify log file creation
        self.log_test_message()  # Log a test message


def main():
    """
    Main function to demonstrate the usage of the LoggerSetup class.
    """
    # Initialize the LoggerSetup instance and call initialize()
    logger = LoggerSetup()
    logger.initialize()  # Perform all setup steps in one call


if __name__ == "__main__":
    main()
