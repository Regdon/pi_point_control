# Setup Autostart

## Script to create an executable on the PI to start the venv and run the server:
nano server_start.sh
    #!/bin/bash
    cd /home/pi/code/pi_point_control
    source venv/bin/activate
    python server.py

Save CTRL + O, Enter
Close CTRL + X

Make executable:
chmod +x server_start.sh

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

## Configuration validation and tests

Node, route, and toggle configuration is validated during startup. Invalid
node types, duplicate IDs, missing references, unsupported point states, and
malformed button settings raise a `ConfigurationError` with the relevant
configuration item identified.

Toggle buttons are configured in `data/toggle_data.json`. Each toggle defines
its button position and colour scheme, a `default_state`, point IDs, route IDs
with their active colours, and node IDs with their active colours. Toggles
start off: their points are set to `default_state` and locked. Clicking a toggle
sets and locks those points to the opposite state while applying its route and
node colours; clicking again restores the off state and normal colours.

Run the test suite from the repository root with:

```sh
python -m unittest discover -s tests
```