# this was initially gonna send inputs directly to the Roblox process but that turned out to be infeasible with
# the anticheat so it just only performs inputs when the window is focused

import ctypes
import pydirectinput
from ctypes import wintypes
from win32gui import GetForegroundWindow


def _check_zero(result, func, args):
    if not result:
        err = ctypes.get_last_error()
        if err:
            pass
            # raise ctypes.WinError(err)  the script throws a lot of these so i had to silence it
    return args


class RobloxInterface:
    def __init__(self, window_name="Roblox"):  # this whole function is just getting the window
        user32 = ctypes.WinDLL('user32', use_last_error=True)

        if not hasattr(wintypes, 'LPDWORD'):  # PY2
            wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

        WNDENUMPROC = ctypes.WINFUNCTYPE(
            wintypes.BOOL,
            wintypes.HWND,  # _In_ hWnd
            wintypes.LPARAM, )  # _In_ lParam

        user32.EnumWindows.errcheck = _check_zero
        user32.EnumWindows.argtypes = (
            WNDENUMPROC,  # _In_ lpEnumFunc
            wintypes.LPARAM,)  # _In_ lParam

        user32.IsWindowVisible.argtypes = (
            wintypes.HWND,)  # _In_ hWnd

        user32.GetWindowThreadProcessId.restype = wintypes.DWORD
        user32.GetWindowThreadProcessId.argtypes = (
            wintypes.HWND,  # _In_      hWnd
            wintypes.LPDWORD,)  # _Out_opt_ lpdwProcessId

        user32.GetWindowTextLengthW.errcheck = _check_zero
        user32.GetWindowTextLengthW.argtypes = (
            wintypes.HWND,)  # _In_ hWnd

        user32.GetWindowTextW.errcheck = _check_zero
        user32.GetWindowTextW.argtypes = (
            wintypes.HWND,  # _In_  hWnd
            wintypes.LPWSTR,  # _Out_ lpString
            ctypes.c_int,)  # _In_  nMaxCount

        self.roblox_window = None

        @WNDENUMPROC
        def _enum_proc(hWnd, lParam):
            if user32.IsWindowVisible(hWnd):
                pid = wintypes.DWORD()
                tid = user32.GetWindowThreadProcessId(
                    hWnd, ctypes.byref(pid))
                length = user32.GetWindowTextLengthW(hWnd) + 1
                title = ctypes.create_unicode_buffer(length)
                user32.GetWindowTextW(hWnd, title, length)
                if title.value == window_name:
                    self.roblox_window = hWnd
            return True

        user32.EnumWindows(_enum_proc, 0)

        if not self.roblox_window:
            raise Exception("Roblox application not found.")

    def press(self, key):
        if GetForegroundWindow() == self.roblox_window:
            pydirectinput.keyDown(key)

    def release(self, key):
        if GetForegroundWindow() == self.roblox_window:
            pydirectinput.keyUp(key)

    def click(self, x, y):
        if GetForegroundWindow() == self.roblox_window:
            pydirectinput.click(x, y)
