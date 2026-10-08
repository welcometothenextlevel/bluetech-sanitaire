import numpy as np
from PIL import Image
from scipy import ndimage as ndi
im=Image.open("_src/WhatsApp Image 2026-10-04 at 6.20.42 PM.jpeg").convert("RGB").crop((220,420,810,640))
S=4; im=im.resize((im.width*S,im.height*S),Image.LANCZOS)
a=np.asarray(im).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]
blue=(b-r>45); grey=(~blue)&(r<200)&(abs(r-b)<40)
yy=np.arange(a.shape[0])[:,None]; grey&=(yy>128*S)
for name,m in (("blue",blue),("grey",grey)):
    m=ndi.binary_opening(m,iterations=2)
    lab,n=ndi.label(m); objs=ndi.find_objects(lab); dt=ndi.distance_transform_edt(m)
    rows=[]
    for k,sl in enumerate(objs):
        mk=lab[sl]==k+1; area=mk.sum()
        if area<300: continue
        y0,y1=sl[0].start/S,sl[0].stop/S; x0,x1=sl[1].start/S,sl[1].stop/S
        sw=2*np.median(dt[sl][mk][dt[sl][mk]>np.percentile(dt[sl][mk],80)])/S
        rows.append((round(x0,1),round(y0,1),round(x1,1),round(y1,1),round(sw,1)))
    rows.sort(); print(name); [print(" ",r) for r in rows]
