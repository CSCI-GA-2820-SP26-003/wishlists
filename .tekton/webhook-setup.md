# GitHub Webhook Setup

This document describes how to configure the GitHub webhook to trigger the CD pipeline automatically when changes are pushed to the `master` branch.

## Prerequisites

Before setting up the webhook, make sure the following resources are applied to your OpenShift cluster:

```bash
oc apply -f .tekton/workspace.yaml
oc apply -f .tekton/tasks.yaml
oc apply -f .tekton/pipeline.yaml
oc apply -f .tekton/triggers.yaml
oc apply -f .tekton/listener-route.yaml
```

## Get the EventListener Route URL

After applying the resources, get the EventListener route URL:

```bash
oc get route el-cd-listener -o jsonpath='{.spec.host}'
```

The URL will look like:
`https://el-cd-listener-<namespace>.apps.<cluster-domain>.com`

## Configure GitHub Webhook

1. Go to the GitHub repository: https://github.com/CSCI-GA-2820-SP26-003/wishlists
2. Click **Settings** → **Webhooks** → **Add webhook**
3. Set **Payload URL** to the EventListener route URL above
4. Set **Content type** to `application/json`
5. Select **Just the push event**
6. Click **Add webhook**

## Verify

Push a commit to `master` or merge a PR — the CD pipeline should trigger automatically in OpenShift.
