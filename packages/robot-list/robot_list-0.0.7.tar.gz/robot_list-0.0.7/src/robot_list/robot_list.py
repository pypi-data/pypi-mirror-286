"""This module helps to list the robot tests with given robot parameters"""
import json
import os
import re
import subprocess
import xmltodict
import tempfile
import shutil
import sys

help_doc = """
Please provide the robot command or robot flags
Usage:
python -m robot_list.robot_list '--include test1 --exclude test2 tests/'
python -m robot_list.robot_list '-i test1 -e test2 tests/'
python -m robot_list.robot_list '--suite suite1 --test test1 tests/'
python -m robot_list.robot_list '-s suite1 -t test1 tests/'
python -m robot_list.robot_list '--include test1 --exclude test2 --suite suite1 tests/'
python -m robot_list.robot_list '-i test1 -e test2 -s suite1 tests/'

or
from robot_list import robot_list
robot_list = RobotList(command)
robot_list.list_robot_tests()
"""

if len(sys.argv) != 2:
    raise Exception(help_doc)

command = sys.argv[-1]

class RobotList:
    """This class helps to list the robot tests with given robot parameters"""

    _REGEX_PATTERN_FILTER_INCLUDED = (r'--include\s+("[^"]+"|\S+|\'['
                                      r'^\']+\')|-i\s+("[^"]+"|\S+|\'['
                                      r'^\']+\')')
    _REGEX_PATTERN_FILTER_EXCLUDED = (r'--exclude\s+("[^"]+"|\S+|\'['
                                      r'^\']+\')|-e\s+("[^"]+"|\S+|\'['
                                      r'^\']+\')')

    _REGEX_PATTERN_FILTER_SUITE = (r'--suite\s+("[^"]+"|\S+|\'['
                                   r'^\']+\')|-s\s+("[^"]+"|\S+|\'[^\']+\')')

    _REGEX_PATTERN_FILTER_TEST = (r'--test\s+("[^"]+"|\S+|\'[^\']+\')|-t\s+('
                                  r'"[^"]+"|\S+|\'[^\']+\')')

    _REGEX_PATTERN_SRC = r'\s+(\S+)$'

    def __init__(self, cmd):
        """This function initializes the robot parameters"""
        self.command = cmd
        self.__temp_dir_name = tempfile.TemporaryDirectory().name
        self.__xml_file_output = os.path.join(self.__temp_dir_name,
                                              'xunit.xml')

    def __robot_command(self, robot_cmd_flags, src_directory):
        """This function forms the robot command with given flags

        @param robot_cmd_flags: list of robot command flags
        @param src_directory: source directory
        """

        return (f'python -m robot --dryrun -x {self.__xml_file_output} -d '
                f'{self.__temp_dir_name}'
                f' {" ".join(robot_cmd_flags)} {src_directory}').strip()

    def __parse_robot_command(self):
        """This function parses the robot command"""
        suites = itags = etags = src_matches = []
        try:
            itags = re.findall(self._REGEX_PATTERN_FILTER_INCLUDED,
                               self.command)
            etags = re.findall(self._REGEX_PATTERN_FILTER_EXCLUDED,
                               self.command)
            tests = re.findall(self._REGEX_PATTERN_FILTER_TEST,
                               self.command)
            suites = re.findall(self._REGEX_PATTERN_FILTER_SUITE, self.command)
            src_matches = re.findall(self._REGEX_PATTERN_SRC, self.command)
        except Exception as e:
            pass
        tags = []

        # parsing itags
        for tag in itags:
            if len(tag) >= 1:
                tags.append('--include ' + tag[0].strip())

        # parsing etags
        for tag in etags:
            if len(tag) >= 1:
                tags.append('--exclude ' + tag[0].strip())

        # parsing etags
        suites = [suite[0].strip() for suite in suites if len(suite) >= 1]
        return suites, tags, (src_matches[-1] if src_matches
                                          else'').strip()

    def __get_executed_testcases(self, test_data):
        executed_testcases = []
        if isinstance(test_data, dict):
            test_data = [test_data]
        for suite_details in test_data:
            for key, value in suite_details.items():
                if key == 'testsuite':
                    executed_testcases.extend(
                        self.__get_executed_testcases(suite_details[
                                                        'testsuite']))
                elif key == 'testcase':
                    if isinstance(value, dict):
                        testcases = [value]
                    else:
                        testcases = value
                    for test in testcases:
                        executed_testcases.append(test['name'])
        return executed_testcases

    def __executed_tests(self, xunit_xml_path):
        """Reads the xml file and return the list of tests"""
        executed_testcases = []
        # Parse Xunit XML files
        try:
            with open(xunit_xml_path, 'r') as f:
                xunit_xml = f.read()
                json_xml = json.dumps(xmltodict.parse(xunit_xml)).translate(
                    {ord('@'): None})
                xml_log_dict = eval(json_xml)
                executed_testcases = self.__get_executed_testcases(
                    xml_log_dict['testsuite'])
        except FileNotFoundError as e:
            pass
        return executed_testcases

    def __delete_log_files(self):
        """Delete the log files if exists"""
        try:
            for file in os.listdir(self.__temp_dir_name):
                os.remove(os.path.join(self.__temp_dir_name, file))
        except Exception as e:
            pass

    def __delete_log_directory(self):
        """Delete the log directory if exists"""
        try:
            shutil.rmtree(self.__temp_dir_name, ignore_errors=True)
        except Exception as e:
            pass

    @staticmethod
    def __execute_command(cmd, ignore_errors=True):
        """This function executes the command"""
        try:
            subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
        except Exception as e:
            if not ignore_errors:
                raise e

    def list_robot_tests(self):
        """This function lists the robot tests with given robot parameters"""
        tests = {}
        test_list = []
        suites, tags, src_directory = self.__parse_robot_command()
        try:
            if suites:
                for suite in suites:
                    rcmd = self.__robot_command(tags + [f'--suite {suite}'],
                                                src_directory)
                    self.__execute_command(rcmd)
                    tests[suite] = self.__executed_tests(
                        self.__xml_file_output)
                    self.__delete_log_files()
            else:
                rcmd = self.__robot_command(tags, src_directory)
                self.__execute_command(rcmd)
                test_list = self.__executed_tests(self.__xml_file_output)
        except Exception as e:
            pass
        self.__delete_log_files()
        self.__delete_log_directory()
        return tests, test_list


if __name__ == '__main__':
    robot_list = RobotList(command)
    print(robot_list.list_robot_tests())
