"""Acceleromenter processing module"""

from typing import Tuple
from logger import logger
from singleton import Singleton
from string_utility import is_checksum_valid, is_string_valid
import datetime


class MessageParser(Singleton):
    """The message parser class"""

    def __init__(self) -> None:
        self.total_messages = 0
        self.valid_messages = 0
        self.invalid_checksum_messages = 0
        self.max_x = 0
        self.max_y = 0
        self.max_z = 0
        self.alrets = 0
        self.is_z_axis_offset_enabled = False
        self.alrets_threshold_counter = 0
        self.alrets_counter = 0

    def toggle_z_axis_offset(self):
        """Toggle z-axiss offset"""
        if self.is_z_axis_offset_enabled:
            self.is_z_axis_offset_enabled = False
            logger.debug("z-axis offset disabled")
        else:
            self.is_z_axis_offset_enabled = True
            logger.debug("z-axis offset enabled")

    def parse_line(self, input_str: str) -> str:
        """Parse accelerationn line

        Update internal statistics and
        process the string

        Args:
            input_str (str): The acceleration line
        """
        self.total_messages += 1

        if not is_string_valid(input_str):
            return None

        if not is_checksum_valid(input_str):
            self.invalid_checksum_messages += 1
            return None

        self.valid_messages += 1

        g_x, g_y, g_z = self.__extrat_x_y_x(input_str)

        # apply z-axis offset if enabled
        g_z = g_z - 1 if self.is_z_axis_offset_enabled else g_z

        # save max g
        self.max_x = g_x if g_x > self.max_x else self.max_x
        self.max_y = g_y if g_y > self.max_y else self.max_y
        self.max_z = g_z if g_z > self.max_z else self.max_z

        # check absolute y-axis g acceleration
        if g_y > 0.2:
            self.alrets_threshold_counter += 1
        else:
            self.alrets_threshold_counter = 0

        return_str = f"X={g_x:.2f}, Y={g_y:.2f}, Z={g_z:.2f}"

        # if 3 consecutive messages, reset and raise the alert
        if self.alrets_threshold_counter >= 3:
            return_str += " [ALERT]"
            self.alrets_counter += 1

        logger.info(return_str)
        return return_str

    @staticmethod
    def __extrat_x_y_x(input_str: str) -> Tuple[int, int, int]:
        """Extract g acceleration from input string

        Args:
            input_str (str): The valid input string

        Returns:
            Tuple[int, int, int]: g acceleration on x,y and z axis
        """
        raw_x = MessageParser.hex_to_signed_int(input_str[3:6])
        raw_y = MessageParser.hex_to_signed_int(input_str[6:9])
        raw_z = MessageParser.hex_to_signed_int(input_str[9:12])
        return (raw_value / 64 for raw_value in [raw_x, raw_y, raw_z])

    @staticmethod
    def hex_to_signed_int(hex_str: str) -> int:
        """Convert hex tring into int

        Generate a 12-bit signed integer
        from a hex string of 3 digits

        Args:
            hex_str (str): The input hex string of 3 digits

        Returns:
            int: The signed 12-bit integer
        """

        unsigned_value = int(hex_str, base=16)

        max_positive_value = 2**11 - 1

        if unsigned_value > max_positive_value:
            # negative number
            return -(2**12 - unsigned_value)

        # positive number
        return unsigned_value

    def parse(
        self, input_file: str = "sample_data.txt", output_file: str = "sample_out.txt"
    ) -> None:
        """Parse file

        Parse an input file acceleration messages.
        The new line delimeter used is `\\r\\n`

        Args:
            input_file (str, optional): The input file to be parsed.
            Defaults to "sample_data.txt".
            output_file (str, optional): The otuput file.
            Defaults to "sample_out.txt".
        """

        # UTC timestamp in ISO-8601 format
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat() + 'Z'

        with open(input_file, "r", newline="\r\n", encoding="utf-8") as file:
            for line in file:
                self.parse_line(line)

        # Open input and output files
        with open(
            input_file, "r", newline="\r\n", encoding="utf-8"
        ) as input_file, open(output_file, "w", encoding="utf-8") as output_file:
            # timestamp header
            print(timestamp, file=output_file)

            for line in input_file:
                returnt_str = self.parse_line(line)
                if returnt_str:
                    print(returnt_str, file=output_file)

    def print_statistics(self) -> None:
        """Print statistics"""
        print("-" * 30)
        print("STATISTICS")
        print(f"Total messages: {self.total_messages}")

        if self.valid_messages > 0:
            print("Valid message:", end=" ")
            print(self.valid_messages, end=" - ")
            print(f"{self.valid_messages/self.total_messages:.2%}")
            print("Invalid checksum messages:", end=" ")
            print(self.invalid_checksum_messages, end=" - ")
            print(f"{self.invalid_checksum_messages/self.total_messages:.2%}")
            print(f"Total alerts: {self.alrets_counter}", end=" - ")
            print(f"{self.alrets_counter/self.total_messages:.2%}")
            print(f"Max G X-Axis: {self.max_x:.2}")
            print(f"Max G Y-Axis: {self.max_y:.2}")
            print(f"Max G Z-Axis: {self.max_z:.2}")

        print("-" * 30)


def main():
    """Script main function"""

    parser = MessageParser()
    parser.is_z_axis_offset_enabled = False
    parser.parse()
    parser.print_statistics()


if __name__ == "__main__":
    main()
