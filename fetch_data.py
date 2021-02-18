import requests, cv2, os
import pandas as pd
import numpy as np
from scryfall_client import scryfall
from task_executor import TaskExecutor
from config import Config
# from IPython.display import display

def fetch_card_img(card, to_file=False):
    '''
    `card` should have the following properties: {`set`, `name`, (`image_uris` or `img_url`)}
    '''
    if 'image_uris' in card:
        # img_url = card['image_uris']['large']
        img_url = card['image_uris']['normal']
    else:
        img_url = card['img_url']
    setid = card['set']
    card_name = card['name'] \
                    .lower() \
                    .replace(' ', '_') \
                    .replace(',', '') \
                    .replace('\'', '')
    filename = f'{setid}-{card_name}'
    subdir = f"{Config.cards_path}/images"
    path = f'{subdir}/{filename}.jpg'

    
    # get img from local dir
    if os.path.exists(path):
        print(f"image exists, loading '{filename}'..") #DEBUG
        return cv2.imread(path)
    # else:
    # get img from url
    print(f"image doesnt exist, fetching '{filename}'..") #DEBUG
    res = requests.get(img_url, stream=True).raw
    img = np.asarray(bytearray(res.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # save it
    if to_file:
        os.makedirs(subdir, exist_ok=True)
        cv2.imwrite(path, img)
    print(f"'{filename}' done.")
    return img

def fetch_card_images(cards_df:pd.DataFrame, limit_n=None, limit_frac=None, max_workers=5, delay=0.1):#, i=None):
    if limit_n != None:
        cards_df = cards_df.sample(n=limit_n)
    elif limit_frac != None:
        cards_df = cards_df.sample(frac=limit_frac)

    # setup queue for fetching requested card images
    # added delay to workers as requested by scryfall,
    # https://scryfall.com/docs/api#rate-limits-and-good-citizenship
    task_master = TaskExecutor(max_workers=max_workers, delay=delay)
    futures = []
    for (_i,card) in cards_df.iterrows():
        future = task_master.submit(task=fetch_card_img, card=card, to_file=True)
        futures += [(card['name'], future)]
    
    # get results from futures
    res = []
    for (card_name,future) in futures:
        try:
            res += [future.result()]
        except TypeError as err:
            if 'NoneType' in str(err):
                print(f'#### TypeError(NoneType) while retrieving results from {card_name} ####')
                # print(err)
            else:
                raise err
    return res
    


#######################################################################################


'''
get all prints of a specific card
https://api.scryfall.com/cards/search?q=oracleid:aa7714b0-2bfb-458a-8ebf-37ec2c53383e&unique=prints
https://api.scryfall.com/cards/search?q="sol ring"&unique=prints
## for a fuzzy search drop the "" in the 'q=' 

get all cards from a set
https://api.scryfall.com/cards/search?q=set:m10+lang:en

for layout&frame specific tasks refer to
https://scryfall.com/docs/api/layouts
'''