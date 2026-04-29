# Tekton CD Pipeline for Wishlist Service

This directory contains the OpenShift Pipelines resources for the Wishlist
service CD flow.

## Files

- `workspace.yaml`: PersistentVolumeClaim used by the pipeline workspace.
- `tasks.yaml`: Custom tasks for unit tests, linting, the Buildah image build, deploy, and BDD tests.
- `pipeline.yaml`: Pipeline orchestration for clone, test, lint, image build, deploy, and BDD tests.

## Pipeline Flow

```text
git-clone
  |-- unit-tests --|
  |-- lint ------- |--> buildah --> deploy --> behave
```

The `buildah` pipeline task runs only after both `unit-tests` and `lint`
complete successfully. The `deploy` task rolls out the exact
image digest built by Buildah to the `wishlists` deployment. The `behave` task
runs against that deployed service as the BDD verification gate.

## Pipeline Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `GIT_REPO` | Git repository URL to clone | Required |
| `GIT_REF` | Branch, tag, or ref to build | `master` |
| `IMAGE` | Base image used by the lint task | `python:3.12-slim` |
| `REGISTRY` | Image registry host | `image-registry.openshift-image-registry.svc:5000` |
| `IMAGE_NAME` | Image stream name to build and push | `wishlist-service` |
| `IMAGE_TAG` | Image tag to build and push | `latest` |
| `DOCKERFILE` | Dockerfile path | `./Dockerfile` |
| `CONTEXT` | Build context path | `.` |
| `TLSVERIFY` | Verify TLS when pushing to the image registry | `false` |
| `FORMAT` | Image manifest format | `docker` |
| `STORAGE_DRIVER` | Buildah storage driver | `vfs` |
| `DEPLOYER_IMAGE` | OpenShift CLI image used by the deploy task | `quay.io/openshift/origin-cli:4.18` |
| `BEHAVE_IMAGE` | Image used to run Behave and Selenium BDD tests | `quay.io/rofrano/pipeline-selenium:sp26` |
| `BASE_URL` | Base URL of the deployed Wishlist service UI | `http://wishlists` |
| `WAIT_SECONDS` | Seconds Selenium should wait for UI elements | `30` |
| `DRIVER` | Browser driver used by Selenium | `chrome` |

The Buildah task runs as a non-root user with user namespaces and `vfs` storage.
This avoids requiring the `pipeline` service account to run privileged TaskRun
pods in OpenShift.

## Apply Resources

```bash
kubectl apply -f .tekton/workspace.yaml
kubectl apply -f .tekton/tasks.yaml
kubectl apply -f .tekton/pipeline.yaml
```

After starting a PipelineRun in the OpenShift console, verify that the
`behave` task starts after `deploy`, then completes successfully.
