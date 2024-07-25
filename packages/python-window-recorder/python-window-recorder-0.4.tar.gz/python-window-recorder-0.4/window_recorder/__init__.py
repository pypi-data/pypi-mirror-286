
import time, os
import cv2
from threading import Thread
import ctypes
import win32gui
from window_recorder.capture.d3dcapture import CaptureSession

class Recorder():
    def __init__(recorder, window_title, timeout=120):
        recorder.hwnd = recorder.get_hwnd(window_title)
        session = CaptureSession()
        recorder.state_box = [None, False, False] # frame, changed, stop

        def frame_callback(session):
            frame = session.get_frame()
            if frame is None:
                return
            recorder.state_box[0] = frame
            recorder.state_box[1] = True
        session.frame_callback = frame_callback
        recorder.session = session
        recorder.timeout = timeout
    
    def start(recorder, folder=None, filename=None):
        # Get the current timestamp for the filename
        timestamp = time.strftime('%Y%m%d-%H%M%S')

        # Define the output filename with the timestamp
        if folder:
            if not os.path.exists(folder):
                os.makedirs(folder)

            folder_path = folder + '/'
        else:
            folder_path = ''
        if filename:
            full_filename = f'{filename}_{timestamp}.mp4'
        else:
            full_filename = timestamp + '.mp4'
        recorder.output_file_path = folder_path + full_filename
        # print('recorder.output_file_path', recorder.output_file_path)

        # Define video codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        window_rect = win32gui.GetWindowRect(recorder.hwnd)
        width, height = window_rect[2] - window_rect[0], window_rect[3] - window_rect[1]
        recorder.video_ouput = cv2.VideoWriter(recorder.output_file_path, fourcc, 50, (width, height))

        # Check if the VideoWriter object is opened successfully
        if not recorder.video_ouput.isOpened():
            raise Exception('Failed to open the video writer')
        
        # Start window capture
        hwnd = recorder.hwnd
        recorder.session.start(hwnd, False)

        recorder.stop_flag = False
        recorder.timeout_at = time.time() + recorder.timeout
        def start_recorder(recorder):
            while not recorder.stop_flag:
                if recorder.state_box[1]:
                    recorder.state_box[1] = False
                    img = recorder.state_box[0]
                    recorder.video_ouput.write(img)
                if time.time() >= recorder.timeout_at:
                    recorder.video_ouput.release()
                    recorder.session.stop()
                    print(f'Video saved as {recorder.output_file_path} after timing out')
                    break

        recorder.thread = Thread(target=start_recorder, args=(recorder,), daemon=True) # Daemon otherwise won't be able to exit with Ctrl+C
        recorder.thread.start()
    
    def stop(recorder):
        recorder.stop_flag = True
        recorder.thread.join()

        recorder.video_ouput.release()
        recorder.session.stop()
        print(f'Video saved as {recorder.output_file_path}')
        return recorder.output_file_path
    
    def get_hwnd(recorder, window_title):
        # Get window handle with partial match
        
        def callback(hwnd, hwnds):
            hwnds.append(hwnd)
            return True
            
        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        for current_hwnd in hwnds:
            current_window_title = win32gui.GetWindowText(current_hwnd)
            if window_title.lower() in current_window_title.lower():
                return current_hwnd
        
        raise Exception(f'Window title "{window_title}" not found')