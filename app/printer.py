import win32print
import win32gui
import win32ui
import win32con
import pywintypes
from typing import Optional, Tuple, TYPE_CHECKING
from PIL import Image, ImageWin

if TYPE_CHECKING:
    from _win32typing import PyDEVMODEW

def get_printer_info(printer_name: Optional[str] = None) -> Tuple[str, str, "PyDEVMODEW"]:
    printer_name = printer_name if printer_name is not None else win32print.GetDefaultPrinter()
    PRINTER_DEFAULTS = {
        "DesiredAccess":win32print.PRINTER_ALL_ACCESS
    }
    handle = win32print.OpenPrinter(printer_name, PRINTER_DEFAULTS)
    level = 2
    

    attributes = win32print.GetPrinter(handle, level)
    driver_name = attributes["pDriverName"]
    
    dev_mode = pywintypes.DEVMODEType(attributes['pDevMode'].DriverExtra)

    win32print.DocumentProperties(
        0,
        handle,
        attributes["pDriverName"],
        dev_mode,
        attributes['pDevMode'],
        win32con.DM_OUT_BUFFER
    )
    win32print.ClosePrinter(handle)

    return printer_name, driver_name, dev_mode

def get_printer_height(printer_name: Optional[str] = None):
    printer_name, driver_name, dev_mode = get_printer_info(printer_name)
    hDC = win32gui.CreateDC(
        driver_name,
        printer_name,
        dev_mode
    )
    height = win32ui.GetDeviceCaps(hDC, win32con.VERTRES)
    win32gui.DeleteDC(hDC)
    return height


def print(image: Image.Image, printer_name: Optional[str] = None):
    
    printer_name, driver_name, dev_mode = get_printer_info(printer_name)

    hDC = win32gui.CreateDC(
        driver_name,
        printer_name,
        dev_mode
    )

    width = win32ui.GetDeviceCaps(hDC, win32con.HORZRES)
    height = win32ui.GetDeviceCaps(hDC, win32con.VERTRES)
    win32gui.DeleteDC(hDC)
    
    while True:
        hDC = win32gui.CreateDC(
            driver_name,
            printer_name,
            dev_mode
        )
        width = win32ui.GetDeviceCaps(hDC, win32con.HORZRES)
        height = win32ui.GetDeviceCaps(hDC, win32con.VERTRES)
        if width < image.size[0]:
            win32gui.DeleteDC(hDC)
            dev_mode.PaperLength += 50
            continue
        win32print.StartDoc(hDC, ("document_ptouch_proxy", None, None, 0))
        win32print.StartPage(hDC)
        dib = ImageWin.Dib(image)
        dib.draw(hDC, (0, 0, image.size[0], height))
        win32print.EndPage(hDC)
        win32print.EndDoc(hDC)
        win32gui.DeleteDC(hDC)
        break
