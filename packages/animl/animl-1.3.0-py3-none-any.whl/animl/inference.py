"""
    Inference Module

    Provides functions for species classifier inference

    @ Kyra Swanson 2023
"""
import torch
import pandas as pd
import numpy as np
from tqdm import tqdm
from . import generator, file_management


def softmax(x):
    '''
    Helper function to softmax
    '''
    return np.exp(x)/np.sum(np.exp(x), axis=1, keepdims=True)


def tensor_to_onnx(tensor):
    '''
    Helper function for onnx, shifts dims to BxHxWxC
    '''
    tensor = tensor.permute(0, 2, 3, 1)  # reorder BxCxHxW to BxHxWxC
    tensor = tensor.cpu().detach().numpy()
    # tensor = np.asarray(tensor, dtype='float32')
    return tensor


def predict_species(detections, model, classes, device='cpu', out_file=None,
                    file_col='Frame', crop=True, resize=299, standardize=True,
                    batch_size=1, workers=1, channel_last=False, raw=False):
    """
    Predict species using classifier model

    Args
        - detections (pd.DataFrame): dataframe of (animal) detections
        - model: preloaded classifier model
        - classes: preloaded class list
        - device (str): specify to run model on cpu or gpu, default to cpu
        - out_file (str): path to save prediction results to
        - file_col (str): column name containing file paths
        - resize (int): image input size
        - batch_size (int): data generator batch size
        - workers (int): number of cores
        - channel_last (bool): swap dims for onnx models trained with BHWC order
        - raw (bool): return raw logits instead of applying labels

    Returns
        - detections (pd.DataFrame): MD detections with classifier prediction and confidence
    """
    if file_management.check_file(out_file):
        return file_management.load_data(out_file)

    if isinstance(detections, pd.DataFrame):
        # initialize lists
        
        detections = detections.reset_index(drop=True)
        predictions = []
        probabilities = []
        if raw:
            raw_output = []

        dataset = generator.manifest_dataloader(detections, file_col=file_col,
                                                crop=crop, resize=resize, standardize=standardize,
                                                batch_size=batch_size, workers=workers)

        with torch.no_grad():
            for _, batch in tqdm(enumerate(dataset)):
                # pytorch
                if model.framework == "pytorch" or model.framework == "EfficientNet":
                    data = batch[0]
                    data = data.to(device)
                    output = model(data)
                    if raw:
                        raw_output.extend(output.cpu().detach().numpy())

                    labels = torch.argmax(output, dim=1).cpu().detach().numpy()
                    pred = classes['Code'].values[labels]
                    predictions.extend(pred)

                    probs = torch.max(torch.nn.functional.softmax(output, dim=1), 1)[0]
                    probabilities.extend(probs.cpu().detach().numpy())

                # onnx
                elif model.framework == "onnx":
                    device = "cpu"

                    data = batch[0]

                    # TODO: RUN ON GPU
                    if channel_last:
                        inputs = {model.get_inputs()[0].name: tensor_to_onnx(data)}
                    else:
                        inputs = {model.get_inputs()[0].name: data.cpu().detach().numpy()}

                    output = model.run(None, inputs)[0]
                    if raw:
                        raw_output.extend(output)

                    labels = np.argmax(output, axis=1)
                    pred = classes['Code'].values[labels]
                    predictions.extend(pred)

                    # onnx_probs = np.max(softmax(output),axis=1)
                    onnx_probs = np.max(output, axis=1)
                    probabilities.extend(onnx_probs)

                else:
                    raise AssertionError("Model architechture not supported.")

            detections['prediction'] = predictions
            detections['confidence'] = probabilities

    else:
        raise AssertionError("Input must be a data frame of crops or vector of file names.")

    if out_file:
        file_management.save_data(detections, out_file)

    if raw:
        return np.vstack(raw_output)
    else:
        return detections
