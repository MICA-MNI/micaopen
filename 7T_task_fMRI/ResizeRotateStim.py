# housekeeping
import os
import shutil
import random
from PIL import Image
from psychopy import data

# import stimuli
root_dir = "/Users/shahin/Desktop/"
src_dir = root_dir + "ListA_2/"
img_dir = root_dir + "ListA_2/"

# create list of rotation angles (ie, [-45, -15] U [15, 45])
ang1 = range(15, 46)
ang2 = range(-45, -14)
angle = list(set(ang1).union(ang2))

for idx in list(range(0, 24)):

    # load stimuli
    prime = Image.open(src_dir + "prime" + str(idx + 1) + ".png")
    target = Image.open(src_dir + "target" + str(idx + 1) + ".png")
    foil1 = Image.open(src_dir + "foil" + str(idx + 1) + "_1.png")
    foil2 = Image.open(src_dir + "foil" + str(idx + 1) + "_2.png")

    # resize stimuli
    prime_size = prime.size
    x_prime = prime_size[0]
    y_prime = prime_size[1]

    target_size = target.size
    x_target = target_size[0]
    y_target = target_size[1]

    foil1_size = foil1.size
    x_foil1 = foil1_size[0]
    y_foil1 = foil1_size[1]

    foil2_size = foil2.size
    x_foil2 = foil2_size[0]
    y_foil2 = foil2_size[1]

    # if x_prime     >= y_prime:
    # primeFact  = 240 / x_prime
    # else:
    # primeFact  = 240 / y_prime

    new_xP = int(x_prime * .0808)
    new_yP = int(y_prime * .0808)

    new_xT = int(x_target * .0808)
    new_yT = int(y_target * .0808)

    new_xF1 = int(x_foil1 * .0808)
    new_yF1 = int(y_foil1 * .0808)

    new_xF2 = int(x_foil2 * .0808)
    new_yF2 = int(y_foil2 * .0808)

    resized_P = prime.resize((new_xP, new_yP))
    resized_T = target.resize((new_xT, new_yT))
    resized_F1 = foil1.resize((new_xF1, new_yF1))
    resized_F2 = foil2.resize((new_xF2, new_yF2))

    # rotate stimuli
    rot_ang = random.choice(angle)

    Rot_T = resized_T.rotate(rot_ang, expand=True, resample=Image.BICUBIC)
    Rot_F1 = resized_F1.rotate(rot_ang, expand=True, resample=Image.BICUBIC)
    Rot_F2 = resized_F2.rotate(rot_ang, expand=True, resample=Image.BICUBIC)

    # save stimuli
    resized_P.save(img_dir + "prime" + str(idx + 1) + ".png")
    Rot_T.save(img_dir + "target" + str(idx + 1) + ".png")
    Rot_F1.save(img_dir + "foil" + str(idx + 1) + "_1.png")
    Rot_F2.save(img_dir + "foil" + str(idx + 1) + "_2.png")
