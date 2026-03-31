#!/bin/bash

poetry shell

export CMAKE_ARGS="-DGGML_HIPBLAS=on"

pip install --force-reinstall --no-cache-dir --no-binary :all: llama-cpp-python
