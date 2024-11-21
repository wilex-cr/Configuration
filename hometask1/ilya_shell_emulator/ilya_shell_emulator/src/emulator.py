import tarfile
import csv
import os
import datetime
import sys
import io  # Import io module


class Emulator:
    def __init__(self, computername, filesystem):
        self.current_path = "/"
        self.computername = computername
        try:
            self.filesystem = tarfile.open(filesystem, "r")
        except FileNotFoundError:
            print(f"Error: Filesystem file '{filesystem}' not found. Exiting.")
            sys.exit(1)
        self.history = []

    def execute(self):
        while True:
            command = input(
                f'user@{self.computername}:{self.current_path} ')
            self.history.append(command)
            self.execute_command(command)

    def execute_command(self, command):
        """Parses and executes the given shell command."""
        command_parts = command.strip().split()

        if not command_parts:
            print("No command entered. Please try again.")
            return

        command_name = command_parts[0]

        if command_name == "ls":
            path = command_parts[1] if len(
                command_parts) > 1 else self.current_path
            self.ls(path)
        elif command_name == "cd":
            try:
                path = command_parts[1]
                self.cd(path)
            except IndexError:
                print("cd: missing operand")
        elif command_name == "exit":
            self.filesystem.close()
            sys.exit()
        elif command_name == "pwd":
            self.pwd()
        elif command_name == "history":
            self.print_history()
        elif command_name == "mkdir":
            try:
                path = command_parts[1]
                self.mkdir(path)
            except IndexError:
                print("mkdir: missing operand")
        else:
            print(f"{command_name}: command not found")

    def ls(self, path):
        """Lists the contents of the specified directory within the virtual filesystem."""
        file_list = self.filesystem.getnames()

        if path.startswith("/"):
            full_path = path
        else:
            full_path = os.path.join(
                self.current_path, path).replace("\\", "/")

        if full_path == "/":
            result = set()
            for item in file_list:
                tarinfo = self.filesystem.getmember(item)
                if "/" not in item:
                    result.add(item + ("/" if tarinfo.isdir() else ""))
                else:
                    parts = item.split("/")
                    result.add(
                        parts[0] + ("/" if self.filesystem.getmember(parts[0]).isdir() else ""))
            for item in sorted(list(result)):
                print(item)
        else:
            try:
                tarinfo = self.filesystem.getmember(full_path[1:])
                prefix = full_path[1:] + "/"
                result = set()
                for item in file_list:
                    if item.startswith(prefix) and item != prefix:
                        rest = item[len(prefix):]
                        tarinfo = self.filesystem.getmember(item)
                        if "/" not in rest:
                            result.add(rest + ("/" if tarinfo.isdir() else ""))
                        else:
                            parts = rest.split("/")
                            result.add(
                                parts[0] + ("/" if self.filesystem.getmember(prefix + parts[0]).isdir() else ""))
                for item in sorted(list(result)):
                    print(item)
            except KeyError:
                print(f"ls: {path}: No such file or directory")

    def cd(self, path):
        """Changes the current directory within the virtual filesystem."""
        if path == "/":
            self.current_path = "/"
            return

        if path.startswith("/"):
            full_path = path
        else:
            full_path = os.path.join(
                self.current_path, path).replace("\\", "/")

        try:
            tarinfo = self.filesystem.getmember(full_path[1:])

            if tarinfo.isdir():
                self.current_path = full_path
            else:
                print(f"cd: {path}: Not a directory")
        except KeyError:
            print(f"cd: can't cd to {path}: No such file or directory")

    def pwd(self):
        """Prints the current working directory within the virtual filesystem."""
        print(self.current_path)

    def print_history(self):
        """Prints the command history with line numbers."""
        for i, command in enumerate(self.history):
            print(f"{i+1} {command}")

    def mkdir(self, path):
        """Creates a new directory within the virtual filesystem (not implemented)."""
        if path.startswith("/"):
            full_path = path[1:]
        else:
            full_path = os.path.join(
                self.current_path[1:], path).replace("\\", "/")

        try:
            self.filesystem.getmember(full_path)
            print(f"mkdir: cannot create directory '{path}': File exists")
            return
        except KeyError:
            pass

        tarinfo = tarfile.TarInfo(full_path)
        tarinfo.type = tarfile.DIRTYPE
        tarinfo.mode = 0o755
        tarinfo.mtime = datetime.datetime.now().timestamp()

        temp_tar_path = "temp.tar"
        with tarfile.open(temp_tar_path, "w") as temp_tar:
            for member in self.filesystem.getmembers():
                temp_tar.addfile(member, self.filesystem.extractfile(member))

            temp_tar.addfile(tarinfo)

        self.filesystem.close()
        os.replace(temp_tar_path, self.filesystem.name)

        # Reopen the archive
        self.filesystem = tarfile.open(self.filesystem.name, "r")
