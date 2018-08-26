# Raspbery as a webcam server

```
ssh pi@$RASPBERRY_IP
sudo apt-get update
sudo apt-get install -y motion

# Directory to save photos and streams
mkdir /home/pi/Monitor
sudo chgrp motion /home/pi/Monitor
chmod g+rwx /home/pi/Monitor

sudo vim /etc/motion/motion.conf
# daemon on
# stream_localhost off
# target_dir /home/pi/Monitor
# v4ld2_pallete 15 # ??
# width 640
# height 480
# framerate 10

sudo vim /etc/default/motion
# start_motion_daemon yes

# Enable via systemd
sudo cat > /lib/systemd/system/motion.service  << EOF
[Unit]
Description=Motion - WebCam control
After=multi-user.target

[Service]
#KillMode=process
#Restart=on-failure
#RestartPreventExitStatus=255
ExecStart=/usr/bin/motion
Type=idle

[Install]
WantedBy=multi-user.target
Alias=motion.service
EOF

sudo systemctl daemon-reload
sudo systemctl enable motion.service
```
