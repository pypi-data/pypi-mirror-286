![Inferno Header](./misc/assets/inferno-header-github.png)

## About
Inferno is an extensible library for simulating spiking neural networks. It is built on top of [PyTorch](https://github.com/pytorch/pytorch) and is designed with machine learning practitioners in mind. This project is still an early release and features may be subject to change.

## Installation
### With PyTorch 2.2.2 (CPU Only)
#### Pip
```
pip install inferno[torch]
```

### Without PyTorch
#### Pip
```
pip install inferno
```
*Note: Inferno is still dependent upon PyTorch and a version of PyTorch must be installed.*

### With PyTorch 2.2.2 and CUDA 12 (Linux and Windows Only)
#### Pip
```
pip install inferno
pip install torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cu121
```

### With PyTorch 2.2.2 and CUDA 11 (Linux and Windows Only)
#### Pip
```
pip install inferno
pip install torch==2.2.2 torchvision==0.17.2 --index-url https://download.pytorch.org/whl/cu118
```
