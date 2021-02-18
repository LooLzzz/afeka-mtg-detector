import os, cv2
import pandas as pd
from matplotlib import pyplot as plt

import scryfall_client as Scryfall
import fetch_data as fetch
import p_hash as phash
from dtd import Backgrounds as bg
from config import Config

if __name__ == "__main__":
    cards_df = fetch.load_all('cards')
    sets_df = fetch.load_all('sets')
    
    # download `n` random images from df
    fetch.fetch_card_images(cards_df, limit_n=10, max_workers=5, delay=0.2)

    flag = input('would you like to calculate pHash for all the cards? THIS WILL TAKE ABOUT 10-15 MINUTES (y/n): ')
    if flag:
        phash_df = phash.get_pHash()

    # bgs = Backgrounds()
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    while True:
        img = bg.get_random()
        cv2.imshow('image', img)
        key = cv2.waitKey(0)
        if key == 32: #space key
            continue
        else:
            break
    cv2.destroyAllWindows()

    # loaded_sets.columns
    # list(loaded_sets[loaded_sets['digital']==True]['code'])


    # 'scryfall_query': {
    #     'q': {
    #         'border': 'black',
    #         'frame': 2015, # newest magic
    #         'layout': 'normal', # no flip,fuze,modal,etc..
    #     },
    #     '_is': 'funny', # no un-sets
    # }
    # scryfall_query = {
    #     'q': {
    #         'set': ['m21','m20'],
    #         'frame': 'legendary',
    #     },
    # }

    # res = scryfall.search(**scryfall_query)
    # res[['name', 'set', 'image_uris']]