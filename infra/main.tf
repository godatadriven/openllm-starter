provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_compute_instance" "default" {
  name         = "${lower(replace(var.author, " ", "-"))}-instance"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = var.disk_image
    }
  }

  metadata = {
    install-nvidia-driver = "True"
  }

  guest_accelerator {
    type  = var.gpu_type
    count = 1
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  scheduling {
    on_host_maintenance = "TERMINATE"
    automatic_restart   = false
  }

  metadata_startup_script = file("startup.sh")
}
