import contextlib
import io
import logging
import os.path
import tempfile

import pytest
from translator import run_translator
from vm import run_vm


@pytest.mark.golden_test("golden/*.yml")
def test_asm(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as temp_dir_name:
        source_code = os.path.join(temp_dir_name, "source_code.s")
        input_file = os.path.join(temp_dir_name, "input_file.txt")
        target = os.path.join(temp_dir_name, "target.json")

        with open(source_code, "w", encoding="utf-8") as file:
            file.write(golden["source"])
        with open(input_file, "w", encoding="utf-8") as file:
            file.write(golden["stdin"])

        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            run_translator(source_code, target)
            run_vm(target, input_file)

        with open(target, encoding="utf-8") as file:
            target = file.read()

        logs = ""
        with open(golden["logs"], encoding="utf-8") as file:
            logs = file.read()

        assert target == golden["target"]
        assert stdout.getvalue() == golden["stdout"]
        print(logs)
        assert caplog.text == logs
