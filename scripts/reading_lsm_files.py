import numpy as np
from tqdm import tqdm
import tifffile as tiff
from utils import SpectralStack2RGB, tile_stitching
from PhasorUnmixing import *

IMAGE_PATH = ""                         # define the .lsm file path.
N_TILES = 5                           # could be 5 or 3, check via lsm file dimensions.
TILE_OVERLAP = 10                       # 10 is default.
TIME_POINTS = 15                        # could be 15, 24 or 1 (single timepoint), check via lsm file dimensions.
CHANNEL_VEC = np.arange(0, 32)
DYE_SPECTRA_FP = 'Lipi Modified spectra.npz'
USE_EXTRA_COORD = False  # whether or not to use redundant phasor harmonic component in unmixing.
DYE_LIST = ['LipiBlue', '342', 'BODIPY', 'pHrodo', 'TMRM', 'Lyso', 'Tubulin']  # for 7 color
NTH_HARMONIC = 1  # what harmonic of phasor transform is computed and plotted
WIENER = True


# Loading image tiles and stitching to make full image.
image = tiff.imread(IMAGE_PATH)

full_image = []
for i in range(TIME_POINTS):
    full_image.append(tile_stitching(image[:,i,:,:,:],N_TILES,N_TILES, bidirectional=False, percentage_overlap = TILE_OVERLAP))

image = np.array(full_image)

# Phasor Unmixing.
with tiff.TiffFile(IMAGE_PATH) as tif:
    ms_880 = tif.lsm_metadata
    channel_lambdas = np.asarray(ms_880['ChannelColors']['ColorNames'][:32], dtype=np.float32)

n_comps = len(DYE_LIST)

phasors = []

for t in tqdm(range(TIME_POINTS)):
    t_img = image[t]
    channels, brightfield = t_img[CHANNEL_VEC], t_img[-1]
    int_img = np.sum(channels, axis=0)

    pure_phasors = load_pure_phasors(pure_spectra_path=DYE_SPECTRA_FP,
                                    dye_list=DYE_LIST,
                                    ch_vec=CHANNEL_VEC,
                                    use_extra_coord=USE_EXTRA_COORD)
    
    #Pure Phasors
    pure_phasor_g = pure_phasors[:, (NTH_HARMONIC - 1) * 2]
    pure_phasor_s = -pure_phasors[:, (NTH_HARMONIC - 1) * 2 + 1]

    threshold_mask = (int_img > np.mean(int_img))
    g, s = phasor_transform(channels, n_harm=NTH_HARMONIC, axis=0)
    g = g[threshold_mask]
    s = -s[threshold_mask]
    #Operating on WIENER
    if WIENER:
        filterted_channels = wiener(channels, (1,5,5))

    comp_imgs_wiener = image_to_components_multi_harm_less_coords(
        filterted_channels,
        pure_phasors,
        use_extra_coord=USE_EXTRA_COORD)
    
    phasors.append(comp_imgs_wiener)

phasors = np.array(phasors)

print(phasors.shape) # Should be (TIME_POINTS, 7,  H, W)
    
