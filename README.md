# skinning2morph
For Blender

### (1)
Install Skinning2Morph.py
<img width="674" alt="image" src="https://user-images.githubusercontent.com/46149216/176428845-3a9a8e81-7c26-4dcf-a92e-0adaa02bb2b3.png">

### (2)
Strip the target animation and create NLATrack.
For NLATrack, enter an animation name such as walk/idle.
This name is used as "animName" on the module side.

<img width="1484" alt="image" src="https://user-images.githubusercontent.com/46149216/176429079-5fb0a2da-6338-4af8-9402-3ceefa550539.png">

### (3)
With the target object selected, specify the number of frames and press "convert2morph".
<img width="561" alt="image" src="https://user-images.githubusercontent.com/46149216/176429194-86a9a9e4-805d-4cc2-8acf-d4e239d72804.png">

### (4)
Maintain the transform, clear the relationship with Armature, delete Armature, and you're done!
<img width="796" alt="image" src="https://user-images.githubusercontent.com/46149216/176429580-af8a32c8-ecd2-4fca-8d20-1771ec9f788d.png">

### (5)
Verify that the morphing is successful.

Open Gltf-viewer, drag and drop the 3D model, and if the animation plays, you have succeeded.

https://gltf-viewer.donmccurdy.com/

![スクリーンショット 2022-09-13 21 29 23](https://user-images.githubusercontent.com/46149216/189901389-cb83f4dd-909d-42dd-8308-6457476fc15a.png)
