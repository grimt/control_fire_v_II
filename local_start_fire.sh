 #!/bin/bash
echo starting scripts

sudo python ./local_remote_read_measured_temperature.py &
sleep 1
sudo python ./local_read_remote_control.py &
sleep 1
sudo python ./local_accept_temperature_from_remote.py &
sleep 1
sudo python ./local_control_fire.py &

echo scripts started
