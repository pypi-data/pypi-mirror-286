直接把huggingface_hub单个库的所有下载链接，打包输出，
结果如下：
```json
[...,
['https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/resolve/main/vae/diffusion_pytorch_model.fp16.safetensors', ' out=vae/diffusion_pytorch_model.fp16.safetensors']
]
```

## 直接运行源文件

- parse_main函数即可

## pip 安装使用

```shell
pip install .
or 
pip install huggingface_urls
```


```py
from huggingface_urls import parse_main

url = 'https://huggingface.co/RunDiffusion/Juggernaut-XL-v9/tree/main'

print(parse_main(url))
```