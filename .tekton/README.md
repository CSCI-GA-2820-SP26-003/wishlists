# Tekton CD Pipeline for Wishlist Service

This directory contains Tekton pipeline definitions for continuous delivery (CD) of the Wishlist Service on OpenShift.

## Overview

The Tekton CD pipeline automates the build and deployment process with the following stages:

1. **Clone**: Clones the git repository
2. **Lint** (pylint): Runs Python linting checks
3. **Test**: Executes unit tests with code coverage validation
4. **Build** (buildah): Builds a container image and pushes it to a registry

## Files

- `tasks.yaml`: Defines individual Tekton tasks
  - `clone`: Clones the source code repository
  - `pylint`: Runs linting and code quality checks
  - `test`: Executes unit tests
  - `buildah`: Builds and pushes the container image

- `pipeline.yaml`: Defines the overall pipeline orchestration
  - `wishlist-cd-pipeline`: Main pipeline definition
  - `wishlist-cd-pipeline-run`: Example PipelineRun for manual execution

## Buildah Task Details

The buildah task performs the following:

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| IMAGE | Container image reference | `quay.io/rofrano/wishlist-service:latest` |
| DOCKERFILE | Path to Dockerfile | `./Dockerfile` |
| CONTEXT | Build context directory | `.` |
| TLSVERIFY | Verify TLS on registry | `false` |
| FORMAT | Image format (docker/oci) | `docker` |

### Steps

1. **build**: Uses buildah to build the container image
   - Builds from the specified Dockerfile
   - Applies labels and layers
   - Outputs image in specified format

2. **push**: Pushes the built image to the container registry
   - Uses buildah push
   - Handles TLS verification based on parameters
   - Stores image in remote registry

### Security

- Runs with `privileged: true` to allow container operations
- Uses buildah's stable image for compatibility

## Task Execution Order

```
clone
  ├── lint (pylint) ──┐
  └── test ──────────┴──→ build (buildah)
```

The buildah task runs **after** both `test` and `lint` complete successfully, ensuring code quality before image creation.

## Usage

### Apply to OpenShift

```bash
# Apply tasks
kubectl apply -f .tekton/tasks.yaml

# Apply pipeline
kubectl apply -f .tekton/pipeline.yaml
```

### Trigger Pipeline Run

```bash
# Apply the example PipelineRun
kubectl apply -f .tekton/pipeline.yaml -o jsonpath='{.items[1]}'
```

### View Pipeline Status

```bash
# List pipeline runs
kubectl get pipelineruns

# Watch pipeline run
kubectl describe pipelinerun <run-name>

# Stream logs
tkn pipelinerun logs <run-name> -f
```

## Environment Variables

- `DATABASE_URI`: PostgreSQL connection string for test task

## Acceptance Criteria Validation

✓ **Given**: The "test" and "pylint" tasks are completed
✓ **When**: The buildah task runs
✓ **Then**: On OpenShift UI, completion is verifiable via:
  - PipelineRun status in OpenShift web console
  - Built image available in registry
  - Pipeline execution logs showing buildah steps

## Next Steps

1. Create a Trigger to automatically run the pipeline on git push
2. Configure authentication for private registries
3. Add deployment tasks after image build
4. Implement promotion pipeline for staging/production
