import typer
import os
import typer
import os
import httpx
from pathlib import Path
from tqdm import tqdm
from rich import print
from common.ai import get_civitai_model_info_by_hash, calculate_file_hash
from typing import Annotated

app = typer.Typer(help="AI utility")

@app.command('info', help='Get model info.')
def get_model_info(path: Annotated[str, typer.Option("--path", "-p", help="Path to the model file")]):
    file_item = Path(path)
    model_info = get_civitai_model_info_by_hash(calculate_file_hash(file_item))
    if model_info is None:
        print("未找到模型信息")
    else:
        print(model_info)
        
@app.command('classify', help='Classify model type.')
def classify_model(path: Annotated[str, typer.Option("--path", "-p", help="Path to the model file")] = os.getcwd(),
                   recursion: Annotated[bool, typer.Option("--recursion", "-r", help="If you want to classify the models in sub folder")] = False,
                   auto_download_preview_file: Annotated[bool, typer.Option("--auto-download-preview-file", "-a", help="Download the preview image automatically")] = False):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for item in filenames:
            file_item = Path(dirpath) / item
            if(file_item.suffix == '.safetensors' or file_item.suffix == '.ckpt'):
                total += 1
        if not recursion:
            dirnames[:] = []  # Skip subdirectories in this git repository
    print(f"共计 {total} 个模型需要被整理。")
    
    progress_bar = tqdm(total=total)
    for dirpath, dirnames, filenames in os.walk(path):
        for item in filenames:
            file_item = Path(dirpath) / item
            if(file_item.suffix == '.safetensors' or file_item.suffix == '.ckpt'):
                file_item = Path(dirpath) / item
                model_hash = calculate_file_hash(file_item)
                model_info = get_civitai_model_info_by_hash(model_hash)
                if model_info == None:
                    print(f'模型{item}在c站上无法找到预览图，可能是对应hash值仍未存储入c站模型hash库')
                    progress_bar.update(1)
                    continue
                # 创建对应模型类型的文件夹
                os.makedirs(f"{file_item.parent}/{model_info['baseModel']}", exist_ok=True)
                file_item.rename(f"{file_item.parent}/{model_info['baseModel']}/{file_item.name}")
                # 找到对应模型文件的预览图片
                preview_file = file_item.with_suffix(".preview.png")
                # 移动图片到对应的文件夹
                if preview_file.exists():
                    preview_file.rename(f"{file_item.parent}/{model_info['baseModel']}/{file_item.stem}.preview.png")
                else:
                    preview_file = file_item.with_suffix(".png")
                    if preview_file.exists():
                        preview_file.rename(f"{file_item.parent}/{model_info['baseModel']}/{file_item.stem}.png")
                    else:
                        if auto_download_preview_file:
                            # get the preview image of model
                            model_preview_image_url = model_info['images'][0]['url']
                            response = httpx.get(model_preview_image_url)
                            preview_path = file_item.with_suffix(".preview.png")
                            if response.status_code == 200:
                                with open(preview_path, "wb") as f:
                                    f.write(response.content)
            progress_bar.update(1)
        if not recursion:
            dirnames[:] = []  # Skip subdirectories in this git repository

@app.command('preview', help='Get model preview image.')
def preview_model(path: Annotated[str, typer.Option("--path", "-p", help="The path to the directory")] = os.getcwd(),
                  recursion: Annotated[bool, typer.Option("--recursion", "-r", help="If you want to git pull for the sub folder")] = False):
    
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for item in filenames:
            file_item = Path(dirpath) / item
            if(file_item.suffix == '.safetensors' or file_item.suffix == '.ckpt'):
                total += 1
        if not recursion:
            dirnames[:] = []  # Skip subdirectories in this git repository
    print(f"获取预览图中，总计 {total} 个模型。")
    
    progress_bar = tqdm(total=total)
    for dirpath, dirnames, filenames in os.walk(path):
        for item in filenames:
            file_item = Path(dirpath) / item
            if(file_item.suffix == '.safetensors' or file_item.suffix == '.ckpt'):
                model_hash = calculate_file_hash(file_item)
                model_info = get_civitai_model_info_by_hash(model_hash)
                if model_info == None:
                    print(f'模型{item}在c站上无法找到预览图，可能是对应hash值仍未存储入c站模型hash库')
                    progress_bar.update(1)
                    continue
                # get the preview image of model
                model_preview_image_url = model_info['images'][0]['url']
                response = httpx.get(model_preview_image_url)
                preview_path = file_item.with_suffix(".preview.png")
                if response.status_code == 200:
                    with open(preview_path, "wb") as f:
                        f.write(response.content)
                progress_bar.update(1)
        if not recursion:
            dirnames[:] = []  # Skip subdirectories in this git repository
