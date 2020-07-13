#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:59:38 2017

@author: reinder
"""
from psychopy import visual, core, event

screenRes = [1024,768]
isFullScreen=True
screenToShow=0
fontSize=62
escapeKeys = ['q','escape']

#create window and stimuli
win = visual.Window(screenRes, fullscr=isFullScreen, allowGUI=False, monitor='testMonitor', screen=screenToShow, units='pix', name='win', color=[0.700,0.700,0.700])
#fixation = visual.GratingStim(win, color='black', tex=None, mask='circle',size=0.2)
#fixation = visual.ShapeStim(win,lineColor='#000000',lineWidth=3.0,vertices=((-fixCrossSize/2,0),(fixCrossSize/2,0),(0,0),(0,fixCrossSize/2),(0,-fixCrossSize/2)),units='pix',closeShape=False);
fixation = visual.TextStim(win, name='fixation', text='+', height=fontSize, pos=(0,0),color='black')#set pix pos
fixation.draw()
win.flip()

keyPress = event.waitKeys(keyList=escapeKeys)
if keyPress[0] in escapeKeys:
    win.close()
    core.quit()