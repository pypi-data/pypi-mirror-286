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
python -m robot_list '--include test1 --exclude test2 tests/'
python -m robot_list '-i test1 -e test2 tests/'
python -m robot_list '--suite suite1 --test test1 tests/'
python -m robot_list '-s suite1 -t test1 tests/'
python -m robot_list '--include test1 --exclude test2 --suite suite1 tests/'
python -m robot_list '-i test1 -e test2 -s suite1 tests/'

or

robot_list = RobotList(command)
robot_list.list_robot_tests()
"""



class RobotList:
    """This class helps to list the robot tests with given robot parameters"""

    _REGEX_PATTERN_FILTER = (r'--include [^.*]+|-i [^.*]+|--exclude ['
                             r'^.*]+|-e [^.*]+|--suite [^.*]+|-s ['
                             r'^.*]+|-t [^.*]+|--test [^.*]+')

    _REGEX_PATTERN_SRC = r'(\s[^.*])$'

    def __init__(self, cmd):
        """This function initializes the robot parameters"""
        self.command = cmd
        self.__temp_dir_name = tempfile.TemporaryDirectory().name
        self.__xml_file_output = os.path.join(self.__temp_dir_name,
                                              'xunit.xml')

    def robot_command(self, robot_cmd_flags, src_directory):
        """This function forms the robot command with given flags

        @param robot_cmd_flags: list of robot command flags
        @param src_directory: source directory
        """

        return (f'python -m robot --dryrun -x {self.__xml_file_output} -d '
                f'{self.__temp_dir_name}'
                f' {" ".join(robot_cmd_flags)} {src_directory}').strip()

    def parse_robot_command(self):
        """This function parses the robot command"""
        flags = re.findall(self._REGEX_PATTERN_FILTER, self.command)
        src_matches = re.findall(self._REGEX_PATTERN_SRC, self.command)
        return self.robot_command(flags, (src_matches[-1] if src_matches
                                          else''))

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
                        status_dict = {
                            'name': test['name']
                        }
                        executed_testcases.append(status_dict)
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
            print(str(e))
        return executed_testcases

    def __delete_log_files(self):
        """Delete the log files if exists"""
        try:
            shutil.rmtree(self.__temp_dir_name, ignore_errors=True)
        except Exception as e:
            pass

    def list_robot_tests(self):
        """This function lists the robot tests with given robot parameters"""
        tests = []
        try:
            rcmd = self.parse_robot_command()
            subprocess.check_output(rcmd, shell=True, stderr=subprocess.PIPE)
        except Exception as e:
            pass
        tests = self.__executed_tests(self.__xml_file_output)
        self.__delete_log_files()
        return tests


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception(help_doc)

    command = sys.argv[-1]
    robot_list = RobotList(command)
    print(robot_list.list_robot_tests())
