from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tqdm import tqdm

import matplotlib.pyplot as plt
from PIL import Image

from pathlib import Path


def get_voucher(idx: int, ax) -> int:
    
    # select voucher
    voucher_buttons = driver.find_elements(By.CLASS_NAME, 'voucher-content-wrapper')
    button = voucher_buttons[idx]
    driver.execute_script("arguments[0].scrollIntoView();", button)
    
    try:
        button.click()
        
        redeem_button = driver.find_element(By.ID, 'redeem-button')
        redeem_button.click()
        file_name = f'{IMAGE_PATH}/test-{idx}.png'
        voucher_div = driver.find_element(By.CLASS_NAME, 'redemption-card').screenshot(file_name)
        with open(file_name,'rb') as f:
            image=Image.open(f)
            ax_idx = idx%8
            row = ax_idx//2
            col = ax_idx%2
            a = ax[row][col] 
            # print('row', row, 'col', col)
            # a.axis('off')
            a.imshow(image)
            
        back_button = driver.find_element(By.ID, 'redemption-page-back-button')
        back_button.click()
    
        # unselect voucher
        voucher_buttons = driver.find_elements(By.CLASS_NAME, 'voucher-content-wrapper')
        button = voucher_buttons[idx]
        driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()
    except:
        print('Button unclickable. Was the voucher redeemed?')
    
def create_new_plot(bg_color: str):
    fig, ax = plt.subplots(4,2)
    fig.patch.set_facecolor(bg_color)
    # A4 dimensions
    fig.set_size_inches(8.27, 11.69)
    [axi.set_axis_off() for axi in ax.ravel()]
    return fig, ax    

def save_fig(file_name: str): 
    plt.tight_layout()
    print(f'Saving "{file_name}"...')
    plt.savefig(file_name, dpi=300)
    
def get_voucher_by_type(voucher_type: str, bg_color: str):
    nav_button = driver.find_element(By.ID, voucher_type)
    nav_button.click()
    
    num_vouchers = len(driver.find_elements(By.CLASS_NAME, 'voucher-content-wrapper'))

    curr_plot_num = 0
    fig, ax = create_new_plot(bg_color)
    

    for i in tqdm(range(num_vouchers)):
        if i // 8 > curr_plot_num:
            save_fig(f'{PLOT_PATH}/{voucher_type}-{curr_plot_num}.png')
            fig, ax = create_new_plot(bg_color)
            curr_plot_num += 1
        # print('curr_plot_num', curr_plot_num)
        get_voucher(i, ax)
        
    # save last page if num_vouchers not multiples of 2*4 (8 plots on each page)
    if num_vouchers%8 != 0:
        save_fig(f'{PLOT_PATH}/{voucher_type}-{curr_plot_num}.png')
        
    back_button = driver.find_element(By.ID, 'voucher-types-select-vouchers-back-button')
    back_button.click()


if __name__ == '__main__':
    WEB_PATH = '' # Enter CDC link here
    PLOT_PATH = './plots'
    IMAGE_PATH = './images'

    driver=webdriver.Chrome()
    driver.get(WEB_PATH)

    Path(PLOT_PATH).mkdir(parents=True, exist_ok=True)
    Path(IMAGE_PATH).mkdir(parents=True, exist_ok=True)
        
    get_voucher_by_type('cdc-heartland-vouchers-button', 'xkcd:turquoise')
    get_voucher_by_type('cdc-supermarket-vouchers-button', 'xkcd:goldenrod')

    print('Done!')
    driver.close()