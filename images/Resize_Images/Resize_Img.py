import os
import glob
from skimage import io
import shutil
import torchvision
import torchvision.transforms as transforms



root_dir = 'Original_Imgs/*'
target_dir = 'Resized_Imgs/'   ##### To get the best visualization result, we need images to be 2400 * 2400

count = 0

"""
needed_transform = transforms.Compose(
    [transforms.ToPILImage(mode=None),
     transforms.Resize(size=(512, 512), interpolation=2),
     transforms.ToTensor(),])
"""

needed_transform = transforms.Compose(
    [transforms.ToPILImage(mode=None),
     transforms.Resize(size=(2400,4000), interpolation=2),
     transforms.ToTensor(),])



for img_path in glob.glob(root_dir):
    if count == 100:
        print('We have {} images now!'.format(count))
        break
    cur_img = io.imread(img_path)
    img_name = img_path.split('/')[-1]
    img_path_dest = os.path.join(target_dir, img_name)
    print('#####')
    print(cur_img.shape)
    try:
        resize_img = needed_transform(cur_img)
    except:
        assert False, 'Resizing cannot be done!'
    torchvision.utils.save_image(resize_img, img_path_dest)




