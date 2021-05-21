# Pinot Helix Controller Separation

Pinot and Helix controller separation is a super useful feature if there are thousands of Pinot tables within a single Pinot cluster and performance issue started to arise. 
Here is complete design doc: https://cwiki.apache.org/confluence/display/PINOT/Controller+Separation+between+Helix+and+Pinot

In the following section, we'd display how to enable/disable this feature.

## Rollout

Since Release 0.8.0, the resource in Step 1 is enabled by default. So you don't have to turn it one by yourself. But be sure it's `enabled` before proceeding with the following steps.

### Step 1

Make sure that the "RESOURCE_ENABLED" config is set to true in the ZNode "CONFIGS/RESOURCE/leadControllerResource" in your Pinot cluster.
```
{
 "id" : "leadControllerResource",
 "simpleFields" :{ "RESOURCE_ENABLED" : "true" },
 "mapFields" : {},
 "listFields" : {}
}
```

If you want to keep Helix controller and Pinot controller running in the `same` hardware, you can stop at this step. If you want to have these two controllers run in separate hardware, please follow the following steps below.

### Step 2

After verifying everything working fine, we can add 1 or more `Helix-only` controllers to the Pinot cluster, so that they can be the candidates of the Helix cluster leadership.
The below is the config of setting which pinot controller mode you'd like to run on a machine (`DUAL` mode by default):
```
controller.mode=HELIX_ONLY // DUAL, PINOT_ONLY, HELIX_ONLY
```


### Step 3 
Restart all the original `dual` mode controllers to `Pinot-only` mode one by one. After doing so, only Helix-only controller can be Helix leader, and all the Pinot-only controllers only work on Pinot’s workloads. Rollout finished. 

## Rollback

The rollback procedure is exactly the reverse way of rollout plan. Mostly you can stop after the step 2 is finished.