# Tekton CD Pipeline for Wishlist Service

This directory contains the OpenShift Pipelines resources for the Wishlist
service CD flow.

## Files

- `workspace.yaml`: PersistentVolumeClaim used by the pipeline workspace.
- `tasks.yaml`: Custom tasks for unit tests, linting, the Buildah image build, and deploy.
- `pipeline.yaml`: Pipeline orchestration for clone, test, lint, image build, and deploy.

## Pipeline Flow

```text
git-clone
  |-- unit-tests --|
  |-- lint ------- |--> buildah --> deploy
```

The `buildah` pipeline task runs only after both `unit-tests` and `lint`
complete successfully. The `deploy` task runs last and rolls out the exact
image digest built by Buildah to the `wishlists` deployment.

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
`deploy` task starts after `buildah`, then completes successfully.
