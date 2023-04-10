import argparse
import asyncio
import importlib
import os
import sys
from typing import Dict

from turbindo.database.codegen import generate_data_accessors
from turbindo.log.logger import Logger


def generate_skeleton_project(name):
    os.mkdir(f"{name}")
    os.mkdir(f"{name}/data")
    os.mkdir(f"{name}/input_output")
    os.mkdir(f"{name}/jobs")
    os.mkdir(f"{name}/machine")
    os.mkdir(f"{name}/server")
    os.mkdir(f"{name}/tests")
    from turbindo import util
    util.render_skel(name)






def main():
    parser = argparse.ArgumentParser()

    _context = "CLI"
    logger = Logger('main')

    parser.add_argument("--test", help="run the testsuite", action="store_true", default=False)
    parser.add_argument("--test_suite", help="specify test suite", type=str, default="*")
    parser.add_argument("--test_case", help="specify test case from suite", type=str, default="*")
    parser.add_argument("--integration_tests", help="run integration tests", action="store_true", default=False)
    parser.add_argument("--io_recording", help="enable io recording", action="store_true", default=False)
    parser.add_argument("--io_mocking", help="enable io mocking", action="store_true", default=False)
    parser.add_argument("--gen_accessors", help="generate the database accessors", action="store_true",
                        default=False)
    parser.add_argument("--gen_test_accessors", help="generate test accessors", action="store_true",
                        default=False)
    parser.add_argument("--data_package", help="data package to use for generation", type=str,
                        default="turbindo.database.default.data_objects")
    parser.add_argument("--generate_skeleton_project", help="generate a skeleton project", type=str, default=False)

    args = parser.parse_args()

    if args.test or args.integration_tests:
        app_loop = asyncio.new_event_loop()

        from turbindo.test import test_system as test_system
        results: Dict[str, Exception] = app_loop.run_until_complete(
            test_system.run_tests(f"turbindo.test.suites{'.integration' if args.integration_tests else ''}",
                                  suite_name=args.test_suite,
                                  case_name=args.test_case))
        status = 0
        for n, e in results.items():
            if e is None:
                logger.log(f"{n}: Pass")
            else:
                status = 1
                logger.error(f"{n}: Fail")
                logger.error(f"{e}")
        from turbindo.database.impl import sqlite
        if sqlite.Sqlite.conn != None:
            app_loop.run_until_complete(sqlite.Sqlite.conn.close())
        app_loop.stop()
        app_loop.close()
        import os
        os._exit(status)
    elif args.generate_skeleton_project:
        generate_skeleton_project(args.generate_skeleton_project)

    elif args.gen_accessors:
        app_loop = asyncio.new_event_loop()
        from turbindo.database.default import classes
        results = app_loop.run_until_complete(generate_data_accessors(classes))
        f = open("turbindo/database/default/accessors.py", "w").write(results)

    elif args.gen_test_accessors:
        app_loop = asyncio.new_event_loop()
        from turbindo.test.data import classes
        results = app_loop.run_until_complete(generate_data_accessors(classes))
        f = open("turbindo/test/data/accessors.py", "w").write(results)


if __name__ == '__main__':
    main()
