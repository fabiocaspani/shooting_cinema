import datetime
import win32api
import win32gui
import win32ui
import win32con
import numpy as np
import cv2

def prepareScreenshot():
    # Get the dimensions of the primary display
    width_screen = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height_screen = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    # Create a device context (DC) object for the full-screen window
    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    dc = win32ui.CreateDCFromHandle(desktop_dc)

    # Create a memory DC object for the screenshot
    mem_dc = dc.CreateCompatibleDC()

    # Create a bitmap object for the screenshot
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(dc, width_screen, height_screen)
    mem_dc.SelectObject(screenshot)
    return screenshot, mem_dc, dc, width_screen, height_screen

def takeScreenshot(mem_dc, dc, width_screen, height_screen):
    mem_dc.BitBlt((0, 0), (width_screen, height_screen), dc, (0, 0), win32con.SRCCOPY)
    print(datetime.datetime.now())


def convertScreenshot(screenshot):
    bmpinfo = screenshot.GetInfo()
    img = np.frombuffer(screenshot.GetBitmapBits(True), dtype='uint8')
    img.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)
    return img

def clearScreenshotMemory(mem_dc, screenshot):
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())


def showScreenshot():
    screenshot, mem_dc, dc, width_screen, height_screen = prepareScreenshot()
    print(width_screen)
    print(height_screen)
    takeScreenshot(mem_dc, dc, width_screen, height_screen)
    image = convertScreenshot(screenshot)
    cv2.imshow("Test", image)
    clearScreenshotMemory(mem_dc, screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
