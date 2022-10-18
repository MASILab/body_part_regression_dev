import os
import numpy as np
import nibabel as nb
from nibabel.processing import resample_from_to 
from PIL import Image
import matplotlib.pyplot as plt


class Pre_bodypart(object):
# 0. Resize all image to [512, 512, z]
    def __init__(self, args):
        """Initialize and preprocess the data path."""
        self.data_dir = args.data_dir

    def processing(self):
        print('Check dimension and save a soft tissue window image')
        count = 0
        #create soft img director
        image_dir=os.path.join(self.data_dir, 'images')
        soft_image_dir=os.path.join(self.data_dir, 'soft_images')
        if not os.path.isdir(soft_image_dir):
            os.makedirs(soft_image_dir)
        for image in os.listdir(image_dir):

            # image_idx = int(image.split('_')[1])
            # if image_idx <= 1000: 
            if image.endswith('.nii.gz') and not image.endswith('soft.nii.gz'):
                count+=1
                # Image 
                image_path = os.path.join(image_dir, image)
                soft_image_path = os.path.join(soft_image_dir, image)
                if os.path.isfile(soft_image_path):
                    print('[{}] Exits, skipping {}'.format(count, image))
                    continue
                imgnb = nb.load(image_path)
                imgnp = np.array(imgnb.dataobj)
                shape_size = [imgnp.shape[0], imgnp.shape[1], imgnp.shape[2]]

                
                if shape_size[0] != 512 and shape_size[1] == 512 and shape_size[2] == 512:
                    print('[{}] image reconstruction type invalid (1), rearanging. {}'.format(count, image))
                    imgnp = np.transpose(imgnp, (1,2,0))
                    affine = imgnb.affine
                    affine_tmp = affine[0].copy()

                    affine[0] = affine[1]
                    affine[0][0] = affine[0][1]
                    affine[0][1] = 0.0

                    affine[1] = affine[2]
                    affine[1][1] = affine[1][2]
                    affine[1][2] = 0.0

                    affine[2] = affine_tmp
                    affine[2][2] = affine[2][0]
                    affine[2][0] = 0.0
                    new_imgnb = nb.Nifti1Image(imgnp, affine) 

                    nb.save(new_imgnb, image_path)  

                # elif shape_size[1] != 512 and shape_size[0] == 512 and shape_size[2] == 512:
                elif shape_size[1] != 512 and shape_size[0] == 512:

                    print('[{}] image reconstruction type invalid (2), rearanging. {}'.format(count, image))
                    imgnp = np.transpose(imgnp, (0,2,1))
                    # swap affine matrix
                    nb_affine = imgnb.affine
                    affine_tmp = nb_affine[1].copy()

                    nb_affine[1] = nb_affine[2]
                    nb_affine[1][1] = nb_affine[1][2]
                    nb_affine[1][2] = 0.0

                    nb_affine[2] = affine_tmp
                    nb_affine[2][2] = nb_affine[2][1]
                    nb_affine[2][1] = 0.0

                    new_imgnb = nb.Nifti1Image(imgnp, nb_affine)        
                    nb.save(new_imgnb, image_path)  
                elif shape_size[0] == 512 and shape_size[1] == 512:
                    imgnp = imgnp
                else:
                    print('[{}] image reconstruction type invalid (3), skipping. {}'.format(count, image))
                    continue
                # Set the soft tissue window
                soft_np = imgnp
                idx = np.where(soft_np < -175)
                soft_np[idx[0], idx[1], idx[2]] = -175 # set minmum to -175
                idx = np.where(soft_np > 275)
                soft_np[idx[0], idx[1], idx[2]] = 275 # set maximum to 275
                soft_np = (soft_np - soft_np.min()) * (1.0 - 0.0) / (soft_np.max() - soft_np.min())

                # save an copy of soft tissue window
                soft_nb = nb.Nifti1Image(soft_np, imgnb.affine)        
                nb.save(soft_nb, soft_image_path)  

                
                print('[{}] Saved a copy of soft tissue windowed image {}'.format(count,image))

