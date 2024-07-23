#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : nickdecodes
@Email   : nickdecodes@163.com
@Usage   :
@FileName: exec.py
@DateTime: 2024/7/19 12:08
@SoftWare: 
"""

import time
import logging
import subprocess
from typing import Union, Iterable, Tuple


class CommandExecutor:
    """
    A command executor class.

    Attributes:
        bin_path (str): The path to the binary executable.
        logger (logging.Logger): The logger object for logging messages.
    """

    def __init__(self, bin_path: str = 'ffmpeg', logger=None) -> None:
        """
        Initialize the Command Executor class.

        Args:
            bin_path (str): The path to the binary executable. Defaults to 'ffmpeg'.
        """
        self.bin_path = bin_path
        if logger is None:
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(level=logging.INFO)
        else:
            self.logger = logger
        self.commands = []

    def rebin(self, bin_path: str = 'ffmpeg') -> None:
        """
        reload binary executable. set new path
        :param bin_path: str: The path to the binary executable. Defaults to 'ffmpeg'.
        :return:
        """
        self.bin_path = bin_path

    def run(
            self,
            command: Union[Iterable[str], str] = None,
            timeout: int = None,
            retries: int = 0,
            delay: int = 1,
            alone: bool = False
    ) -> Tuple[int, Union[None, str], Union[None, str]]:
        """
        execute command with retry logic.

        Args:
            command (Union[Iterable[str], str]): The command and its arguments as a list of strings or a single string.
            timeout (int): The timeout in seconds. If the command takes longer than this, it will be terminated.
            retries (int): The number of times to retry the command in case of failure.
            delay (int): The delay in seconds between retries.
            alone (bool): If True, the command will be executed without append bin path.

        Returns:
            Tuple[int, Union[None, str], Union[None, str]]: A tuple containing the return code, the standard output,
            and the standard error output of the command.
        """
        if len(self.commands) > 0:
            _command = command if alone else [self.bin_path, *self.commands]
        else:
            if isinstance(command, str):
                _command = command.split() if alone else [self.bin_path] + command.split()
            else:
                _command = command if alone else [self.bin_path, *command]
        print(_command)

        attempt = 0
        while attempt <= retries:
            self.logger.info(f"Executing command: {' '.join(_command)} (Attempt {attempt + 1})")
            try:
                result = subprocess.run(
                    _command,  # The command to run, as a list of strings.
                    text=True,  # Capture output as text (not bytes).
                    check=True,  # Raise CalledProcessError if command exits with a non-zero status.
                    stdin=subprocess.PIPE,  # Use a pipe for the standard input.
                    stdout=subprocess.PIPE,  # Use a pipe for the standard output.
                    stderr=subprocess.PIPE,  # Use a pipe for the standard error output.
                    timeout=timeout,  # Timeout for the command in seconds.
                    encoding='utf-8',  # Use UTF-8 encoding for the output.
                    errors='replace'  # Replace errors in the output with a placeholder character.
                )

                # Check if the command was successful. If so, return the result.
                if result.returncode == 0:
                    return result.returncode, result.stdout, result.stderr
                else:
                    self.logger.error(f"Command failed with return code {result.returncode}.")
                    if attempt >= retries:
                        return result.returncode, result.stdout, result.stderr

            except subprocess.TimeoutExpired as ex:
                self.logger.error(f"Process timed out: {ex}")
                if attempt >= retries:
                    return -1, None, f"Process timed out: {ex}"
            except subprocess.CalledProcessError as ex:
                self.logger.error(f"Process error: {ex}")
                if attempt >= retries:
                    return ex.returncode, ex.stdout, ex.stderr
            except Exception as ex:
                self.logger.error(f"An unexpected error occurred: {ex}")
                if attempt >= retries:
                    return -1, None, str(ex)

            # Increment attempt counter and sleep before retrying
            attempt += 1
            if attempt <= retries:
                self.logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)

        return -1, None, "All retries failed."

