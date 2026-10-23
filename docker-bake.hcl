variable "TAG" {}

group "default" {
    targets = ["app"]
}

target "app" {
    context    = "."
    dockerfile = "Dockerfile"
    platforms  = [
        "linux/amd64",
        // "linux/arm64"
    ]
    args = {
        VERSION_ARG = TAG
    }
    tags = [
    "ghcr.io/theraphael0000/ch.tahm-ken.www-api:latest",
    "ghcr.io/theraphael0000/ch.tahm-ken.www-api:${TAG}"
  ]
    cache_from = ["type=gha"]
    cache_to   = ["type=gha,mode=max"]
}