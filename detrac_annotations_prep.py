import xml.etree.ElementTree as ET
from pathlib import Path
import json
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='Transform DETRAC XML annotations to VOC json format.'
    )
parser.add_argument("--xml_dir", dest="xml_dir",
                    help="Directory containing the XML files",
                    default='train_annotations_xml', type = str)
parser.add_argument("--image_dir", dest="image_dir",
                    help="Directory containing the images",
                    default = 'train_images', type = str)
parser.add_argument("--out_dir", dest="out_dir",
                    help="Where to write .json file",
                    default=".", type = str)

args = parser.parse_args()

classes = ['car', 'bus', 'van', 'others']
categories = [{'id':id, 'name':cat} for id,cat in enumerate(classes)]
cat2id = {elem['name']:elem['id'] for elem in categories}

IMG_PTH = Path(args.image_dir)
train_names = [x.parent.name + '/' + x.name for x in IMG_PTH.glob('*/*.jpg')]
images = [{'file_name':name, 'id':id} for id,name in enumerate(train_names)]
im2id = {elem['file_name']:elem['id'] for elem in images}

annotations=[]
ANNO_PTH = Path(args.xml_dir)

file_iter = list(ANNO_PTH.iterdir())
for fanno in tqdm(file_iter, 'Parsing .xml files'):
    tree = ET.parse(fanno)
    root = tree.getroot()
    for frame in root.iter('frame'):
        frame_n = int(frame.attrib['num'])
        im_name = f'{root.attrib["name"]}/img{frame_n:05}.jpg'
        for target in frame.iter('target'):
            label = target.find('attribute').attrib['vehicle_type']
            bb = [int(float(x)) for x in target.find('box').attrib.values()]
            annotations.append({'bbox': bb,
                                'category_id': cat2id[label],
                                'image_id': im2id[im_name]})


trn_j = {'images': images, 'annotations': annotations, 'categories': categories}

print('writing .json\n')
with open(Path(args.out_dir)/'detrac_train.json', 'w') as fp:
    json.dump(trn_j, fp)
