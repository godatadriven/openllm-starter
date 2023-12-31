# Open LLM Kickstarter

This repo aims to help you spin up resources and get started with open source LLMs.

It contains:

- Infra to provision a GPU instance on GCP, as many LLMs are too big to run on a CPU
- Instructions to install basic requirements
- Kickstarter notebook for loading and running open source LLMs
- Streamlit app to allow you to chat with your LLM!


<img width="500" alt="image" src="https://github.com/godatadriven/openllm-starter/assets/48921025/165901a8-870b-462a-8014-163104b69120">


## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

## Setup

### 1. Configure GCP CLI

1. Login to GCP

```bash
gcloud auth login
```

2. Select and set your GCP project

```bash
gcloud config set project {project}
```

- You can run the following to find your personal project ID: `gcloud projects list`
- If you don't have a project, you can create a new one: `gcloud projects create {project}`

### 2. Provision GPU instance

1. Open the `/infra` directory
2. Within the `terraform.tfvars` file, set the following variables:
   - `author`: Your name
   - `project`: Your GCP project ID, i.e. `{project}` from above
   - Optionally set other variables (see `variables.tf`) in the `terraform.tfvars` file
3. Initialize terraform: `terraform init`
4. Check the plan with: `terraform plan`
5. Spin up the infra: `terraform apply`
6. A GPU instance should now be ready for you. You should be able to see it here: <br>https://console.cloud.google.com/compute/instances?project={project}

> **Note:** The instance we provision is a `n1-standard-8` with a `NVIDIA Tesla V100` GPU. This costs about €2.30 per hour. It's configured to stop after 1 hour of idle time, but please be mindful of the costs, and still shut it down manually if you're not using it. You can change the compute type in `terraform.tfvars`, and find more [pricing info here](https://cloud.google.com/compute/vm-instance-pricing).

### 3. Connecting to the instance

1. Configure ssh for the compute instance.

```bash
gcloud compute config-ssh
```

> **Note:** It will take a few minutes before the instance is ready to accept ssh connections. Wait a few minutes, and try again if the next step doesn't work.

2. Connect with the instance as prompted

```bash
ssh {author}-instance.{zone}.{project}
```

3. In VSCode, you can also connect to the instance by:
   1. Opening the command palette (Command+Shift+P)
   2. Select "Remote-SSH: Connect to Host..."
   3. Select your compute instance `{author}-instance.{zone}.{project}`

### 4. Clone this repo on your VM

```bash
git clone https://github.com/godatadriven/openllm-starter.git
```
And open the project folder: `cd openllm-starter`

### 5. Setup the environment

1. Create a new conda environment `conda create --name {env_name} python=3.10`
2. And activate it `conda activate {env_name}`
3. Install the requirements

```bash
pip install -r requirements.txt
```

> **Note:** There are probably more elegant ways to manage the dependencies, but I've struggled to get it to work smoothly with conda/poetry and GPUs. So for now, this is the easiest way I've found.

4. Install some dependencies depending on which editor you use:

a. VSCode
```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension github.copilot  # optional
```
b. Jupyter
```bash
pip install notebook
python -m ipykernel install --user  # install the kernel in jupyter
```

### 6. Port forwarding

To make sure we can inspect streamlit apps in a browser on our local machine, we need to forward the ports from the VM to our local machine. To do so, run the following **on your local machine**:

```bash
gcloud compute ssh {author}-instance --project {project} --zone {zone} -- -L 8501:localhost:8501 -L 8888:localhost:8888
```

You can find the author, project, and zone in `terraform.tfvars` or `variables.tf`

## Run some code 🚀

### 1. Run the kickstarter notebook

0. (If you're working with Jupyter) Launch Jupyter with `jupyter notebook`
1. Open `llms.ipynb`
2. Select the `{env_name}` kernel
3. Have fun!

### 2. Run the chat interface app

1. Make sure you've forwarded the ports (see above)

2. Run the app on the instance:

```bash
streamlit run app.py
```

3. Open the app in your browser: http://localhost:8501 
4. Change the `load_model` and `predict` functions (and more) and have fun!

## Clean up

1. The instance is configured to stop after 1 hour of inactivity. But you can also stop it manually here: <br>https://console.cloud.google.com/compute/instances?project={project}

2. When you fully want to clean up, run (on your local machine):

```bash


terraform destroy
```

> **Note:** When deleting the instance with `terraform destroy`, your data will be lost. So make sure to save your work before doing so.


## Extra: Going really big with Falcon 40b

While it becomes increasingly feasible to run your own small (~1 billion param) small models as described above, there are also more and more tutorials becoming available to run and deploy the biggest models of them all.

One example of such a model is the [falcon-40b](https://huggingface.co/tiiuae/falcon-40b), which is among the top 10 performing models in the [open LLM leaderboard]([url](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) at the time of writing. 

To deploy this model in your own (AWS) infrastructure, we recommend to follow the following tutorial: [falcon-40b-accelerate.ipynb](https://github.com/aws/amazon-sagemaker-examples/blob/main/inference/generativeai/llm-workshop/lab10-falcon-40b-and-7b/falcon-40b-accelerate.ipynb)

Provided you have the required quota for provisioning a g5.12xlarge machine (which you can request otherwise), you can deploy this model within 30 minutes by just running the notebook in a Sagemaker instance.

Some useful things to keep in mind:
- deployment takes about 15-30 minutes
- inference takes about 35 seconds, which is not yet ideal
- the g5.12xlarge costs about €5.60 per hour, so make sure to clean up afterwards
