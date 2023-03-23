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
    argument_parser.add_argument("--parse_latest_version", metavar="<true>",
        help="Takes '$(git tag)' and returns the highest version in the list", default="false")
    parsed_commands = argument_parser.parse_args()

    if (parsed_commands.parse_latest_version == "true"):
        version_list = parsed_commands.version.split("\n")
        highest = [0, 0, 0]

        for i in range(0, len(version_list)):
            i_version = version_list[i]
            i_version = i_version.replace("v", "")

            i_version_tuple = i_version.split(".")
            if (len(i_version_tuple) != 3):
                continue

            i_version_tuple[0] = int(i_version_tuple[0])
            i_version_tuple[1] = int(i_version_tuple[1])
            i_version_tuple[2] = int(i_version_tuple[2])

            if (highest == None):
                highest = i_version_tuple
                continue
            else:
                if (i_version_tuple[0] > highest[0]):
                    highest = i_version_tuple
                    continue
                if (i_version_tuple[0] >= highest[0] and i_version_tuple[1] > highest[1]):
                    highest = i_version_tuple
                    continue
                if (i_version_tuple[0] >= highest[0] and i_version_tuple[1] >= highest[1] and i_version_tuple[2] >= highest[2]):
                    highest = i_version_tuple
                    continue

        if (highest[0] != 0 or highest[1] != 0 or highest[2] != 0):
            print(f"v{highest[0]}.{highest[1]}.{highest[2]}")
            sys.exit(0)
        else:
            sys.exit(-1)

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
