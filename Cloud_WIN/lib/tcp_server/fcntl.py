import os
import win32con
import pywintypes
import win32file

LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
LOCK_SH = 0  # The default value
LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY


__overlapped = pywintypes.OVERLAPPED()

def flock(file, flags):
    if (type(file).__name__ == 'int'):
        f_fileno = file
    else:
        f_fileno = file.fileno(f_fileno)
    hfile = win32file._get_osfhandle(f_fileno)
    win32file.LockFileEx(hfile, flags, 0, 0xffff0000, __overlapped)
def funlock(file):
    if (type(file).__name__ == 'int'):
        f_fileno = file
    else:
        f_fileno = file.fileno()
    hfile = win32file._get_osfhandle(f_fileno)
    win32file.UnlockFileEx(hfile, 0, 0xffff0000, __overlapped)
