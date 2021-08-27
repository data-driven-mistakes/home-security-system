
import pygame.camera

pygame.camera.init()
cams = (pygame.camera.list_cameras()) #Camera detected or not
print(cams, len(cams))

for ii in range(int(len(cams)/2)):
    cam = pygame.camera.Camera("/dev/video"+str(2*ii),(640,480))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,"filename"+str(ii) +".jpg")
