#!/bin/bash
echo starting scripts

sudo python ./local_remote_read_measured_temperature.py &
sleep 1
sudo python ./remote_read_desired_temperature_buttons.py  &
sleep 1
sudo python ./remote_accept_temperature_from_local.py &
sleep 1
sudo python ./remote_send_temperature_to_local.py &

echo scripts started
