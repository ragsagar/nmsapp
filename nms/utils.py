import subprocess

def is_nms_running():
    """ Check if the LinuxNMS command is running or not.
    Returns True if nms is running."""
    command = ['/bin/ps', '-C', 'LinuxNMS']
    returncode = subprocess.call(command)
    if returncode == 0:
        return True
    else:
        return False


def start_nms():
    """ Command to start LinuxNMS. Returns True if nms is started."""
    command = ['sudo', '/etc/init.d/LinuxNMS', 'start']
    returncode = subprocess.call(command)
    if returncode == 0:
        return True
    else:
        return False


def stop_nms():
    """ Command to stop LinuxNMS. Return True if nms is stopped."""
    command = ['sudo', '/etc/init.d/LinuxNMS', 'stop']
    returncode = subprocess.call(command)
    if returncode == 0:
        return True
    else:
        return False
