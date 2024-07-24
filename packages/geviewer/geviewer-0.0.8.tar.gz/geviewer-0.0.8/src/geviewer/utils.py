import sys
import asyncio


def read_file(filename):
    '''
    Read the content of the file.
    '''
    print('Reading mesh data from ' + filename + '...')
    with open(filename, 'r') as f:
        data = f.read()
    return data


def clear_input_buffer():
    '''
    Clear the input buffer to avoid stray keystrokes influencing
    later inputs.
    '''
    try:
        # if on Unix
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except ImportError:
        # if on Windows
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()


async def prompt_for_camera_view():
    '''
    Asyncronously get camera view input from the terminal.
    '''
    print('Setting the camera position and orientation.')
    print('Press enter to skip any of the following prompts.')
    print('If the camera view is overdefined, later inputs will override earlier ones.')
    clear_input_buffer()
    while(True):
        try:
            fov = await asyncio.to_thread(input, 'Enter the field of view in degrees: ')
            if fov == '':
                fov = None
                break
            fov = float(fov)
            break
        except ValueError:
            print('Error: invalid input. Please enter a number.')
    while(True):
        try:
            position = await asyncio.to_thread(input, 'Enter the position as three space-separated numbers: ')
            if position == '':
                position = None
                break
            position = list(map(float, position.split()))
            if len(position) != 3:
                raise ValueError
            break
        except ValueError:
            print('Error: invalid input. Please enter three numbers separated by spaces.')
    while(True):
        try:
            up = await asyncio.to_thread(input, 'Enter the up vector as three space-separated numbers: ')
            if up == '':
                up = None
                break
            up = list(map(float, up.split()))
            if len(up) != 3:
                raise ValueError
            break
        except ValueError:
            print('Error: invalid input. Please enter three numbers separated by spaces.')
    while(True):
        try:
            zoom = await asyncio.to_thread(input, 'Enter the zoom factor: ')
            if zoom == '':
                zoom = None
                break
            zoom = float(zoom)
            break
        except ValueError:
            print('Error: invalid input. Please enter a number.')
    while(True):
        try:
            elev = await asyncio.to_thread(input, 'Enter the elevation in degrees: ')
            if elev == '':
                elev = None
                break
            elev = float(elev)
            break
        except ValueError:
            print('Error: invalid input. Please enter a number.')
    while(True):
        try:
            azim = await asyncio.to_thread(input, 'Enter the azimuth in degrees: ')
            if azim == '':
                azim = None
                break
            azim = float(azim)
            break
        except ValueError:
            print('Error: invalid input. Please enter a number.')
    return fov, position, up, zoom, elev, azim


async def prompt_for_file_path(*args):
    '''
    Asynchronously get file path input from the terminal.
    '''
    print('Enter the file path to save the ' + args[0])
    clear_input_buffer()
    file_path = await asyncio.to_thread(input,'  (e.g., /path/to/your_file.' + args[1] + '): ')
    return file_path


async def prompt_for_window_size():
    '''
    Asynchronously get window size input from the terminal.
    '''
    clear_input_buffer()
    while(True):
        try:
            width = await asyncio.to_thread(input, 'Enter the window width in pixels: ')
            width = int(width)
            break
        except ValueError:
            print('Error: invalid input. Please enter an integer.')
    while(True):
        try:
            height = await asyncio.to_thread(input, 'Enter the window height in pixels: ')
            height = int(height)
            break
        except ValueError:
            print('Error: invalid input. Please enter an integer.')
    return width, height