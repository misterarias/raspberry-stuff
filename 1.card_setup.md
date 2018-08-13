# Custom Raspbian image

```
IMG_NAME=raspbian.img

# GEt raspbian lite
wget -O raspbian.gz https://downloads.raspberrypi.org/raspbian_lite_latest
unzip raspbian.gz && mv *-raspbian*.img $IMG_NAME

# Mount it locally - using moount
START=$(fdisk -l $IMG_NAME | grep "${IMG_NAME}2" | awk '{print $2}')
sudo mkdir /mnt/raspbian
sudo mount -o loop,offset=$(echo 512*${START} | bc) raspbian.img /mnt/raspbian

# or using loop devices
DEVICE=$(sudo losetup --find --partscan --show raspbian.img)

lsblk $DEVICE
sudo mount ${DEVICE}p2 -o rw /mnt/raspbian

# Install QEMU and copy it inside
sudo apt install -y binfmt-support qemu qemu-user-static
sudo cp $(which qemu-arm-static) /mnt/raspbian/usr/bin/

# check
sudo chroot /mnt/raspbian bin/bash
$ uname -a
$ raspi-config # enable ssh
$ echo "bebepi" > /etc/hostname
$ ENCRYPTED_PASS=$(wpa_passphrase "SSID "PASSWORD")
$ cat >> /etc/wpa_supplicant/wpa_supplicant.conf << EOF
network {
  ssid="SSID"
  psk="${ENCRYPTED_PASS}
  ssid_scan=1
  key_mgmt=WPA-PSK
}
EOF
$ exit

# after editing stuff
sudo umount /mnt/raspbian
sudo losetup -d ${DEVICE}

# Burn the image (be careful with the of path)
sudo umount /dev/sde1
sudo umount /dev/sde2
sudo dd if=$(pwd)/${IMG_NAME} of=/dev/sde status=progress bs=4M

# Connect the SD to the raspberry, plug a cable, and ssh
ssh pi@raspberrypi.local

```
