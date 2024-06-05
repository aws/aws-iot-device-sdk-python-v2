# Test for Greengrass Discovery Sample

Greengrass discovery test runs using [Greengrass Development Kit Command-Line Interface](https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-development-kit-cli.html) (GDK CLI).

### Greengrass discovery component

For Greengrass discovery sample to work, a Greengrass component subscribed to a particular topic is required.  
The following files defines this custom component:

- [gdk-config.json](./gdk-config.json) - `gdk` reads this file to build and publish component.
- [copy_files.sh](./copy_files.sh) - utility to copy all required files for `gdk` to be able to build the component.
- [recipe.yaml](./recipe.yaml) - defines a component's details, dependencies, artifacts, and lifecycles.
- [hello_world_subscriber.py](./hello_world_subscriber.py) - a simple Greengrass client that subscribes to a given topic using Greengrass IPC.

### How the test runs

The first step is to build GreengrassV2 component artifacts and recipes from its source code:

```shell
gdk component build
```

Then the following command builds the testing module:

```shell
gdk test-e2e build
```

Finally, the test can run:

```shell
gdk test-e2e run
```

The test behavior is defined in the [component.feature](./gg-e2e-tests/src/main/resources/greengrass/features/component.feature)
config file using a domain-specific language called [Gherkin](https://docs.aws.amazon.com/greengrass/v2/developerguide/gg-testing-framework.html).

The test spins up Greengrass core, installs and configures Greengrass component dependencies (including the custom
Greengrass component described in the previous section). After everything is set up, it performs checks. They are defined
at the very bottom of the file and basically grep a log file for specific messages.

On completion, the test creates log files in `testResult` directory with the run details. The component's logs are stored
in `testResult/gg-<RANDOM_STRING>/software.amazon.awssdk.sdk-gg-test-discovery.log` file. Though, if error occurred before
the component started its execution, this file might be absent.
