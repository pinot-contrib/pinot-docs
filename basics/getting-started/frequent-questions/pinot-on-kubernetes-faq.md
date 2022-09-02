# Pinot On Kubernetes FAQ

## How to increase server disk size on AWS

Below is an example of AWS EKS.

#### **1. Update Storage Class**

In the K8s cluster, check the storage class: in AWS, it should be gp2.

![](https://lh6.googleusercontent.com/-\_s9xgJoO\_jchVj0n424Phq8LZFLbkvlrEix\_XvHpHeT6fugJeZbq7yzuwrLs\_US9qqFGJeN2OJr2XeHLd4p6rDQ1BXaIkIpcNw3404AQ7JQUpenu\_et83jra9BLBedTbc7kE2LY)

Then update StorageClass to ensure:

```
allowVolumeExpansion: true
```

Once StorageClass is updated, it should be like:

![](https://lh6.googleusercontent.com/aYF44E1KGU6dFoM3E9M\_lOSzsJ7gsCLy4oL0EJvfKMpMS0AdLOuL0dx58dcmiXCPcODgV285qrjkEg4laIT9XCNd1HoLGJRkGmsQI8lQRpzvlpwcpsLr6EDSSmhT3iLmQG0dccIU)

#### **2. Update PVC**

Once the storage class is updated, then we can update PVC for the server disk size.

Now we want to double the disk size for pinot-server-3.

Below is an example of current disks:

![](https://lh3.googleusercontent.com/s3tBb8hyQBWKwQ-fc3p4EjP1rBsScauHCGlCTU5T9uvGIZ53\_i7RyRMv8NgcjviUkDztXytJ9LPExmvCxnz\_rcEdIhI\_B79VQoGD12uwLxjYeHnogiDdPl9PFcTs1MNK47ByY0EW)

Below is the output of **data-pinot-server-3**

![PVC data-pinot-server-3](https://lh4.googleusercontent.com/yyIaKpAK5xOjbnw3zWKMhi5ybamZxppPKdzwVCsowZuKEPqE8sT5MpssVpZzAdxTNw-2D5u08bsLUIYgdmkwJRzOxzex96lkNq9e\_0tTyNcFzP3Z5zs0arQW0IfZtXnScL2\_yqhf)

Now, let's change the PVC size to 2T by editing the server PVC.

```
kubectl edit pvc data-pinot-server-3 -n pinot
```

Once updated, the spec's PVC size is updated to 2T, but the status's PVC size is still 1T.

![](https://lh4.googleusercontent.com/OBIEE2GFsUKNa\_bInkrjjMh1fouEsdd3U\_S8TiVsFymcAAH7WXBxxPyz\_9zEFfTRrPbQm0ComaxLeIOa9NIcggIWMjBnv5swR6UfBMErbWp7KG64GcjO03atsfkVrUGO7dwaw50B)

#### **3. Restart pod to let it reflect**

Restart pinot-server-3 pod:

![](https://lh5.googleusercontent.com/uglBVfhh1\_dNF1bVrbpAsWQwbB0qZ34X3MgTMBVa5BIDxZg6UgQX6OO3z-YQrE4asnSBHWruiyPhI3s6\_u4OfBZjicGttqhe4hcC30yVLaS5mXlkOsZWIjFJVcxSfpLSxv2\_BwFK)

Recheck PVC size:

![](https://lh4.googleusercontent.com/GNyz66IhVZFpW4RTxGWxGCAty716x1joQxXVCX-9T5BBUf3FqHNFA1VRjXjYgNjUH6bv3YmCewJgJpiA\_cOGB8nY8O9jp-\_J\_D40uYPZbRL9PgPT8JW2di9\_TYs8UW3Lfvtsz62b)

![](https://lh6.googleusercontent.com/QXkSPfwoxnVD2HOkyMlbvlI\_2xXL7u1VIWZO9MZrKu4S5hCTXrH0vqVNoXAkQmB\_B1rS7SoWWZvjk-giA1LZEwyLhI67myrQhYVMsexegVMecFQ1s5SZiyQJZNP0uioqo2nXh6Xh)

![](https://lh5.googleusercontent.com/SdanllIsXUnK6DedaxxhaJ1rvpn6vS5lJg4YSDmi-wLFnfZHzwqMpMfeYR-RE6CNUbkSA2UvNjQdz8PuwOGSlyqDVvK2HAqsDS7JX1brN31sTqGkIEZGFGWU\_rwyz4pz-nNF-Ss3)
