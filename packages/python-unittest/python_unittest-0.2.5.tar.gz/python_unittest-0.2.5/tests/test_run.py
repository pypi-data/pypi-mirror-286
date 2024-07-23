import io
import os
import json
from pathlib import Path

from testsolar_testtool_sdk.pipe_reader import read_test_result
from src.run import run_testcases_from_args

testdata_dir: str = str(Path(__file__).parent.absolute().joinpath("testdata"))


def test_run_all_testcases():
    with open(os.path.join(testdata_dir, "test_entry.json"), "w") as f:
        content = {
            "TaskId": "aa",
            "ProjectPath": testdata_dir,
            "FileReportPath": "",
            "Collectors": [],
            "Context": {},
            "TestSelectors": [
                "."
            ]
        }
        json.dump(content, f)
        
    pipe_io = io.BytesIO()
    run_testcases_from_args(
        args=["run.py", Path.joinpath(Path(testdata_dir), "test_entry.json")],
        workspace=testdata_dir,
        pipe_io=pipe_io,
    )

    pipe_io.seek(0)
    for i in range(6):
        re = read_test_result(pipe_io)
        assert re.Test.Name
        assert re.ResultType
        assert re.Steps
        assert re.StartTime
        assert re.EndTime

def test_run_file():
    with open(os.path.join(testdata_dir, "test_entry.json"), "w") as f:
        content = {
            "TaskId": "aa",
            "ProjectPath": testdata_dir,
            "FileReportPath": "",
            "Collectors": [],
            "Context": {},
            "TestSelectors": [
                "test_demo02.py"
            ]
        }
        json.dump(content, f)
        
    pipe_io = io.BytesIO()
    run_testcases_from_args(
        args=["run.py", Path.joinpath(Path(testdata_dir), "test_entry.json")],
        workspace=testdata_dir,
        pipe_io=pipe_io,
    )

    pipe_io.seek(0)
    for i in range(2):
        re = read_test_result(pipe_io)
        assert re.Test.Name
        assert re.ResultType
        assert re.Steps
        assert re.StartTime
        assert re.EndTime
        
def test_run_dir():
    with open(os.path.join(testdata_dir, "test_entry.json"), "w") as f:
        content = {
            "TaskId": "aa",
            "ProjectPath": testdata_dir,
            "FileReportPath": "",
            "Collectors": [],
            "Context": {},
            "TestSelectors": [
                "test_demo01"
            ]
        }
        json.dump(content, f)
        
    pipe_io = io.BytesIO()
    run_testcases_from_args(
        args=["run.py", Path.joinpath(Path(testdata_dir), "test_entry.json")],
        workspace=testdata_dir,
        pipe_io=pipe_io,
    )

    pipe_io.seek(0)
    for i in range(4):
        re = read_test_result(pipe_io)
        assert re.Test.Name
        assert re.ResultType
        assert re.Steps
        assert re.StartTime
        assert re.EndTime
        
def test_run_class():
    with open(os.path.join(testdata_dir, "test_entry.json"), "w") as f:
        content = {
            "TaskId": "aa",
            "ProjectPath": testdata_dir,
            "FileReportPath": "",
            "Collectors": [],
            "Context": {},
            "TestSelectors": [
                "test_demo01/test_demo04.py?MyTest01"
            ]
        }
        json.dump(content, f)
        
    pipe_io = io.BytesIO()
    run_testcases_from_args(
        args=["run.py", Path.joinpath(Path(testdata_dir), "test_entry.json")],
        workspace=testdata_dir,
        pipe_io=pipe_io,
    )

    pipe_io.seek(0)
    for i in range(2):
        re = read_test_result(pipe_io)
        assert re.Test.Name
        assert re.ResultType
        assert re.Steps
        assert re.StartTime
        assert re.EndTime
        
def test_run_case():
    with open(os.path.join(testdata_dir, "test_entry.json"), "w") as f:
        content = {
            "TaskId": "aa",
            "ProjectPath": testdata_dir,
            "FileReportPath": "",
            "Collectors": [],
            "Context": {},
            "TestSelectors": [
                "test_demo01/test_demo04.py?name=MyTest01/test_01"
            ]
        }
        json.dump(content, f)
        
    pipe_io = io.BytesIO()
    run_testcases_from_args(
        args=["run.py", Path.joinpath(Path(testdata_dir), "test_entry.json")],
        workspace=testdata_dir,
        pipe_io=pipe_io,
    )

    pipe_io.seek(0)
    for i in range(1):
        re = read_test_result(pipe_io)
        assert re.Test.Name
        assert re.ResultType
        assert re.Steps
        assert re.StartTime
        assert re.EndTime