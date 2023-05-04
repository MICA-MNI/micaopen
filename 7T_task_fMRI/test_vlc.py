from rs_dependencies import *
import subprocess
import time

currentDir = os.getcwd()
path = os.path.normpath(currentDir)
path = path.split(os.sep)

if path[2] == 'neichert':
    clipDir_6min = currentDir + '/videos/6min_clips/'
    clipDir_3min = currentDir + '/videos/3min_clips/'
    VLCBIN = '/Applications/VLC.app/Contents/MacOS/VLC'
elif path[2] == 'percy':
    clipDir_6min = '/data/mica3/7T_task_fMRI/7T_task_fMRI/videos/6min_clips/'
    clipDir_3min = '/data/mica3/7T_task_fMRI/7T_task_fMRI/videos/3min_clips/'
    VLCBIN = '/usr/bin/vlc'
elif path[2] == 'mica3':
    clipDir_6min = '/data/mica3/7T_task_fMRI/7T_task_fMRI/videos/6min_clips/'
    clipDir_3min = '/data/mica3/7T_task_fMRI/7T_task_fMRI/videos/3min_clips/'
    VLCBIN = '/usr/bin/vlc'
else:
    clipDir_6min = currentDir + '/videos/6min_clips/'
    clipDir_3min = currentDir + '/videos/3min_clips/'
    print('vlcbin not defined')
    sys.exit()

t_clip = 10
clip = clipDir_3min + 'suspense_kirsten_gets_hit.mp4'
print(f'start playing {clip}')
proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
time.sleep(t_clip)
proc.terminate()
print('vlc closed successfully.')

