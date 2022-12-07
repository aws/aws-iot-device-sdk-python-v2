import argparse
import sys

# A simple little helper script for increasing the semantic version passed in.
# Used in the CD workflow.


def main():
    argument_parser = argparse.ArgumentParser(
        description="Get a new semantic version bumped by the passed-in string")
    argument_parser.add_argument("--version", metavar="<1.2.3 for example>",
                                 required=True, help="The version string to update")
    argument_parser.add_argument("--type", metavar="<string containing PATCH, MINOR, or MAJOR>",
                                 required=True, help="Which version number to bump")
    parsed_commands = argument_parser.parse_args()

    version_tuple = parsed_commands.version.split(".")
    if len(version_tuple) != 3:
        print("0.0.0")  # Error
        sys.exit(1)

    if "PATCH" in parsed_commands.type:
        version_tuple[2] = str(int(version_tuple[2]) + 1)
    elif "MINOR" in parsed_commands.type:
        version_tuple[1] = str(int(version_tuple[1]) + 1)
        version_tuple[2] = "0"
    elif "MAJOR" in parsed_commands.type:
        version_tuple[0] = str(int(version_tuple[0]) + 1)
        version_tuple[1] = "0"
        version_tuple[2] = "0"
    else:
        print("0.0.0")  # error
        sys.exit(1)

    print(f"{version_tuple[0]}.{version_tuple[1]}.{version_tuple[2]}")
    sys.exit(0)


if __name__ == "__main__":
    main()
