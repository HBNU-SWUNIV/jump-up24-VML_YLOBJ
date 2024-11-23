import comet_ml
from ultralytics import YOLO
import torch

comet_ml.login(project_name="comet-yolov8-resize")

for size in [640, 900, 1280, 1600, 1920]:  
  model = YOLO("yolov8n.pt")

  def put_in_eval_mode(trainer, n_layers=22):
    for i, (name, module) in enumerate(trainer.model.named_modules()):
      if name.endswith("bn") and int(name.split('.')[1]) < n_layers:
        module.eval()
        module.track_running_stats = False

  model.add_callback("on_train_epoch_start", put_in_eval_mode)
  model.add_callback("on_pretrain_routine_start", put_in_eval_mode)

  results = model.train(
      data='/content/datasets/yolo_dataset/data.yaml',
      project='yolov8-resize',
      freeze=22,
      epochs=100,
      imgsz=size,
      batch=16
  )
  
  new_state_dict = dict()
  
  for k, v in model.state_dict().items():
    if k.startswith("model.model.22"):
      new_state_dict[k.replace("model.22", "model.23")] = v
  
  torch.save(new_state_dict, "yolov8n_single.pth")

  model_2 = YOLO('ultralytics/cfg/models/v8/yolov8n-transfer.yaml', task="detect").load('yolov8n.pt')
  state_dict = torch.load("yolov8n_single.pth")
  model_2.load_state_dict(state_dict, strict=False)
  model_2.save(f"yolov8n_merged_{size}.pt")
  