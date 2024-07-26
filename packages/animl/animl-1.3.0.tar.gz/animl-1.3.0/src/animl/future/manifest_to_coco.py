import numpy as np
import json
import sys
import argparse
import pandas as pd







def image(row):
    image = {}
    image["license"] = 0
    image["file_name"] = row.FileName
    
    image["height"] = row.height
    image["width"] = row.width
    image["date_captured"] = row.FileModifyDate
    image["gps_lat_captured"]: -1.000000
    image["gps_lon_captured"]: -1.000000
    
    image["id"] = row.fileid
    
    return image

def category(row):
    category = {}
    category["supercategory"] = 'None'
    category["id"] = row.categoryid
    category["name"] = row[2]
    return category

def annotation(row):
    annotation = {}
    area = (row.xmax -row.xmin)*(row.ymax - row.ymin)
    annotation["segmentation"] = []
    annotation["iscrowd"] = 0
    annotation["area"] = area
    annotation["image_id"] = row.fileid

    annotation["bbox"] = [row.xmin, row.ymin, row.xmax -row.xmin,row.ymax-row.ymin ]

    annotation["category_id"] = row.categoryid
    annotation["id"] = row.annid
    return annotation




def wildme_output(manifest):
    images = []
    categories = []
    annotations = []


    data['fileid'] = data['filename'].astype('category').cat.codes
    data['categoryid']= pd.Categorical(data['class'],ordered= True).codes
    data['categoryid'] = data['categoryid']+1
    data['annid'] = data.index


    for row in data.itertuples():
        annotations.append(annotation(row))

    imagedf = data.drop_duplicates(subset=['fileid']).sort_values(by='fileid')
    for row in imagedf.itertuples():
        images.append(image(row))

    catdf = data.drop_duplicates(subset=['categoryid']).sort_values(by='categoryid')
    for row in catdf.itertuples():
        categories.append(category(row))

    wildme_coco = {}
    wildme_coco["info"] = []
    wildme_coco["licenses"] = []
    wildme_coco["images"] = images
    wildme_coco["annotations"] = annotations
    wildme_coco["parts"] = []
    
    json.dump(wildme_coco, open(save_json_path, "w"), indent=4)
    
    

def main():

    parser = argparse.ArgumentParser(
        description='Convert an Animl-formatted .csv results file to MD-formatted .json results file')

    parser.add_argument(
        'input_file',
        type=str,
        help='input .csv file')

    parser.add_argument(
        '--output_file',
        type=str,
        default=None,
        help='output .json file (defaults to input file appened with ".json")')

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    
    path = 'annotations.csv' # the path to the CSV file
    save_json_path = 'traincoco.json'

    manifest = pd.read_csv(args.input_file)



if __name__ == '__main__':
    main()
