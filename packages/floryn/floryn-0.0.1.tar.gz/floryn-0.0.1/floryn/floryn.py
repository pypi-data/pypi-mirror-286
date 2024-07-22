# Packge floryn is for creating a plot for text with shaded based on percentage value provide in the parameter

import io
import skimage
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def pp(text, percentage=0.5, 
       color='denim blue',
       font='Helvetica',
       fontsize=144, 
       ax=None, 
       orientation='vertical', 
       gradient=True):
    """
    Plot a text with percentage filled
    
    :param str text: the string to be plot
    :param float percentage: the percentage of filled color, from 0 to 1
    :param str color: the color of the text, based on seaborn color palette
    :param plt.Axes ax: the matplotlib axes object to put the result into

    """

    # Create the base text
    fig, ax1 = plt.subplots(figsize=(13, 2));
    ax1.text(0, 0, text, fontname=font, fontsize=fontsize, fontweight='bold', color=sns.xkcd_rgb['light grey']);
    ax1.axis('off');

    ax1.xaxis.set_major_locator(plt.NullLocator());
    ax1.yaxis.set_major_locator(plt.NullLocator());

    io_buf = io.BytesIO()
    fig.savefig(io_buf, format='png', dpi=300, bbox_inches='tight', pad_inches=0);
    
    io_buf.seek(0)
    img = skimage.io.imread(io_buf)
    height, width, _ = img.shape
    output = np.copy(img)
    
    io_buf.close()
    plt.close()

    # create the mask to be to filter the filled area
    light_grey = sns.xkcd_palette(['light grey'])[0]
    light_grey = [int(x*255) for x in light_grey] + [255]
    light_grey

    mask = (img == light_grey).all(-1)

    if orientation == 'vertical':
        np_index = 1
    elif orientation == 'horizontal':
        np_index = 0
    else:
        raise Exception('Orientation is not recognized. Please select either vertical or horizontal')

    start = np.where(mask.any(np_index) == True)[0][0]
    end = np.where(mask.any(np_index) == True)[0][-1]
    font_height = end - start

    mask2 = np.zeros((height, width), dtype=bool)

    # because image coordinate (0, 0) is at the top left
    if orientation == 'vertical':
        mask2[(font_height - int(percentage*font_height)):end, :] = True
    elif orientation == 'horizontal':
        mask2[:, start:(start+int(font_height*percentage))] = True

    mask3 = mask & mask2

    # apply the new color on top of base image based on the mask
    if gradient:
        mask_color = sns.light_palette(sns.xkcd_palette([color])[0], 20)[int(15*percentage)+4]
    else:
        mask_color = sns.xkcd_palette([color])[0]
    mask_color = [int(x*255) for x in mask_color]
    output[mask3] = mask_color + [255]

    if ax is not None:
        ax.imshow(output)
        ax.axis('off');

    return output
