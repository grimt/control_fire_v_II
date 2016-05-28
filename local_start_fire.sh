 #!/bin/bash
echo starting scripts

sudo python /home/pi/code/python_code/new_heat_home/local_remote_read_measured_temperature.py &
sleep 1
sudo python /home/pi/code/python_code/new_heat_home/local_read_remote_control.py &
sleep 1
sudo python /home/pi/code/python_code/new_heat_home/local_accept_temperature_from_remote.py &
sleep 1
sudo python /home/pi/code/python_code/new_heat_home/local_control_fire.py &

echo scripts started
