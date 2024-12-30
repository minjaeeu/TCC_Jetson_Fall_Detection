# TCC_Jetson_Fall_Detection

This is a project that aims to detect if a person has fallen using Jetson Inference's poseNet. 
Upon a fall detection, an alert containing the last captured frame is sent via e-mail and Telegram.

In a gist, fall detection rules are: 1° if the absolute distance from shoulder-waist or ankle-waist is lower than a set threshold && 2° if the width/height outline proportion is greater than 1.

This project was built & deployed to a Jetson Nano 2GB. 

Dependencies are: Python 3.6.9, Jetson Inference (c038530, as Oct 16th 2024) and requests 2.32.3.

This project was created as part of the final paper for my graduation course. Hope this helps anyone in need (specially for those trying to do something with a Jetson Nano 2GB alongside Jetson Inference)