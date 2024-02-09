# 3d-printing
- [3d-printing](#3d-printing)
  - [Overall Setup (Raspberry Pi)](#overall-setup-raspberry-pi)
  - [Camera](#camera)
    - [Start (CLI)](#start-cli)
    - [Start (PM2)](#start-pm2)

## Overall Setup (Raspberry Pi)

Install PM2:
```
sudo npm install pm2 -g
pm2 startup
```

## Camera

### Start (CLI)
```
python3 rpi-serve-camera/rpi_serve_camera.py
```

### Start (PM2)
Start the Python process permanently (so that it starts even after reboot):
```
pm2 start rpi-serve-camera/rpi_serve_camera.py
pm2 save
```


