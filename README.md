# Open LLM Kickstarter

This repo aims to help you spin up resources and get started with open source LLMs.

It contains:

- Infra to provision a GPU instance on GCP, as many LLMs are too big to run on a CPU
- Instructions to install basic requirements
- Kickstarter notebook for loading and running open source LLMs

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)

## Setup and clean up

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
   - Optionally set other variables (see `variables.tf`)
3. Initialize terraform: `terraform init`
4. Check the plan with: `terraform plan`
5. Spin up the infra: `terraform apply`
6. A GPU instance should now be ready for you. You should be able to see it here: <br>https://console.cloud.google.com/compute/instances?project={project}

> **Note:** The instance we provision is a `n1-standard-8` with a `NVIDIA Tesla V100` GPU. This costs about €2.30 per hour. It's configured to stop after 1 hour of idle time, but please be mindful of the costs, and still shut it down manually if you're not using it. You can change the compute type in `variables.tf`, and find more [pricing info here](https://cloud.google.com/compute/vm-instance-pricing).

### 3. Connecting to the instance

1. Configure ssh for the compute instance (if it doesn't work, try again)

```bash
gcloud compute config-ssh
```

2. Connect with the instance as prompted

```bash
ssh {author}-instance.{zone}.{project}
```

3. In VSCode, you can also connect to the instance by:
   1. Opening the command palette (Command+Shift+P)
   2. Select "Remote-SSH: Connect to Host..."
   3. Select your compute instance `{author}-instance.{zone}.{project}`

## 4. Clone this repo on your VM

```bash
git clone ...
```

## 5. Setup the environment

1. Create a virtual environment of your choice: 
   1. A new conda environment: `conda create --name {env_name} --clone base`
   2. A python venv: `python -m venv .venv`

2. And activate it:
   1. Conda: `conda activate {env_name}`
   2. Venv: `source .venv/bin/activate`

3. Install the requirements

```bash
pip install -r requirements.txt
```

4. Install some extensions (if you're using VSCode)

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension github.copilot  # optional
```

> **Note:** There are probably more elegant ways to manage the dependencies, but I've struggled to get it to work smoothly on GPUs. So for now, this is the easiest way I've found.

## 6. Run the kickstarter notebook

1. Open `llms.ipynb`
2. Select the `{env_name}` kernel
3. Have fun!

## 7. Cleaning up

1. The instance is configured to stop after 1 hour of inactivity. But you can also stop it manually here: <br>https://console.cloud.google.com/compute/instances?project={project}

2. When you fully want to clean up, run (on your local machine):

```bash
terraform destroy
```

> **Note:** When deleting the instance with `terraform destroy`, your data will be lost. So make sure to save your work before doing so.
