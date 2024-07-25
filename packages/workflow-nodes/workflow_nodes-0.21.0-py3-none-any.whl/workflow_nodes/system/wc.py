# Copyright 2024 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import subprocess
import sys

import click
from xmlhelpy import Path
from xmlhelpy import option

from .main import system


@system.command()
@option("file", char="f", param_type=Path(path_type="file", exists=True))
@option(
    "bytes",
    char="c",
    var_name="count_bytes",
    is_flag=True,
    description="Print the number of bytes.",
)
@option("chars", char="m", is_flag=True, description="Print number of chars.")
@option("words", char="w", is_flag=True, description="Print the number of words.")
@option("lines", char="l", is_flag=True, description="Print number of lines.")
@option(
    "max-line-length",
    char="L",
    is_flag=True,
    description="Print the maximum line length.",
)
def wc(file, count_bytes, chars, words, lines, max_line_length):
    """Wrapper node for wc."""
    cmd = ["wc"]

    if count_bytes:
        cmd.append("-c")
    if chars:
        cmd.append("-m")
    if lines:
        cmd.append("-l")
    if max_line_length:
        cmd.append("-L")
    if words:
        cmd.append("-w")
    if file:
        cmd.append(file)

    click.echo(cmd, err=True)
    sys.exit(subprocess.run(cmd).returncode)
