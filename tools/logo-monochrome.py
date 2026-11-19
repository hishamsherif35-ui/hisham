import sys, numpy as np
from PIL import Image
W=sys.argv[1]
INK=(17,18,20)
L=[ # slug, file, opts
 ('mbc','mbc.png',{}),('redbull','redbull.png',{}),('vogue-arabia','v_p2.png',{}),
 ('shark-tank-masr','v_p1.png',{}),('eg-bank','raw/egbank.jpg',{}),('madinet-masr','v_p3.png',{}),
 ('magdi-yacoub','raw/myf.png',{}),('saoud','v_saoud.png',{}),('mostakbal-city','raw/mostakbal.png',{}),
 ('masyaf','raw/masyaf.png',{}),('alqamzi','raw/alqamzi.jpg',{}),('vzbl','raw/vzbl.jpg',{'crop':(300,980,560,1110)}),
 ('plugn','plugn.png',{'gain':2}),('il-cazar','v_ilcazar.png',{}),('kulture','raw/kulture.png',{}),
 ('grand-lane','raw/grandlane.png',{}),('navy26','raw/navy26.png',{}),('cred','raw/cred.png',{}),
 ('one-of-one','raw/oneofone.png',{}),('ladyy','raw/ladyy.png',{}),('elmehelmy','raw/elmehelmy.jpg',{'cut':0.45,'gain':1.6}),
 ('atai','raw/atai_still.png',{'crop':(931,1672,1022,1768),'lum':True}),
]
import json; meta=[]
for slug,f,o in L:
  im=Image.open(W+'/'+f).convert('RGBA')
  if 'crop' in o: im=im.crop(o['crop'])
  a=np.asarray(im).astype(float); rgb=a[...,:3]; al=a[...,3]/255
  if o.get('lum'):
    m=1-(rgb.mean(-1)/255); m=np.clip((m-0.05)/0.9,0,1)
  elif (al<0.08).mean()>0.2:
    m=al; mode='alpha'
  else:
    comp=rgb*al[...,None]+255*(1-al[...,None])
    h,w=al.shape; cs=[comp[:8,:8],comp[:8,-8:],comp[-8:,:8],comp[-8:,-8:]]
    bg=np.median(np.concatenate([c.reshape(-1,3) for c in cs]),0)
    d=np.sqrt(((comp-bg)**2).sum(-1)); mx=np.percentile(d[d>12],95) if (d>12).any() else 1
    m=np.clip(d/mx*o.get('gain',1),0,1)
    cut=o.get('cut',0.12); m=np.clip((m-cut)/(1-cut),0,1)
  ys,xs=np.where(m>0.1)
  y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
  m=m[y0:y1,x0:x1]
  out=np.zeros(m.shape+(4,),np.uint8); out[...,0],out[...,1],out[...,2]=INK; out[...,3]=(m*255).astype(np.uint8)
  img=Image.fromarray(out); img.thumbnail((480,160),Image.LANCZOS)
  img.save(f'{W}/out/{slug}.png',optimize=True)
  meta.append((slug,img.size))
print(json.dumps(meta))
