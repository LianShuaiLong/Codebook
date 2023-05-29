import numpy as np
import cv2

from segment_anything import sam_model_registry, SamPredictor

def box_prompt(box, picpath, predictor, outpath='./output'):
    #im = cv2.imread(picpath)
    im = picpath
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

    input_box = np.array(box)
    predictor.set_image(im)
    masks, predictions, _ = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=input_box[None, :],
        multimask_output=True
    )

    highest_prediction = 0
    final_mask = []
    for i,mask in enumerate(masks):
        if predictions[i]>highest_prediction:
            final_mask = mask
            highest_prediction = predictions[i]
    return final_mask, highest_prediction
