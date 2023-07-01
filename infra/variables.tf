variable "author" {
  description = "Your name"
  type        = string
}

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west4"
}

variable "zone" {
  description = "The GCP zone"
  type        = string
  default     = "europe-west4-a"
}

variable "machine_type" {
  description = "The VM instance type"
  type        = string
  default     = "n1-standard-8"
}

variable "gpu_type" {
  description = "The GPU type"
  type        = string
  default     = "nvidia-tesla-v100"
}

variable "disk_image" {
  description = "The disk image for the VM"
  type        = string
  default     = "projects/deeplearning-platform-release/global/images/family/common-cu113-notebooks-debian-11-py310"
}
