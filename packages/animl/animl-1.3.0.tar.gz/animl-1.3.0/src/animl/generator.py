# import numpy as np
from PIL import Image, ImageOps, ImageFile
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms import (Compose, Resize, ToTensor, RandomHorizontalFlip)
from .utils.torch_utils import _setup_size
# import tensorflow as tf
# from tensorflow.keras.utils import Sequence

ImageFile.LOAD_TRUNCATED_IMAGES = True


def resize_with_padding(img, expected_size):
    """Pads a crop to given size
    If the image is torch Tensor, it is expected
    to have [..., H, W] shape, where ... means an arbitrary number of leading dimensions.
    If image size is smaller than output size along any edge, image is padded with 0 and
    then center cropped.

    Args:
        - img (Img): a loaded Img object
        - expected_size (sequence or int): Desired output size of the crop. If size is an
            int instead of sequence like (h, w), a square crop (size, size) is
            made. If provided a sequence of length 1, it will be interpreted as
            (size[0], size[0]).
    Returns:
        - the padded Img object
    """
    if img.size[0] == 0 or img.size[1] == 0:
        return img
    if img.size[0] > img.size[1]:
        new_size = (expected_size[0],
                    int(expected_size[1] * img.size[1] / img.size[0]))
    else:
        new_size = (int(expected_size[0] * img.size[0] / img.size[1]),
                    expected_size[1])
    img = img.resize(new_size, Image.BILINEAR)  # NEAREST BILINEAR
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height,
               delta_width - pad_width,
               delta_height - pad_height)
    return ImageOps.expand(img, padding)


class ResizeWithPadding(torch.nn.Module):
    """Pads a crop to given size
    If the image is torch Tensor, it is expected
    to have [..., H, W] shape, where ... means an arbitrary number of leading dimensions.
    If image size is smaller than output size along any edge, image is padded with 0 and
    then center cropped.

    Args:
        size (sequence or int): Desired output size of the crop. If size is an
            int instead of sequence like (h, w), a square crop (size, size) is
            made. If provided a sequence of length 1, it will be interpreted as
            (size[0], size[0]).
    """
    def __init__(self, expected_size):
        super().__init__()
        self.expected_size = _setup_size(expected_size)

    def forward(self, img):
        """
        Args:
            img (PIL Image or Tensor): Image to be cropped.

        Returns:
            PIL Image or Tensor: Cropped image.
        """
        if img.size[0] == 0 or img.size[1] == 0:
            return img
        if img.size[0] > img.size[1]:
            new_size = (self.expected_size[0],
                        int(self.expected_size[1] * img.size[1] / img.size[0]))
        else:
            new_size = (int(self.expected_size[0] * img.size[0] / img.size[1]),
                        self.expected_size[1])
        img = img.resize(new_size, Image.BILINEAR)  # NEAREST BILINEAR
        delta_width = self.expected_size[0] - img.size[0]
        delta_height = self.expected_size[1] - img.size[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        padding = (pad_width, pad_height,
                   delta_width - pad_width,
                   delta_height - pad_height)
        return ImageOps.expand(img, padding)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(size={self.size})"


# HOW TO HANDLE NON-SQUARE SIZES?
class ImageGenerator(Dataset):
    '''
    Data generator that crops images on the fly, requires relative bbox coordinates,
    ie from MegaDetector

    Options:
        - file_col: column name containing full file paths
        - resize: dynamically resize images to target (square) [W,H]
    '''
    def __init__(self, x, file_col='file', resize=299, crop=True, standardize=True):
        self.x = x
        self.file_col = file_col
        self.crop = crop
        if isinstance(resize, int):
            self.resize = [resize, resize]
        else:
            self.resize = [int(resize[0]), int(resize[1])]
        self.buffer = 0
        self.standardize = standardize
        self.transform = Compose([
            # torch.resize order is H,W
            Resize((self.resize[1], self.resize[0])),
            ToTensor(),
        ])

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        image_name = self.x.loc[idx, self.file_col]

        try:
            img = Image.open(image_name).convert('RGB')
        except OSError:
            print("File error", image_name)
            del self.x.iloc[idx]
            return self.__getitem__(idx)

        width, height = img.size

        if self.crop:
            bbox1 = self.x['bbox1'].iloc[idx]
            bbox2 = self.x['bbox2'].iloc[idx]
            bbox3 = self.x['bbox3'].iloc[idx]
            bbox4 = self.x['bbox4'].iloc[idx]

            left = width * bbox1
            top = height * bbox2
            right = width * (bbox1 + bbox3)
            bottom = height * (bbox2 + bbox4)

            left = max(0, int(left) - self.buffer)
            top = max(0, int(top) - self.buffer)
            right = min(width, int(right) + self.buffer)
            bottom = min(height, int(bottom) + self.buffer)
            img = img.crop((left, top, right, bottom))

        img_tensor = self.transform(img)

        return img_tensor, image_name


# currently working on this class
class TrainGenerator(Dataset):
    '''
    Data generator for training. Requires a list of possible classes

    Options:
        - file_col: column name containing full file paths
        - label_col: column name containing class labels
        - crop: if true, dynamically crop
        - resize: dynamically resize images to target (square)
    '''
    def __init__(self, x, classes, file_col='FilePath', label_col='species', crop=True, resize=299):
        self.x = x
        self.resize = int(resize)
        self.file_col = file_col
        self.label_col = label_col
        self.buffer = 0
        self.crop = crop
        self.transform = Compose([
            # add augmentations
            RandomHorizontalFlip(p=0.5),
            Resize((self.resize, self.resize)),
            ToTensor(),
        ])
        self.categories = dict([[c, idx] for idx, c in list(enumerate(classes))])

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        image_name = self.x.loc[idx, self.file_col]
        label = self.categories[self.x.loc[idx, self.label_col]]

        try:
            img = Image.open(image_name).convert('RGB')
        except OSError:
            print("File error", image_name)
            del self.x.iloc[idx]
            return self.__getitem__(idx)

        if self.crop:
            width, height = img.size

            bbox1 = self.x['bbox1'].iloc[idx]
            bbox2 = self.x['bbox2'].iloc[idx]
            bbox3 = self.x['bbox3'].iloc[idx]
            bbox4 = self.x['bbox4'].iloc[idx]

            left = width * bbox1
            top = height * bbox2
            right = width * (bbox1 + bbox3)
            bottom = height * (bbox2 + bbox4)

            left = max(0, int(left) - self.buffer)
            top = max(0, int(top) - self.buffer)
            right = min(width, int(right) + self.buffer)
            bottom = min(height, int(bottom) + self.buffer)
            img = img.crop((left, top, right, bottom))

        img_tensor = self.transform(img)

        return img_tensor, label, image_name


'''
class TFGenerator(Sequence):

    Generator for TensorFlow/Keras models

    Does not require a dataloader, self-batches

    Options:
        - file_col: column name containing full file paths
        - label_col: column name containing class labels
        - crop: if true, dynamically crop
        - resize: dynamically resize images to target (square)
        - buffer: add buffer to crops
        - batch_size: batch size for loading

    def __init__(self, x, file_col='file', crop=True, resize=299, buffer=0, batch_size=32):
        self.x = x
        self.file_col = file_col
        self.crop = crop
        self.resize = int(resize)
        self.buffer = buffer
        self.batch_size = int(batch_size)

    def __len__(self):
        return int(np.ceil(len(self.x.index) / float(self.batch_size)))

    def __getitem__(self, idx):
        imgarray = []
        for i in range(min(len(self.x.index), idx * self.batch_size),
                       min(len(self.x.index), (idx + 1) * self.batch_size)):
            try:
                file = self.x[self.file_col].iloc[i]
                img = Image.open(file)
            except OSError:
                continue

            if self.crop:
                width, height = img.size
                bbox1 = self.x['bbox1'].iloc[i]
                bbox2 = self.x['bbox2'].iloc[i]
                bbox3 = self.x['bbox3'].iloc[i]
                bbox4 = self.x['bbox4'].iloc[i]

                left = width * bbox1
                top = height * bbox2
                right = width * (bbox1 + bbox3)
                bottom = height * (bbox2 + bbox4)

                left = max(0, left - self.buffer)
                top = max(0, top - self.buffer)
                right = min(width, right + self.buffer)
                bottom = min(height, bottom + self.buffer)
                img = img.crop((left, top, right, bottom))

            img = img.resize((self.resize, self.resize))
            img = tf.keras.utils.img_to_array(img)
            imgarray.append(img)

        return np.asarray(imgarray)
'''


def train_dataloader(manifest, classes, batch_size=1, workers=1, file_col="FilePath", crop=False):
    '''
        Loads a dataset for training and wraps it in a
        PyTorch DataLoader object. Shuffles the data before loading.

        Args:
            - manifest (DataFrame): data to be fed into the model
            - classes (dict): all possible class labels
            - batch_size (int): size of each batch
            - workers (int): number of processes to handle the data
            - file_col: column name containing full file paths
            - crop: if true, dynamically crop

        Returns:
            dataloader object
    '''
    dataset_instance = TrainGenerator(manifest, classes, file_col, crop=crop)

    dataLoader = DataLoader(
            dataset=dataset_instance,
            batch_size=batch_size,
            shuffle=True,
            num_workers=workers
        )
    return dataLoader


def manifest_dataloader(manifest, batch_size=1, workers=1, file_col="file", crop=False, resize=[299, 299], standardize=True):
    '''
        Loads a dataset and wraps it in a PyTorch DataLoader object.
        Always dynamically crops

        Args:
            - manifest (DataFrame): data to be fed into the model
            - batch_size (int): size of each batch
            - workers (int): number of processes to handle the data
            - file_col: column name containing full file paths

        Returns:
            dataloader object
    '''
    if crop is True and not any(manifest.columns.isin(["bbox1"])):
        crop = False

    # default values file_col='file', resize=299
    dataset_instance = ImageGenerator(manifest, file_col=file_col, crop=crop, resize=resize, standardize=standardize)

    dataLoader = DataLoader(
            dataset=dataset_instance,
            batch_size=batch_size,
            shuffle=False,
            num_workers=workers
        )
    return dataLoader
