
import numpy as np 


def wavelength_to_rgb(wavelength, gamma=0.8):
    """
    Converts a wavelength in the range of 380 to 750 nm to an approximate RGB color.

    Parameters:
        wavelength (float): Wavelength in nanometers.
        gamma (float): Gamma correction factor.

    Returns:
        (int, int, int): Tuple representing RGB color values.
    """
    # Validate wavelength range
    if not (380 <= wavelength <= 750):
        return (0, 0, 0)

    # Initial RGB components and attenuation
    R = G = B = 0.0
    attenuation = 1.0

    # Define color transition ranges for each wavelength band
    if 380 <= wavelength < 440:
        R = (440 - wavelength) / (440 - 380)
        B = 1.0
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
    elif 440 <= wavelength < 490:
        G = (wavelength - 440) / (490 - 440)
        B = 1.0
    elif 490 <= wavelength < 510:
        G = 1.0
        B = (510 - wavelength) / (510 - 490)
    elif 510 <= wavelength < 580:
        R = (wavelength - 510) / (580 - 510)
        G = 1.0
    elif 580 <= wavelength < 645:
        R = 1.0
        G = (645 - wavelength) / (645 - 580)
    elif 645 <= wavelength <= 750:
        R = 1.0
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)

    # Apply gamma correction and adjust by attenuation for realistic fading at spectrum edges
    R = int((R * attenuation) ** gamma * 255)
    G = int((G * attenuation) ** gamma * 255)
    B = int((B * attenuation) ** gamma * 255)

    return (R, G, B)


def wavelength_to_rgb_vect(vect, gamma=1):
    if isinstance(vect, int) | isinstance(vect, float):
        RGB_vect = wavelength_to_rgb(vect, gamma=gamma)
    else:
        RGB_vect = np.zeros((len(vect), 3))
        for i in range(len(vect)):
            RGB = wavelength_to_rgb(vect[i], gamma=gamma)
            RGB_vect[i, 0] = RGB[0]
            RGB_vect[i, 1] = RGB[1]
            RGB_vect[i, 2] = RGB[2]
    return RGB_vect


def SpectralStack2RGB(Stack, Ch_wavelength):
    RGB_vect = wavelength_to_rgb_vect(Ch_wavelength)
    Size = np.shape(Stack)
    RGB_img = np.zeros((Size[1], Size[2], 3))
    for ch in range(Size[0]):
        for col in range(3):
            RGB_img[:, :, col] = RGB_img[:, :, col] + Stack[ch, :, :] * RGB_vect[ch, col]
    return RGB_img

def tile_stitching(img, m, n, bidirectional=False, percentage_overlap = 0):
    X = img.shape[-2]
    Y = img.shape[-1]
    dX = int(percentage_overlap/100*X/2)
    dY = int(percentage_overlap/100*Y/2)

    img_rec = np.zeros(np.array([img.shape[1], X-2*dX, Y-2*dY]) * np.array([1, m, n]))

    cnt_slice = 0
    for i in range(m):
        if bidirectional & ((i % 2) != 0):
            j_range = np.flip(np.arange(n))
        else:
            j_range = np.arange(n)
        for j in j_range:
            img_rec[:,i*(X-2*dX):(i+1)*(X-2*dX),j*(Y-2*dY):(j+1)*(Y-2*dY)] = img[cnt_slice,:,dX:X-dX,dY:Y-dY]
            cnt_slice += 1
    return img_rec

def load_pure_phasors(pure_spectra_path=None, dye_list=None, ch_vec=None, use_extra_coord=True, verbose=False,
                      manual=False, s4=False):
    """Loads the pure phasors from a spectra file.
    pure_spectra_path: Path object for desired set of spectra.
    dye_list: list of dyes present in the sample. Necessary since spectra file may have extra spectra.
    ch_vec: array of what channels to use. (i.e. 0-32 or 10-32, etc)
    use_extra_coord: whether or not to use the redundant last harmonic coordinate.
    :type s4: object"""

    with np.load(pure_spectra_path) as npz:
        dye_labels = npz['labels']
        pure_spectra = npz['spectra']

    dye_idxs = [np.nonzero(dye_labels == dye_name)[0][0] for dye_name in dye_list]
    pure_spectra = pure_spectra[:, dye_idxs]  # (32, n_spectra)
    if manual == True:
        pure_phasors = get_phasor_unmix_matrix_manual(pure_spectra, use_extra_coord=use_extra_coord)
    else:
        pure_phasors = get_phasor_unmix_matrix_less_coords(pure_spectra, use_extra_coord=use_extra_coord, s4=s4)
    if ch_vec is not None:
        pure_spectra = pure_spectra[ch_vec, :]

    print(pure_spectra.shape)

    # pure_phasors = get_phasor_unmix_matrix(pure_spectra)
    if verbose:
        print(pure_phasors.shape)
        print(pure_phasors)

    return pure_phasors
    # return np.load('/content/drive/Shareddrives/Laboratory for Fluorescence Dynamics/Data/2022.07.22 - Contractility 2DG/pure_phasors.npy')

def get_phasor_unmix_matrix_manual(mat, use_extra_coord):
    # mat: (channels, n_spectra)
    n_spectra = 4
    gs = np.zeros((n_spectra, n_spectra))

    g1, s1 = phasor_transform(mat, n_harm=1, axis=0)
    g2, s2 = phasor_transform(mat, n_harm=2, axis=0)
    gs = np.stack([g1, s1, g2, s2], axis=1)
    return gs

def phasor_transform(x, n_harm=1, axis=0, debug=False):
    """Computes the phasor transform of 'x'.
    n_harm: which harmonic of the fourier transform to take.
    axis: which dimension of 'x' the phasor transform is computed along."""
    print(x.shape)
    fft = np.fft.fft(x, axis=axis)
    # make sure to take nth harmonic from the correctly collapsed axis
    # this is fancy stuff to make this function work with any dimension of data
    n_harm_index = [slice(None) for _ in range(x.ndim)]
    n_harm_index[axis] = n_harm
    harm_0_index = [slice(None) for _ in range(x.ndim)]
    harm_0_index[axis] = 0

    # actual phasor transform expression
    gs = fft[tuple(n_harm_index)] / fft[tuple(harm_0_index)]
    g, s = np.real(gs), np.imag(gs)

    if debug:
        g_isnan = np.isnan(g)
        s_isnan = np.isnan(s)
        print(f'g nans: {np.sum(g_isnan)}')
        print(f'g good: {np.sum(~g_isnan)}')
        print(f's nans: {np.sum(s_isnan)}')
        print(f's good: {np.sum(~s_isnan)}')
    return (g, s)

def get_phasor_unmix_matrix_less_coords(mat, use_extra_coord=True, s4=False):
    """Generalized unmixing matrix for any number of mixed spectra."""
    # mat.shape: (n_channels, n_spectra (e.g. components))
    n_spectra = mat.shape[1]

    if use_extra_coord:
        n_full_harms = (n_spectra - 1) // 2
    else:
        n_full_harms = n_spectra // 2

    gs = np.zeros((n_spectra, n_spectra))
    for i in range(n_full_harms):
        n_harm = i + 1
        gs[:, 2 * i], gs[:, 2 * i + 1] = phasor_transform(mat, n_harm=n_harm, axis=0)

    if use_extra_coord:
        # an even number of spectra will have two cols blank after full harmonics
        if n_spectra % 2 == 0:
            # first add the s coordinate of the next harmonic
            g_last, s_last = phasor_transform(mat, n_harm=n_full_harms + 1, axis=0)
            gs[:, -2] = s_last

        # add a column of ones to make the matrix a square. This happens regardless of spectra parity
        gs[:, -1] = 1
    else:
        # an even number of spectra will be done after using full harmonics
        if n_spectra % 2 == 1:
            gs[:, -1] = 1
            print('this is being used')

    if s4:
        g_last, s_last = phasor_transform(mat, n_harm=n_full_harms + 1, axis=0)
        gs[:, -1] = s_last

    return gs

def image_to_components_multi_harm_less_coords(img, pure_phasors, use_extra_coord, s4=False):
    """Converts an (c, m, n) image into a (c, m, n) stack of unmixed components.

    Works for number of spectra that require multiple fft harmonics to unmix.
    Does not use the extra g or s coordinate if not necessary."""

    n_components = pure_phasors.shape[0]
    print('n_comps', n_components)

    if use_extra_coord:
        n_full_harms = (n_components - 1) // 2
    else:
        n_full_harms = n_components // 2
    stack_input = []

    for i in range(n_full_harms):
        harm_n = i + 1
        g_harm, s_harm = phasor_transform(img, n_harm=harm_n, axis=0)
        stack_input.extend([np.ravel(g_harm), np.ravel(s_harm)])

    if not use_extra_coord:
        if n_components % 2 == 1:
            if s4:
                g_last, s_last = phasor_transform(img, n_harm=n_full_harms + 1, axis=0)
                stack_input.append(np.ravel(s_last))
                print('4th harmonic is being used')

            else:
                stack_input.append(np.ones_like(stack_input[0]))


    else:
        if n_components % 2 == 0:
            g_last, s_last = phasor_transform(img, n_harm=n_full_harms + 1, axis=0)
            stack_input.append(np.ravel(s_last))

        stack_input.append(np.ones_like(stack_input[0]))

    int_img = np.sum(img, axis=0)  # total intensities for each pixel

    gs_mat = np.stack(stack_input, axis=-1)  # (n_pix, n_harm * 2)
    print('gs_mat.shape', gs_mat.shape)
    phasor_to_frac = np.linalg.inv(pure_phasors)
    print('phasor_to_frac.shape', phasor_to_frac.shape)
    spectra_fracs = gs_mat @ phasor_to_frac

    spectra_fracs[np.isnan(spectra_fracs) | (spectra_fracs < 0)] = 0
    spectra_fracs /= np.sum(spectra_fracs, axis=1)[:, None]
    spectra_fracs[np.isnan(spectra_fracs)] = 0

    spectra_fracs_img = np.zeros((n_components, *int_img.shape))
    # TODO: try transpose method, should be faster
    for i in range(n_components):
        spectra_fracs_img[i] = np.reshape(spectra_fracs[:, i], int_img.shape)

    return spectra_fracs_img * int_img  # (c, 1024, 1024)
