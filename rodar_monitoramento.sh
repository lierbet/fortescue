#!/bin/bash
cd /opt/monitoramento_mme
/root/myenv/bin/python monitor.py >> /opt/monitoramento_mme/cron.log 2>&1
