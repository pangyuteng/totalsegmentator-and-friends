
```
pangyuteng/totalsegmentator:latest
from method `download_pretrained_weights`, locate weights
```

```
docker run -it -v /mnt:/mnt pangyuteng/totalsegmentator:latest bash
python
```

```
import torch
checkpoint_file='/opt/totalsegmentator_weights/nnUNet/3d_fullres/Task251_TotalSegmentator_part1_organs_1139subj/nnUNetTrainerV2_ep4000_nomirror__nnUNetPlansv2.1/fold_0/model_final_checkpoint.model'
m=torch.load(checkpoint_file)
print(m.keys())

dict_keys(['epoch', 'state_dict', 'optimizer_state_dict', 'lr_scheduler_state_dict', 'plot_stuff', 'best_stuff', 'amp_grad_scaler'])


output_folder = '/opt/totalsegmentator_weights/nnUNet/3d_fullres/Task251_TotalSegmentator_part1_organs_1139subj/nnUNetTrainerV2_ep4000_nomirror__nnUNetPlansv2.1/fold_0'

from nnunet.training.network_training.network_trainer import NetworkTrainer
trainer=NetworkTrainer()
trainer.output_folder = output_folder
trainer.load_final_checkpoint()
???



https://github.com/MIC-DKFZ/nnUNet/blob/096639350cee7434abd96987e0c5187a78162804/nnunet/inference/predict.py#L633

-v /cvibraid:/cvibraid -v /radraid:/radraid

docker run -it -w /workdir -v $PWD:/workdir pangyuteng/totalsegmentator:latest bash


/opt/totalsegmentator_weights/nnUNet/3d_fullres/Task251_TotalSegmentator_part1_organs_1139subj/nnUNetTrainerV2_ep4000_nomirror__nnUNetPlansv2.1/fold_0

debug.json  model_final_checkpoint.model  model_final_checkpoint.model.pkl 

from batchgenerators.utilities.file_and_folder_operations import *
expected_num_modalities = load_pickle(join(model, "plans.pkl"))

from nnunet.training.model_restore import load_model_and_checkpoint_files


['num_modalities']





```