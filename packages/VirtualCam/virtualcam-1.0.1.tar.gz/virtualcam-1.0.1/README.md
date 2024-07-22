# Thanks for your supporting!
### For more details, please install this project to see the description of each function.
---
#### Class *VirCam*  contains some functions about virtual camera.

 **1. *config()*** : Change the configuration of virtual camera.
 **2. *install()*** : Change the amount of virtual camera to 1. (Doesn't work if the amount is over 1) (Only for windows)
 **3. *minstall()*** : Change the amount of virtual camera to the number you entered. (Doesn't work if the amount is over the number you entered.) (Only for windows)
 **4.  *load()*** : Load a video or an image as source.
 **5. *display()*** : Run the virtual camera with specific configuration. (Must have an loaded source.)
 **6. *rgbwheel()*** : Run the virtual camera with the color wheel as source.
 **7. *rgbimg()*** : Run the virtual camera with a single-colored image as source.
 **8. *img()*** : Run the virtual camera with a image (MatLike, ndarray or other types that can convert to MatLike or ndarray directly.)

#### Class *VirCamUI* is used to run the UI. Use *run()* to run the UI.

 **1. Section *'Source'*** : Click it to load a source.
 **2. Section *'Config'*** : Edit, import or save the configuration.
 **3. Section *'Install'*** : Install a single virtual camera or multiple virtual cameras.
 **4. Section *'RGB'*** : Run the virtual camera with a color wheel or a single-colored image as source. About section *'Single Color'* which is in Section *'RGB'*, the three scale means the red/green/blue value of the image.
 **5. Main window** : Press *'Preview'* to start/stop preview. Press *'Start'* to start the virtual camera with the specific configuration and source.