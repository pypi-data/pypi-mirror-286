# robot_list
List the robot tests by taking robot flags are command as cmd line arguments </br>

Usage: </br>
python -m robot_list '--include test1 --exclude test2 tests/' </br>
python -m robot_list '-i test1 -e test2 tests/' </br>
python -m robot_list '--suite suite1 --test test1 tests/'  </br>
python -m robot_list '-s suite1 -t test1 tests/' </br>
python -m robot_list '--include test1 --exclude test2 --suite suite1 tests/' </br>
python -m robot_list '-i test1 -e test2 -s suite1 tests/' </br>
 </br>
or </br> </br>

robot_list = RobotList(command) </br>
robot_list.list_robot_tests() </br>
