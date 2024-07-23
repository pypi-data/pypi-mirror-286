# robot_list </br>
Do you want to list the testcases of a suite in robot framework before start execution? </br>
Here, is the solution for this. This package will perform the dry run on the command line which user is given and list all the tests. </br>
**Venixa Robot-List** </br>
List the robot tests by taking robot flags as cmd line arguments </br>

Usage: </br>
python -m robot_list.robot_list '--include test1 --exclude test2 tests/' </br>
python -m robot_list.robot_list '-i test1 -e test2 tests/' </br>
python -m robot_list.robot_list '--suite suite1 --test test1 tests/'  </br>
python -m robot_list.robot_list '-s suite1 -t test1* tests/' </br>
python -m robot_list.robot_list '--include test1 --exclude test2 --suite suite1 tests/' </br>
python -m robot_list.robot_list '-i test1 -e test2 -s suite1* tests/' </br>
 </br>
or </br> </br>

from robot_list import robot_list
robot_list = robot_list.RobotList(command) </br>
test_list = robot_list.list_robot_tests() </br>

