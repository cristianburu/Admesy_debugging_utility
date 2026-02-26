from math import trunc

def wav2RGB(Wavelength):
    Gamma = 0.80
    IntensityMax = 255.0
    def Adjust(Color, Factor):
        if Color == 0.0:
            return 0.0
        else:
            return round(IntensityMax * (Color * Factor)**Gamma)
    if 380 <= trunc(Wavelength) and trunc(Wavelength) <= 439:
        Red = -(Wavelength - 440.0) / (440.0 - 380.0)
        Green = 0.0
        Blue = 1.0
    elif 440 <= trunc(Wavelength) and trunc(Wavelength) <= 489:
        Red = 0.0
        Green = (Wavelength - 440.0) / (490.0 - 440.0)
        Blue = 1.0
    elif 490 <= trunc(Wavelength) and trunc(Wavelength) <= 509:
        Red = 0.0
        Green = 1.0
        Blue = -(Wavelength - 510.0) / (510.0 - 490.0)
    elif 510 <= trunc(Wavelength) and trunc(Wavelength) <= 579:
        Red = (Wavelength - 510.0) / (580.0 - 510.0)
        Green = 1.0
        Blue = 0.0
    elif 580 <= trunc(Wavelength) and trunc(Wavelength) <= 644:
        Red = 1.0
        Green = -(Wavelength - 645.0) / (645.0 - 580.0)
        Blue = 0.0
    elif 645 <= trunc(Wavelength) and trunc(Wavelength) <= 780:
        Red = 1.0
        Green = 0.0
        Blue = 0.0
    else:
        Red = 0.0
        Green = 0.0
        Blue = 0.0
    # Let the intensity fall off near the vision limits
    if 380 <= trunc(Wavelength) and trunc(Wavelength) <= 419:
        factor = 0.3 + 0.7*(Wavelength - 380.0) / (420.0 - 380.0)
    elif 420 <= trunc(Wavelength) and trunc(Wavelength) <= 700:
        factor = 1.0
    elif 701 <= trunc(Wavelength) and trunc(Wavelength) <= 780:
        factor = 0.3 + 0.7*(780.0 - Wavelength) / (780.0 - 700.0)
    else:
        factor = 0.0
    R = Adjust(Red, factor)
    G = Adjust(Green, factor)
    B = Adjust(Blue, factor)
    return [int(R), int(G), int(B)]

def wav2RGB_v2(Wavelength): # from Martin Brown - Stackoverflow
    R = 0
    G = 0
    B = 0
    if 380 <= Wavelength and Wavelength < 440:
        R = (440-Wavelength)/(440-380)
        B = 1
    else:
        if Wavelength < 505:
            G = (Wavelength-440)/(505-440)
            B = 1
        else:
            if Wavelength < 540:
                G = 1
                B = (540-Wavelength)/(540-505)
            else:
                if Wavelength < 585:
                    R = (Wavelength-540)/(585-540)
                    G = 1
                else:
                    if Wavelength <= 675:
                        R = 1
                        G = (675-Wavelength)/(675-585)
                    else:
                        if Wavelength < 780:
                            R = 1
    factor = 1
    lum = 0.55*G + 0.29*R + 0.11*B
    if (lum > 0.65) and (B > 0.6): # fixup cyan luminance excess
        factor = 0.65
    if (lum > 0.8) and (R > 0.7): # fixup yellow luminance excess
        factor = 0.8
    if (380 <= Wavelength) and (Wavelength <= 420):
        factor = 0.3+0.7*(Wavelength-380)/(420-380)
    else:
        if (701 <= Wavelength) and (Wavelength <= 780):
            factor = 0.3+0.7*(780-Wavelength)/(780-700)
    R = 255*R*factor
    G = 255*G*factor
    B = 255*B*factor
    return [int(R), int(G), int(B)]

def generateColor(color,nr_of_colors=256,first_wl=380,last_wl=780):
    nstep = nr_of_colors - 1
    bandW = last_wl - first_wl
    colorTuple = ()
    for i in range(nr_of_colors):
        wlength = first_wl + i * bandW / nstep
        colorTuple += ((1.0 * i / nstep, wav2RGB(wlength)[color] / 255.0, wav2RGB(wlength)[color] / 255.0),)
    return colorTuple

def generateGradient(nr_of_colors=256,first_wl=380,last_wl=780):
  return {'red':  generateColor(0,nr_of_colors,first_wl,last_wl),
          'green': generateColor(1,nr_of_colors,first_wl,last_wl),
          'blue':  generateColor(2,nr_of_colors,first_wl,last_wl)}
