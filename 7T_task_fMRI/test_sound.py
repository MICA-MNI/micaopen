from task_dependencies import *

# load stuff
ab1_fpath = 'audiobook/stimuli_DownTheRabbitHoleFinal_mono_exp120_NR16_pad.wav'
ab1_sound_data, ab1_fs = sf.read(ab1_fpath, dtype='float32')
t_exclude = 17
t_play = 360
data_cropped = ab1_sound_data[t_exclude * ab1_fs:(t_exclude + t_play) * ab1_fs]

# start window
win = visual.Window(fullscr=False, color=1, units='height')
win.flip()
fixation = visual.TextStim(win=win, text="+", height=float(.08), color='black')
fixation.draw()
win.update()

# play sound until escape
sd.play(data_cropped, ab1_fs)
time_start = clock.getTime()
while (clock.getTime() - time_start) < t_play:
    core.wait(5)
    print('wait')
    keys_list = event.getKeys()
    if any("escape" in key for key in keys_list):
        print('escaped')
        sd.stop()
        win.close()
        core.quit()

print('finished')
sd.stop()
win.close()
core.quit()
