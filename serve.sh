#!/bin/sh
echo "Remember to run with nohup."
bin/flask --app server.py run --host=0.0.0.0
