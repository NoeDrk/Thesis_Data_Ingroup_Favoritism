#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 23:06:29 2024

@author: noederijck
"""
#green and blue
#clean up dots and numbers on new screen
#clean up instructions



from psychopy import visual, core, event, gui, clock
import numpy as np
import random
import pandas as pd

df = pd.read_csv('trial_data_thesis_V2.csv')

shuffled_df = df.sample(frac=1).reset_index(drop=True)

list_dots = df["number_dots"]
list_arabic = df["number_arabic"]


columns = ['group_num', 'arabic_num', 'dots_num', "participant_sharing"]
info_participant = {"Numero Groupe": 0,
                    "Participant N1": "",
                    "Participant N2": "",
                    "Participant N3": "",
                    "Participant N4": ""}
attributes = {
    'a': {'p_num': 1, 'group_affil': "VERT", 'col_text': "green"},
    'p': {'p_num': 2, 'group_affil': "VERT", 'col_text': "green"},
    'q': {'p_num': 3, 'group_affil': "ROUGE", 'col_text': "red"},
    'm': {'p_num': 4, 'group_affil': "ROUGE", 'col_text': "red"},
    '1': {'p_num': 1, 'group_affil': "VERT", 'col_text': "green"},
    '2': {'p_num': 2, 'group_affil': "VERT", 'col_text': "green"},
    '3': {'p_num': 3, 'group_affil': "ROUGE", 'col_text': "red"},
    '4': {'p_num': 4, 'group_affil': "ROUGE", 'col_text': "red"},
}

df = pd.DataFrame(columns=columns)
mean = 60

dotRadius = 0.3  # Adjust this value as needed
circleRadius = 5
num_trials = 132
participant_intervention = ['a','p','q','m'] * int(num_trials /4)
letters = ['a','p','q','m']

def create_dot_positions(n, circle_radius, dot_radius):
    positions = []
    while len(positions) < n:
        conflict = True
        while conflict:
            angle = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(dot_radius, circle_radius - dot_radius)
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            conflict = False
            for pos in positions:
                if np.sqrt((pos[0] - x)**2 + (pos[1] - y)**2) < dot_radius * 2:  
                    conflict = True
                    break
        positions.append((x, y))
    return positions

def wait_for_key_presses(trial_number, p_num, p_col):
    win.flip()
    pressed_status = {letter: False for letter in letters}
    reaction_times = {letter: None for letter in letters}
    
    def update_message():
       waiting_for = [str(letters.index(letter) + 1) for letter, pressed in pressed_status.items() if not pressed]
       return "Nous attendons les participants:\n {}".format(', '.join(waiting_for))
    
    start_time = clock.getTime()

    while not all(pressed_status.values()):
        end_time = clock.getTime()
        
        message1 = visual.TextStim(win, text=update_message(), pos=(0, 4), color="white", ori=180)
        message2 = visual.TextStim(win, text=update_message(), pos=(0, -4), color="white")

        num1 = visual.TextStim(win, text="{}".format(trial_number+1), pos=(7, 7), color="white", ori =180)
        num2 = visual.TextStim(win, text="{}".format(trial_number+1), pos=(-7, 7), color="white", ori =180)
        num3 = visual.TextStim(win, text="{}".format(trial_number+1), pos=(7, -7), color="white")
        num4 = visual.TextStim(win, text="{}".format(trial_number+1), pos=(-7, -7), color="white")
        if not isinstance(p_num, int):
            p_num = 1
        chosen = "Participant N{}".format(p_num)
        p_sharing1 = visual.TextStim(win, text="{} du group {}".format(info_participant[chosen],attributes[str(p_num)]["group_affil"]), pos=(0, 7), color=p_col, ori =180)
        p_sharing2 = visual.TextStim(win, text="{} du group {}".format(info_participant[chosen],attributes[str(p_num)]["group_affil"]), pos=(0, -7), color=p_col)
        
        p_sharing1.draw()
        p_sharing2.draw()
        num1.draw()
        num2.draw()
        num3.draw()
        num4.draw()
        message1.draw()
        message2.draw()
        win.flip()
        keys = event.waitKeys(keyList=letters)
        if keys:
            pressed_status[keys[0]] = True  # Update pressed status for the key
            reaction_times[keys[0]] =  end_time - start_time
    return reaction_times

def reference_numerosity():
    intro_ref = visual.TextStim(win, text="Vous allez voir un nuage de points composé de 45 points\n appuyez sur espace lorsque vous êtes prêts", pos=(0, 7), color="white", ori =180)
    intro_ref2 = visual.TextStim(win, text="Vous allez voir un nuage de points composé de 45 points\n appuyez sur espace lorsque vous êtes prêts", pos=(0, -7), color="white")
    end_ref = visual.TextStim(win, text="Appuyez sur espace pour continuer", pos=(0, 7), color="white", ori=180)
    end_ref2 = visual.TextStim(win, text="Appuyez sur espace pour continuer", pos=(0, -7), color="white")
    intro_ref.draw()
    intro_ref2.draw()
    win.flip()
    event.waitKeys(keyList= "space")
    dot_positions_ref = create_dot_positions(45, circleRadius, dotRadius)
    XY_cord_ref = [(x, y+1) for x, y in dot_positions_ref]
    circle = visual.Circle(win, radius=circleRadius+1 ,fillColor=None, lineColor="white", lineWidth=6, pos=(0,1)) 
    dots = visual.ElementArrayStim(win, nElements=45, xys=XY_cord_ref, elementTex=None, elementMask="circle", sizes=dotRadius)
    circle.draw()
    dots.draw()
    win.flip()
    core.wait(4)
    rts_training_ref = wait_for_key_presses(-1, "", "black")
    win.flip()
    end_ref.draw()
    end_ref2.draw()
    win.flip()
    event.waitKeys(keyList= "space")
    fixation_cross.draw()
    win.flip()
    core.wait(3)
            
win = visual.Window(size=[1920, 1080], fullscr=False, units="deg", monitor="testMonitor", color="black")

myDlg = gui.DlgFromDict(dictionary=info_participant, title="", order=[u"Numero Groupe", u"Participant N1", u"Participant N2", u"Participant N3", u"Participant N4"])

#Text stimulus
induction_intro = visual.TextStim(win=win, text= "Formulaires d'Ethique", color='white', pos=(0, 7), height=1, ori=180) 
induction_intro2 = visual.TextStim(win=win, text= "Formulaires d'Ethique", color='white', pos=(0, -7), height=1) 


welcome_message = visual.TextStim(win=win, text= "Evaluation des 10 peintures", color='white', pos=(0, 7), height=1, ori=180) 
welcome_message2 = visual.TextStim(win=win, text= "Evaluation des 10 peintures", color='white', pos=(0, -7), height=1) 

instruction_training1 = visual.TextStim(win=win, text= "Vous allez voir un nuage de points ainsi qu'un chiffre, votre but est d'estimer si le nombre de points dans le nuage est supérieur ou inférieur au chiffre et ensuite indiquer votre confiance en votre réponse", color='white', pos=(0, 7), height=1, ori=180)
instruction_training2 = visual.TextStim(win=win, text= "Vous allez voir un nuage de points ainsi qu'un chiffre, votre but est d'estimer si le nombre de points dans le nuage est supérieur ou inférieur au chiffre et ensuite indiquer votre confiance en votre réponse", color='white', pos=(0, -7), height=1) 
instruction_training3 = visual.TextStim(win=win, text= "Ensuite l'un d'entre vous va partager sa réponse et son niveau de confiance avec les autres, et vous allez tous avoir l'opportunité de changer votre réponse si vous le souhaitez", color='white', pos=(0, 7), height=1, ori=180)
instruction_training4 = visual.TextStim(win=win, text= "Ensuite l'un d'entre vous va partager sa réponse et son niveau de confiance avec les autres, et vous allez tous avoir l'opportunité de changer votre réponse si vous le souhaitez", color='white', pos=(0, -7), height=1) 

instruction_training5 = visual.TextStim(win=win, text= "Tous les 46 essaies vous allez voir un nuage de points composé de 45 points, durant ce type d'essaie il vous est uniquement demandé d'être attentif au nuage de points.", color='white', pos=(0, 7), height=1, ori=180)
instruction_training6 = visual.TextStim(win=win, text= "Tous les 46 essaies vous allez voir un nuage de points composé de 45 points, durant ce type d'essaie il vous est uniquement demandé d'être attentif au nuage de points.", color='white', pos=(0, -7), height=1) 

intro_training = visual.TextStim(win=win, text= "L'entrainement va commencer", color='white', pos=(0, 7), height=1, ori=180)
intro_training2 = visual.TextStim(win=win, text= "L'entrainement va commencer", color='white', pos=(0, -7), height=1) 

instruction_message_deux = visual.TextStim(win=win, text= "La tâche principale commence", color='white', pos=(0, 7), height=1, ori=180)
instruction_message_deux2 = visual.TextStim(win=win, text= "La tâche principale commence", color='white', pos=(0, -7), height=1) 

end_thanks = visual.TextStim(win=win, text= "Vous avez terminé !\n Merci d'avoir participé !", color='white', pos=(0, 7), height=1, ori=180) 
end_thanks2 = visual.TextStim(win=win, text= "Vous avez terminé !\n Merci d'avoir participé !", color='white', pos=(0, -7), height=1) 

#Stimulus

fixation_cross = visual.TextStim(win=win, text="+", color='white', pos=(0, 0), height=5)

welcome_message.draw()
welcome_message2.draw()
win.flip()
event.waitKeys(keyList = "space")
win.flip()

induction_intro.draw()
induction_intro2.draw()
win.flip()
event.waitKeys(keyList= "space")
win.flip()

instruction_training1.draw()
instruction_training2.draw()
win.flip()
event.waitKeys(keyList= "space")
win.flip()

number_dots = 5
arabic_number = 10

dot_positions = create_dot_positions(number_dots, circleRadius, dotRadius)
XY_cord = [(x, y+1) for x, y in dot_positions]  
circle = visual.Circle(win, radius=circleRadius+1 ,fillColor=None, lineColor="white", lineWidth=6, pos=(0,1)) 
dots = visual.ElementArrayStim(win, nElements=number_dots, xys=XY_cord, elementTex=None, elementMask="circle", sizes=dotRadius)
t_number_text = visual.TextStim(win=win, text=str(arabic_number), color='white', pos=(0, 13), height=5, ori=180)
b_number_text = visual.TextStim(win=win, text=str(arabic_number), color='white', pos=(0, -11), height=5)
    
# Draw and show the stimuli
dots.draw()
t_number_text.draw()
b_number_text.draw()
circle.draw()
win.flip()
event.waitKeys(keyList = "space")
win.flip()

instruction_training3.draw()
instruction_training4.draw()
win.flip()
event.waitKeys(keyList= "space")
win.flip()

instruction_training5.draw()
instruction_training6.draw()
win.flip()
event.waitKeys(keyList= "space")
win.flip()

intro_training.draw()
intro_training2.draw()
win.flip()
event.waitKeys(keyList = "space")
win.flip()

num_dots_train = [44, 62, 53, 81]
num_arab_train = [42, 64, 47, 87]
for trial in range(4):
    if trial == 3:
        reference_numerosity()
        
    #np.random.seed(trial+ random.randint(0,1000))  
    number_dots = num_dots_train[trial]
    arabic_number = num_arab_train[trial]

    dot_positions = create_dot_positions(number_dots, circleRadius, dotRadius)
    XY_cord = [(x, y+1) for x, y in dot_positions]  
    
    
    circle = visual.Circle(win, radius=circleRadius+1 ,fillColor=None, lineColor="white", lineWidth=6, pos=(0,1)) 
    dots = visual.ElementArrayStim(win, nElements=number_dots, xys=XY_cord, elementTex=None, elementMask="circle", sizes=dotRadius)
    
    
    t_number_text = visual.TextStim(win=win, text=str(arabic_number), color='white', pos=(0, 13), height=5, ori=180)
    b_number_text = visual.TextStim(win=win, text=str(arabic_number), color='white', pos=(0, -11), height=5)
    
    # Draw and show the stimuli
    dots.draw()
    t_number_text.draw()
    b_number_text.draw()
    circle.draw()
    win.flip()
    core.wait(2)
    win.flip()
    rts_training = wait_for_key_presses(trial, "", "black")
    win.flip()
    
        
    if trial == 0:
        p_sharing = "m"
    if trial == 1:
        p_sharing = "p"
    if trial == 2:
        p_sharing = "a"
    if trial == 3:
        p_sharing = "q"
    
    p_num = attributes[p_sharing]['p_num']
    group_affil = attributes[p_sharing]['group_affil']
    col_text = attributes[p_sharing]['col_text']
    
    chosen = "Participant N{}".format(p_num)
    
    p_sharing1 = visual.TextStim(win, text="{} du groupe {} partage.".format(info_participant[chosen], group_affil), pos=(0, 7), color=col_text, ori =180)
    p_sharing2 = visual.TextStim(win, text="{} du groupe {} partage.".format(info_participant[chosen], group_affil), pos=(0, -7), color=col_text)
    p_sharing1.draw()
    p_sharing2.draw()
    win.flip()
    core.wait(1)
    rts_training = wait_for_key_presses(trial, p_num, col_text)
    win.flip()
    fixation_cross.draw()
    win.flip()
    core.wait(0.5)
    
    
    
    
    
    
    
    
    
instruction_message_deux.draw()
instruction_message_deux2.draw()
win.flip()
event.waitKeys(keyList= "space")







for trial in range(num_trials):
    if trial % 46 == 0 and trial != 0:
        reference_numerosity()
    p_sharing = participant_intervention.pop(random.randrange(len(participant_intervention)))
    number_dots = list_dots[trial]
    arabic_number = list_arabic[trial]
        
    dot_positions = create_dot_positions(number_dots, circleRadius, dotRadius)
    XY_cord = [(x, y+1) for x, y in dot_positions]  
    
    circle = visual.Circle(win, radius=circleRadius+1 ,fillColor=None, lineColor="white", lineWidth=6, pos=(0, 1))
    dots = visual.ElementArrayStim(win, nElements=number_dots, xys=XY_cord, elementTex=None, elementMask="circle", sizes=dotRadius)
    
    t_number_text = visual.TextStim(win=win, text=str(arabic_number), color='white', pos=(0, 13), height=5, ori=180)
    b_number_text = visual.TextStim(win=win, text=str(arabic_number), color='white', pos=(0, -11), height=5)
    
    dots.draw()
    t_number_text.draw()
    b_number_text.draw()
    circle.draw()
    
    win.flip()
    
    core.wait(2)

    win.flip()
    
    rts_frst = wait_for_key_presses(trial, "", "black")
    

    # Update waiting message based on who has yet to respond
    p_num = attributes[p_sharing]['p_num']
    group_affil = attributes[p_sharing]['group_affil']
    col_text = attributes[p_sharing]['col_text']
    
    chosen = "Participant N{}".format(p_num)
    p_sharing1 = visual.TextStim(win, text="{} du groupe {} partage.".format(info_participant[chosen], group_affil), pos=(0, 7), color=col_text, ori =180)
    p_sharing2 = visual.TextStim(win, text="{} du groupe {} partage.".format(info_participant[chosen], group_affil), pos=(0, -7), color=col_text)
    p_sharing1.draw()
    p_sharing2.draw()
    win.flip()
    core.wait(1)
    win.flip()
    rts_sec = wait_for_key_presses(trial, p_num, col_text)
    
    win.flip()
    fixation_cross.draw()
    win.flip()
    core.wait(0.5)
    win.flip()
    for key in rts_frst.keys():
        df.loc[trial, 'rt_{}_first_estimation'.format(key)] = rts_frst[key]
        df.loc[trial, 'rt_{}_sec_estimation'.format(key)] = rts_sec[key]
    df.loc[trial, 'trial_num'] = trial
    df.loc[trial, 'arabic_num'] = arabic_number
    df.loc[trial, 'dots_num'] = number_dots
    df.loc[trial, 'group_num'] = info_participant["Numero Groupe"]
    df.loc[trial, 'participant_sharing'] = p_sharing
    

end_thanks.draw()
end_thanks2.draw()
win.flip()
event.waitKeys(keyList = "space")


df.to_csv('data_group_{}_{}.csv'.format(info_participant["Numero Groupe"],random.randint(0,100) ), index=False)
win.close()
core.quit()
