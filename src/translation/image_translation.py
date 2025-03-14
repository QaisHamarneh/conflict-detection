import pyglet
import Quartz.CoreGraphics as CG
import subprocess
import re
import sys
import ctypes
from ctypes import wintypes

from src.translation.data_constants import *

def _screen_size():
    """
    Get the maximum possible screen resolution so that the pyglet game window is properly set.
    """

    if (sys.platform == MAC_OS):
        return _screen_size_mac()
    elif (sys.platform == LINUX):
        return _screen_size_linux()
    else:
        _screen_size_windows()

def _screen_size_mac():
    screen_width = 0
    screen_height = 0

    display_id = CG.CGMainDisplayID()

    modes = CG.CGDisplayCopyAllDisplayModes(display_id, None)
    
    for mode in modes:
        width = CG.CGDisplayModeGetWidth(mode)
        height = CG.CGDisplayModeGetHeight(mode)
        screen_width = max(screen_width, width)
        screen_height = max(screen_height, height)
    
    return screen_width, screen_height

def _screen_size_linux():
    """
    Created with Chat-GPT - could not be working.
    """
    try:
        # Run xrandr command and capture the output
        output = subprocess.check_output("xrandr | grep '*'", shell=True).decode()
        resolutions = re.findall(r'(\d+)x(\d+)', output)

        # Find the maximum resolution
        screen_width, screen_height = 0, 0
        for res in resolutions:
            width, height = map(int, res)
            if width > screen_width:
                screen_width = width
            if height > screen_height:
                screen_height = height
        
        return screen_width, screen_height
    except Exception as e:
        print("Error getting resolution:", e)
        return 0, 0
    
def _screen_size_windows():
    """
    Created with Chat-GPT - could not be working.
    """
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    ENUM_REGISTRY_SETTINGS = -2

    class DEVMODE(ctypes.Structure):
        _fields_ = [
            ("dmDeviceName", ctypes.c_wchar * 32),
            ("dmSpecVersion", wintypes.WORD),
            ("dmDriverVersion", wintypes.WORD),
            ("dmSize", wintypes.WORD),
            ("dmDriverExtra", wintypes.WORD),
            ("dmFields", wintypes.DWORD),
            ("dmOrientation", wintypes.WORD),
            ("dmPaperSize", wintypes.WORD),
            ("dmPaperLength", wintypes.WORD),
            ("dmPaperWidth", wintypes.WORD),
            ("dmScale", wintypes.WORD),
            ("dmCopies", wintypes.WORD),
            ("dmDefaultSource", wintypes.WORD),
            ("dmPrintQuality", wintypes.WORD),
            ("dmColor", wintypes.WORD),
            ("dmDuplex", wintypes.WORD),
            ("dmYResolution", wintypes.WORD),
            ("dmTTOption", wintypes.WORD),
            ("dmCollate", wintypes.WORD),
            ("dmFormName", ctypes.c_wchar * 32),
            ("dmLogPixels", wintypes.WORD),
            ("dmBitsPerPel", wintypes.DWORD),
            ("dmPelsWidth", wintypes.DWORD),
            ("dmPelsHeight", wintypes.DWORD),
            ("dmDisplayFlags", wintypes.DWORD),
            ("dmDisplayFrequency", wintypes.DWORD),
            ("dmICMMethod", wintypes.DWORD),
            ("dmICMIntent", wintypes.DWORD),
            ("dmMediaType", wintypes.DWORD),
            ("dmDitherType", wintypes.DWORD),
            ("dmReserved1", wintypes.DWORD),
            ("dmReserved2", wintypes.DWORD),
            ("dmPanningWidth", wintypes.DWORD),
            ("dmPanningHeight", wintypes.DWORD),
        ]

    devmode = DEVMODE()
    devmode.dmSize = ctypes.sizeof(DEVMODE)

    if user32.EnumDisplaySettingsW(None, ENUM_REGISTRY_SETTINGS, ctypes.byref(devmode)):
        return devmode.dmPelsWidth, devmode.dmPelsHeight
    else:
        raise ctypes.WinError(ctypes.get_last_error())
    
def scale_img_size(image: pyglet.image.AbstractImage):
    scale_factor = image.width / image.height
    _, screen_height = _screen_size()
    return scale_factor * (screen_height/1.2), screen_height/1.2

def centered_x(image: pyglet.image.AbstractImage):
    width, _ = scale_img_size(image)
    display = pyglet.display.get_display()
    screen = display.get_default_screen()
    return float((screen.width/2) - (width/4))

def image_to_sprite(image: pyglet.image.AbstractImage) -> pyglet.sprite.Sprite:
    tmp_image = image
    image_sprite = pyglet.sprite.Sprite(img=tmp_image)
    width, height = scale_img_size(image)
    image_sprite.width = width
    image_sprite.height = height
    return image_sprite