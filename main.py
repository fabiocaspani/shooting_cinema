import print_screen, camera, image_projection

camera.adjustTarget()
screenshot, mem_dc, dc, width_screen, height_screen = print_screen.prepareScreenshot()
cameraShot = camera.cameraShot()

print_screen.takeScreenshot(mem_dc, dc, width_screen, height_screen)
screenShot = print_screen.convertScreenshot(screenshot)
print_screen.clearScreenshotMemory(mem_dc, screenshot)

x, y = image_projection.projectCenter(cameraShot, screenShot)

image_projection.printResult(screenShot, x, y)

image_projection.cleanup()

