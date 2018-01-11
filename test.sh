#!/bin/bash

URL="localhost:5000"

curl -XPOST "${URL}/121/job1/start"
curl -XPOST "${URL}/121/job2/start"
sleep 1
curl -XPOST "${URL}/121/job1/stop"
curl -XPOST "${URL}/121/job2/stop"

curl -XPOST "${URL}/121/job3/start"
curl -XPOST "${URL}/121/job4/start"
sleep 1
#curl -XPOST "${URL}/121/job3/stop"
#curl -XPOST "${URL}/121/job4/stop"

curl -XPOST "${URL}/123/jobby/start"
sleep 1
curl -XPOST "${URL}/123/jobby/stop"

curl -XPOST "${URL}/124/jobby/start"
sleep 1
curl -XPOST "${URL}/124/jobby/stop"

curl -XDELETE "${URL}/123"

echo 'Test cases can be viewed at http://${URL}/'
