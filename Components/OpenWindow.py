import pygetwindow as gw


def open():
    windows = gw.getWindowsWithTitle('BlueStacks')
    if windows:
        bluestacks_window = windows[0]
        bluestacks_window.activate()
        bluestacks_window.maximize()
    return True


def open_bluestacks_window():
    resp = open()
    return resp
