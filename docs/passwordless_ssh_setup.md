# SSH without password


```
# First, generate new pair of keys locally
ssh-keygen -b 2048 -f ~/.ssh/raspberry

# Copy them to the raspberry using ssh
ssh-copy-id -i ~/.ssh/raspberry.pub pi@bebepi

# Profit!!
```
