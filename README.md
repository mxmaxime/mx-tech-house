[![Netlify Status](https://api.netlify.com/api/v1/badges/23f1a86a-e928-4c19-8139-959c1d307199/deploy-status)](https://app.netlify.com/sites/peaceful-leakey-b90c22/deploys)

## Motivations
At the beginning, I wanted to secure my house. Basically, around my house there have been a lot of burglaries.
On the market to day, we can find a lot of security cameras, supposed to be intelligent and so one. But I have one concern: my privacy. I've analyzed some security camera and I found some real bad things. So I have decided to create everything myself. Sure a lot of open-source software exists, but... I don't want to be rude, but they are really bad designed.

This project is build from the ground up for simplicity, for developers and users, and also privacy first.

## Status
This software is currently under development and we are discovering some bugs day to day. It is currently deployed in one House to test it in the real world,  gather some data, and improve the overall!

### Smart camera
- [x] Work with a PiCamera or USB camera on any hardware.
- [x] Detect human to notify.
  - [x] Send picture to the main system.
 - [x] Define ROIs (Region of interest) and use it to know whether the human is in a ROI or not.
  - [ ] Attatch status to ROI. Basically one ROI can be in security mode and another one can be in watch only mode.
- [ ] Nocturne vision to detect human even when we don't have any light.

### Dumb camera
Nothing has been done yet and no plan for now because I have to finish the smart camera before to unlock some features that the system will use for dumb camera.

### Alarm
- [x] Schedule when to turn on or off the alarm.
- [x] Manage device by device, meaning that I can turn on a alarm device while some others are off.
- [ ] Monitore if someone is detected to notify the end user without triggering the alarm system.
