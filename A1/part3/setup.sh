#!/bin/bash
sudo apt-get install rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server

sudo rabbitmqctl add_user myuser mypassword
rabbitmqctl set_permissions -p / myuser ".*" ".*" ".*"