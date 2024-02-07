.PHONY: all setup_python create_venv install_packages prepare_lambda_layer upload_to_s3

# Variables
PYTHON_VERSION=3.11.x  # Specify the exact Python version
VENV_PATH=~/lambda-layer
LAYER_ZIP=my-python-layer.zip
S3_BUCKET=s3://instabots-lambdalayers/

all: setup_python create_venv install_packages prepare_lambda_layer upload_to_s3

setup_python:
    sudo yum groupinstall -y "Development Tools"
    sudo yum install -y openssl-devel bzip2-devel libffi-devel
    wget https://www.python.org/ftp/python/$(PYTHON_VERSION)/Python-$(PYTHON_VERSION).tgz
    tar xzf Python-$(PYTHON_VERSION).tgz
    cd Python-$(PYTHON_VERSION) && ./configure --enable-optimizations --with-ensurepip=install && make && sudo make altinstall

create_venv:
    python3.11 -m venv $(VENV_PATH)
    source $(VENV_PATH)/bin/activate

install_packages:
    source $(VENV_PATH)/bin/activate && pip install -r requirements.txt  # Assume you have a requirements.txt file

prepare_lambda_layer:
    mkdir -p ~/python
    cp -r $(VENV_PATH)/lib/python3.11/site-packages/* ~/python/
    cd ~ && zip -r $(LAYER_ZIP) python/

upload_to_s3:
    aws s3 cp $(LAYER_ZIP) $(S3_BUCKET)

