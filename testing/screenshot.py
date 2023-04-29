import datetime
import win32api
import win32gui
import win32ui
import win32con

def screenshot(filename):
    print(datetime.datetime.now())
    # Get the dimensions of the primary display
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    # Create a device context (DC) object for the full-screen window
    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    dc = win32ui.CreateDCFromHandle(desktop_dc)

    # Create a memory DC object for the screenshot
    mem_dc = dc.CreateCompatibleDC()

    # Create a bitmap object for the screenshot
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(dc, width, height)
    mem_dc.SelectObject(screenshot)

    # Copy the screen contents to the memory DC
    mem_dc.BitBlt((0, 0), (width, height), dc, (0, 0), win32con.SRCCOPY)
    print(datetime.datetime.now())

    # Save the bitmap to a file
    screenshot.SaveBitmapFile(mem_dc, filename)

    # Free up memory
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

# Call the screenshot function to take a screenshot and save it to a file
screenshot('screenshot.bmp')