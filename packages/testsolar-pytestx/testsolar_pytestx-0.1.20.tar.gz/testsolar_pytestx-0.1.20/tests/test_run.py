import io
from pathlib import Path
from unittest import TestCase

import dacite.exceptions
import pytest
from testsolar_testtool_sdk.model.testresult import ResultType
from testsolar_testtool_sdk.pipe_reader import read_test_result

from run import run_testcases_from_args


class TestExecuteEntry(TestCase):
    testdata_dir: str = str(
        Path(__file__).parent.parent.absolute().joinpath("testdata")
    )

    def test_run_testcases_from_args(self):
        pipe_io = io.BytesIO()
        run_testcases_from_args(
            args=[
                "run.py",
                Path.joinpath(Path(self.testdata_dir), "entry.json"),
            ],
            workspace=self.testdata_dir,
            pipe_io=pipe_io,
        )

        pipe_io.seek(0)
        start = read_test_result(pipe_io)
        self.assertEqual(start.ResultType, ResultType.RUNNING)

    def test_raise_error_when_param_is_invalid(self):
        with self.assertRaises(dacite.exceptions.MissingValueError):
            pipe_io = io.BytesIO()
            run_testcases_from_args(
                args=[
                    "run.py",
                    Path.joinpath(Path(self.testdata_dir), "bad_entry.json"),
                ],
                workspace=self.testdata_dir,
                pipe_io=pipe_io,
            )

    @pytest.mark.skip("暂时未实现，需要执行出错时上报忽略状态")
    def test_continue_run_when_one_case_is_not_found(self):
        pipe_io = io.BytesIO()
        run_testcases_from_args(
            args=[
                "run.py",
                Path.joinpath(Path(self.testdata_dir), "entry_1_case_not_found.json"),
            ],
            workspace=self.testdata_dir,
            pipe_io=pipe_io,
        )

        pipe_io.seek(0)
        start = read_test_result(pipe_io)
        self.assertEqual(start.ResultType, ResultType.IGNORED)
