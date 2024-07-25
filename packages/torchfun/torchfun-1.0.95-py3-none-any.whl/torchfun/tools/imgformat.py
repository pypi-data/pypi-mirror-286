# LICENSE: MIT
# Author: CHEN Si Yu.
# Date: 2018
# Appended constrains: If the content in this project is used in your source-codes, this author's name must be cited at the begining of your source-code. 


import os,shutil
from glob import glob
from tqdm import tqdm
from sys import argv
import argparse
import imageio,img2pdf
from PIL import Image

parser = argparse.ArgumentParser(description='Image Format Transformer')
parser.add_argument('files', metavar='FILE_PATTERN', type=str, nargs='+',
                        help='files to be transformed, can be like xx/yy/z.jpg, or like xx/yy/*.png')
parser.add_argument('-t','--type',dest='type', type=str, default=None, help='output image type')
parser.add_argument('-d','--dir',dest='dir', type=str, default=None, help='dir to store output images, default: same dir as the input image.')

class ImagePuzzleSlicer(object):
    '''slice nchw image into patches for inference. and then also able to put these puzzle patches back into a image.
    usage:
    p = ImagePuzzleSlicer(default_patch_size=256)
    sliceing_plan = p.make_slicing_plan(myimg)
    
    for hs,he,ws,we in sliceing_plan:
        this_patch = myimg[...,hs:he,ws:we]

    '''
    def __init__(self,default_patch_size):
        self.default_patch_size = default_patch_size

    def make_slicing_plan(self,hw_image,override_patch_size=None):
        '''
        override_patch_size: use a given patch size to override default setting.
        '''
        h,w = hw_image.shape[-2:]
        patch_size = override_patch_size or self.default_patch_size
        
        if patch_size>min(h,w):
            tf.ui.error(f"patch size{patch_size} is larger than image size:{h},{w}!")

        hpatches_fullsize = h//patch_size
        hpatches_last = 0 if (hpatches_fullsize*patch_size == h) else 1
        wpatches_fullsize = w//patch_size
        wpatches_last = 0 if (wpatches_fullsize*patch_size == w) else 1

        hstart_hend_wstart_wend_slices = []
        for hpatch_idx in range(hpatches_fullsize + hpatches_last):
            for wpatch_idx in range(wpatches_fullsize + wpatches_last):
                hpixel_idx = hpatch_idx*patch_size
                wpixel_idx = wpatch_idx*patch_size

                hpixel_end_idx = hpixel_idx + patch_size
                wpixel_end_idx = wpixel_idx + patch_size

                if hpixel_end_idx>h:
                    hpixel_end_idx = h 
                    hpixel_idx = h - patch_size

                if wpixel_end_idx>w:
                    wpixel_end_idx = w 
                    wpixel_idx = w - patch_size 

                hstart_hend_wstart_wend_slices.append((hpixel_idx,hpixel_end_idx,wpixel_idx,wpixel_end_idx))
        return hstart_hend_wstart_wend_slices

    def __call__(self,*args,**kws):
        return self.make_slicing_plan(*args,**kws)

    def recover_image_from_puzzles(self,full_image,patches:list,slicing_plan:list):
        for patch,(h1,h2,w1,h2) in zip(patches,slicing_plan):
            full_image[...,h1:h2,w1:w2] = patch
        return full_image



def img2pdf_wrapper(srcpath,destpath):
    img = Image.open(srcpath)
    with open(destpath,'wb') as f:
        pdf_bytes = img2pdf.convert(img.filename)
        f.write(pdf_bytes)
        f.close()
    img.close()
    return

def imgformat():
    opt=parser.parse_args(argv[1:])
    if not opt.type:
        print('please specify output type by -t or --type possible values: png,jpg,eps,bmp,gif...')
        return 0
    else:
        opt.type = opt.type.lower()

    more_files = []
    files = []
    for fpath in opt.files:
        if '*' in fpath:
            more_files.extend(glob(fpath))
        else:
            files.append(fpath)
    all_fpaths = list(set(more_files+files))
    filenumbers = len(all_fpaths)
    for i,imgpath in enumerate(all_fpaths):
        i = i+1
        srcdir = os.path.dirname(imgpath)
        srcname = os.path.basename(imgpath)
        srctag = '.'.join(srcname.split('.')[:-1])
        srctype = srcname.split('.')[-1].lower()
        destdir = opt.dir or srcdir
        destpath = os.path.join(destdir,srctag+'.'+opt.type)
        if opt.type == srctype: # no need to transform nor read file
            if os.path.abspath(srcdir) != os.path.abspath(destdir): 
                shutil.copy(imgpath,destpath)
                print(i,'/',filenumbers,imgpath,'copy->',destpath)
            else:
                print(i,'/',filenumbers,'skipping',imgpath)
        else: # really need to transform format
            print(i,'/',filenumbers,imgpath,'->',destpath)
            if opt.type == 'pdf':
                img2pdf_wrapper(imgpath,destpath)
            else:
                imgnp = imageio.imread(imgpath)
                dims = len(imgnp.shape)
                if (dims==3) and (imgnp.shape[2]==4):
                    # RGBA image
                    imgnp = imgnp[:,:,:3]
                imageio.imsave(destpath,imgnp)
    print('finished.')
    return 0

def main():
    return imgformat()

if __name__ == '__main__':
  main()