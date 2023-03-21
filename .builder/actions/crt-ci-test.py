import Builder
import re

class CiTest(Builder.Action):

    def _write_environment_script_secret_to_env(self, env, secret_name):
        mqtt5_ci_environment_script = env.shell.get_secret(secret_name)
        env_line = re.compile('^export\s+(\w+)=(.+)')

        lines = mqtt5_ci_environment_script.splitlines()
        for line in lines:
            env_pair_match = env_line.match(line)
            if env_pair_match.group(1) and env_pair_match.group(2):
                env.shell.setenv(env_pair_match.group(1), env_pair_match.group(2), quiet=True)


    def run(self, env):

        actions = []

        try:
            self._write_environment_script_secret_to_env(env, "ci/sdk-unit-testing")

            env.shell.exec(["python3", "-m", "unittest", "discover", "--verbose"], check=True)
        except:
            print(f'Failure while running tests')
            actions.append("exit 1")

        return Builder.Script(actions, name='ci-test')
