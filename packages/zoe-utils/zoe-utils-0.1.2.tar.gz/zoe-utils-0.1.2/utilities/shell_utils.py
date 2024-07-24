import subprocess


class ShellTask:
    def __init__(self, command):
        self.command = command

    def run(self):
        with subprocess.Popen(self.command,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              shell=True,
                              text=True,
                              bufsize=1,
                              universal_newlines=True) as process:

            for line in process.stdout:
                print(line.strip())  # Log each line of output
            _, errors = process.communicate()

            if process.returncode != 0:
                print(f"Error executing command: '{self.command}', error: {errors}")
                raise subprocess.CalledProcessError(process.returncode, self.command, output=errors)
            else:
                return process.returncode
