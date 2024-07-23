import os
import json
from cvtk.ml.data import DataClass
from cvtk.ml.mmdet import DataPipeline, Dataset, DataLoader, MMDETCORE, plot_trainlog, draw_outlines, coco


def train(dataclass, train, valid, test, output_weights, batch_size=4, num_workers=8, epoch=10):
    temp_dpath = os.path.splitext(output_weights)[0]

    dataclass = DataClass(dataclass)
    model = MMDETCORE(dataclass, "__TASKARCH__", None, workspace=temp_dpath)

    train_ = DataLoader(
                Dataset(dataclass, train, DataPipeline(is_train=True, with_bbox=True, with_mask=False)),
                phase='train', batch_size=batch_size, num_workers=num_workers)
    valid_ = DataLoader(
                Dataset(dataclass, valid, DataPipeline(is_train=False, with_bbox=True, with_mask=False)),
                phase='valid', batch_size=batch_size, num_workers=num_workers)
    test_ = DataLoader(
                Dataset(dataclass, test, DataPipeline(is_train=False, with_bbox=True, with_mask=False)),
                phase='test', batch_size=batch_size, num_workers=num_workers)
    
    model.train(train_, valid_, test_, epoch=epoch)
    model.save(output_weights)

    plot_trainlog(os.path.splitext(output_weights)[0] + '.train_stats.train.txt',
                  output=os.path.splitext(output_weights)[0] + '.train_stats.train.png')
    plot_trainlog(os.path.splitext(output_weights)[0] + '.train_stats.valid.txt',
                  output=os.path.splitext(output_weights)[0] + '.train_stats.valid.png')    
        

def inference(dataclass, data, model_weights, output, batch_size=4, num_workers=8):
    dataclass = DataClass(dataclass)
    model = MMDETCORE(dataclass, os.path.splitext(model_weights)[0] + '.py', model_weights, workspace=output)

    data = DataLoader(
                Dataset(dataclass, data, DataPipeline()),
                phase='inference', batch_size=batch_size, num_workers=num_workers)
    
    pred_outputs = model.inference(data)

    for im in pred_outputs:
        draw_outlines(im.file_path,
                      os.path.join(output, os.path.basename(im.file_path)),
                      im.annotations)
    with open(os.path.join(output, 'instances.json'), 'w') as fh:
        coco_format = coco(dataclass, pred_outputs)
        json.dump(coco_format, fh, ensure_ascii=False, indent=4)


def _train(args):
    train(args.dataclass, args.train, args.valid, args.test, args.output_weights)

    
def _inference(args):
    inference(args.dataclass, args.data, args.model_weights, args.output)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_train = subparsers.add_parser('train')
    parser_train.add_argument('--dataclass', type=str, required=True)
    parser_train.add_argument('--train', type=str, required=True)
    parser_train.add_argument('--valid', type=str, required=False)
    parser_train.add_argument('--test', type=str, required=False)
    parser_train.add_argument('--output_weights', type=str, required=True)
    parser_train.set_defaults(func=_train)

    parser_inference = subparsers.add_parser('inference')
    parser_inference.add_argument('--dataclass', type=str, required=True)
    parser_inference.add_argument('--data', type=str, required=True)
    parser_inference.add_argument('--model_weights', type=str, required=True)
    parser_inference.add_argument('--output', type=str, required=False)
    parser_inference.set_defaults(func=_inference)

    args = parser.parse_args()
    args.func(args)
    
    
"""
Example Usage:


python __SCRIPTNAME__ train \\
    --dataclass ./data/strawberry/class.txt \\
    --train ./data/strawberry/train/__SAMPLEDATA__.json \\
    --valid ./data/strawberry/valid/__SAMPLEDATA__.json \\
    --test ./data/strawberry/test/__SAMPLEDATA__.json \\
    --output_weights ./output/sb.pth

    
python __SCRIPTNAME__ inference \\
    --dataclass ./data/strawberry/class.txt \\
    --data ./data/strawberry/test/images \\
    --model_weights ./output/sb.pth \\
    --output ./output/pred_results

"""