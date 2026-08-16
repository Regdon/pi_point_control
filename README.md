# Setup Autostart

## Script to create an executable on the PI to start the venv and run the server:
nano server_start.sh
    #!/bin/bash
    cd /home/pi/code/pi_point_control/testing_flask
    source venv/bin/activate
    cd /home/pi/code/pi_point_control
    python3 server.py

Save CTRL + O, Enter
Close CTRL + X

Make executable:
chmod +x start_server.sh

## Script to manage the autostart on PI:
sudo nano /etc/systemd/system/pi_point.service
    [Unit]
    Description=Pi Point Control Server
    After=network.target

    [Service]
    ExecStart=/home/pi/code/pi_point_control/start_server.sh
    WorkingDirectory=/home/pi/code/pi_point_control
    Restart=always
    User=pi

    [Install]
    WantedBy=multi-user.target

## Enable and start:
sudo systemctl daemon-reload
sudo systemctl enable pi_point.service
sudo systemctl start pi_point.service

## Verify and see errors:
sudo systemctl status pi_point.service
journalctl -u pi_point.service -f