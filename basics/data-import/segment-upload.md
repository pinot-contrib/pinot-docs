---
description: Upload a table segment in Apache Pinot.
---

# Upload a table segment from an external source

This procedure uploads one or more table segments that have been stored as Pinot segment binary files outside of Apache Pinot, such as if you had to close an original Pinot cluster and create a new one.

Choose one of the following:

* If your data is in a location that uses HDFS, create a segment fetcher.
* If your data is on a host where you have SSH access, use the Pinot Admin script or the Pinot Controller API.
* If you data is on an external host, such as an Amazon S3 bucket, use the Pinot Controller API.

Before you upload, do the following:

1. [Create a schema configuration](../../basics/getting-started/pushing-your-data-to-pinot#creating-a-schema) or confirm one exists that matches the segment you want to upload.

1. [Create a table configuration](../../configuration-reference/table.md) or confirm one exists that matches the segment you want to upload.

1. (If needed) Upload the schema and table configs.

## Create a segment fetcher

If the data is in a location using HDFS, you can create a [segment fetcher](../../developers/developers-and-contributors/extending-pinot/segment-fetchers.md), which will push segment files from external systems such as those running Hadoop or Spark. It is possible to [implement your own segment fetcher for other systems](../../developers/developers-and-contributors/extending-pinot/segment-fetchers.md) with an external jar by implementing a class that extends this interface.

## Use the Pinot Admin script to upload segments

Upload segment files to your Pinot server from controller using the Pinot Admin script as follows:

```bash
pinot-admin.sh UploadSegment -controllerHost localhost -controllerPort 9000 -segmentDir /path/to/local/dir -tableName myTable
```

All options should be prefixed with `-` (hyphen)

| Option         | Description                               |
| -------------- | ----------------------------------------- |
| controllerHost | Hostname or IP address of the controller          |
| controllerPort | Port of the controller                    |
| segmentDir     | Local directory containing segment files  |
| tableName      | Name of the table to push the segments into |

## Use the Pinot Controller API to upload segments

There are two API call versions. Use the one that corresponds to your installed version of the Pinot query engine, which is dependent on your Pinot release. Releases from 0.11.0 use the [multi-stage query engine](../../developers/advanced/v2-multi-stage-query-engine.md), which is v2.

Use the API to find your Pinot version, as follows:

```
POST /version
```

This will return the versions of all installed Pinot components and plugins. The Pinot version is called `pinot-distribution` in the list.

The parameters for both versions are the same, as follows:

| Parameter Name | Description                               |
| -------------- | ----------------------------------------- |
| body                           | Model, see example |
| tableName                      | Name of the table  |
| tableType                      | Type of the table  |
| enableParallelPushProtection   | If true, enables parallel push protection; false otherwise. |
| allowRefresh                   | If true, refreshes the existing segment; false otherwise.  |

### v1

Upload a segment files to your Pinot server using the Pinot Controller API and the original API call as follows:

```
POST /segments
```

### v2

Upload a segment files to your Pinot server using the Pinot Controller API and the v2 API call as follows:

```
POST /v2/segments
```

### Expected responses

Either API call will return a JSON response like this one for a successful operation:

```json
{
    "status": "200"
}
```

### Example of `body`

See the [Controller Admin API](../../users/api/pinot-rest-admin-interface.md) for more information.

```json
{
  "contentDisposition": {
    "type": "string",
    "parameters": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "fileName": "string",
    "creationDate": "2023-08-25T12:50:12.437Z",
    "modificationDate": "2023-08-25T12:50:12.437Z",
    "readDate": "2023-08-25T12:50:12.437Z",
    "size": 0
  },
  "entity": {},
  "headers": {
    "additionalProp1": [
      "string"
    ],
    "additionalProp2": [
      "string"
    ],
    "additionalProp3": [
      "string"
    ]
  },
  "mediaType": {
    "type": "string",
    "subtype": "string",
    "parameters": {
      "additionalProp1": "string",
      "additionalProp2": "string",
      "additionalProp3": "string"
    },
    "wildcardType": true,
    "wildcardSubtype": true
  },
  "messageBodyWorkers": {},
  "parent": {
    "contentDisposition": {
      "type": "string",
      "parameters": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
      },
      "fileName": "string",
      "creationDate": "2023-08-25T12:50:12.437Z",
      "modificationDate": "2023-08-25T12:50:12.437Z",
      "readDate": "2023-08-25T12:50:12.437Z",
      "size": 0
    },
    "entity": {},
    "headers": {
      "additionalProp1": [
        "string"
      ],
      "additionalProp2": [
        "string"
      ],
      "additionalProp3": [
        "string"
      ]
    },
    "mediaType": {
      "type": "string",
      "subtype": "string",
      "parameters": {
        "additionalProp1": "string",
        "additionalProp2": "string",
        "additionalProp3": "string"
      },
      "wildcardType": true,
      "wildcardSubtype": true
    },
    "messageBodyWorkers": {},
    "providers": {},
    "bodyParts": [
      {
        "contentDisposition": {
          "type": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "fileName": "string",
          "creationDate": "2023-08-25T12:50:12.437Z",
          "modificationDate": "2023-08-25T12:50:12.437Z",
          "readDate": "2023-08-25T12:50:12.437Z",
          "size": 0
        },
        "entity": {},
        "headers": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "mediaType": {
          "type": "string",
          "subtype": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "wildcardType": true,
          "wildcardSubtype": true
        },
        "messageBodyWorkers": {},
        "providers": {},
        "parameterizedHeaders": {
          "additionalProp1": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "additionalProp2": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "additionalProp3": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ]
        }
      }
    ],
    "parameterizedHeaders": {
      "additionalProp1": [
        {
          "value": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          }
        }
      ],
      "additionalProp2": [
        {
          "value": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          }
        }
      ],
      "additionalProp3": [
        {
          "value": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          }
        }
      ]
    }
  },
  "providers": {},
  "bodyParts": [
    {
      "contentDisposition": {
        "type": "string",
        "parameters": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        },
        "fileName": "string",
        "creationDate": "2023-08-25T12:50:12.437Z",
        "modificationDate": "2023-08-25T12:50:12.437Z",
        "readDate": "2023-08-25T12:50:12.437Z",
        "size": 0
      },
      "entity": {},
      "headers": {
        "additionalProp1": [
          "string"
        ],
        "additionalProp2": [
          "string"
        ],
        "additionalProp3": [
          "string"
        ]
      },
      "mediaType": {
        "type": "string",
        "subtype": "string",
        "parameters": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        },
        "wildcardType": true,
        "wildcardSubtype": true
      },
      "messageBodyWorkers": {},
      "providers": {},
      "parameterizedHeaders": {
        "additionalProp1": [
          {
            "value": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            }
          }
        ],
        "additionalProp2": [
          {
            "value": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            }
          }
        ],
        "additionalProp3": [
          {
            "value": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            }
          }
        ]
      }
    }
  ],
  "fields": {
    "additionalProp1": [
      {
        "contentDisposition": {
          "type": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "fileName": "string",
          "creationDate": "2023-08-25T12:50:12.437Z",
          "modificationDate": "2023-08-25T12:50:12.437Z",
          "readDate": "2023-08-25T12:50:12.437Z",
          "size": 0
        },
        "entity": {},
        "headers": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "mediaType": {
          "type": "string",
          "subtype": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "wildcardType": true,
          "wildcardSubtype": true
        },
        "messageBodyWorkers": {},
        "parent": {
          "contentDisposition": {
            "type": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            },
            "fileName": "string",
            "creationDate": "2023-08-25T12:50:12.437Z",
            "modificationDate": "2023-08-25T12:50:12.437Z",
            "readDate": "2023-08-25T12:50:12.437Z",
            "size": 0
          },
          "entity": {},
          "headers": {
            "additionalProp1": [
              "string"
            ],
            "additionalProp2": [
              "string"
            ],
            "additionalProp3": [
              "string"
            ]
          },
          "mediaType": {
            "type": "string",
            "subtype": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            },
            "wildcardType": true,
            "wildcardSubtype": true
          },
          "messageBodyWorkers": {},
          "providers": {},
          "bodyParts": [
            {
              "contentDisposition": {
                "type": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                },
                "fileName": "string",
                "creationDate": "2023-08-25T12:50:12.437Z",
                "modificationDate": "2023-08-25T12:50:12.437Z",
                "readDate": "2023-08-25T12:50:12.437Z",
                "size": 0
              },
              "entity": {},
              "headers": {
                "additionalProp1": [
                  "string"
                ],
                "additionalProp2": [
                  "string"
                ],
                "additionalProp3": [
                  "string"
                ]
              },
              "mediaType": {
                "type": "string",
                "subtype": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                },
                "wildcardType": true,
                "wildcardSubtype": true
              },
              "messageBodyWorkers": {},
              "providers": {},
              "parameterizedHeaders": {
                "additionalProp1": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ],
                "additionalProp2": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ],
                "additionalProp3": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ]
              }
            }
          ],
          "parameterizedHeaders": {
            "additionalProp1": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ],
            "additionalProp2": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ],
            "additionalProp3": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ]
          }
        },
        "providers": {},
        "name": "string",
        "value": "string",
        "simple": true,
        "formDataContentDisposition": {
          "type": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "fileName": "string",
          "creationDate": "2023-08-25T12:50:12.437Z",
          "modificationDate": "2023-08-25T12:50:12.437Z",
          "readDate": "2023-08-25T12:50:12.437Z",
          "size": 0,
          "name": "string"
        },
        "parameterizedHeaders": {
          "additionalProp1": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "additionalProp2": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "additionalProp3": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ]
        }
      }
    ],
    "additionalProp2": [
      {
        "contentDisposition": {
          "type": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "fileName": "string",
          "creationDate": "2023-08-25T12:50:12.437Z",
          "modificationDate": "2023-08-25T12:50:12.437Z",
          "readDate": "2023-08-25T12:50:12.437Z",
          "size": 0
        },
        "entity": {},
        "headers": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "mediaType": {
          "type": "string",
          "subtype": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "wildcardType": true,
          "wildcardSubtype": true
        },
        "messageBodyWorkers": {},
        "parent": {
          "contentDisposition": {
            "type": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            },
            "fileName": "string",
            "creationDate": "2023-08-25T12:50:12.437Z",
            "modificationDate": "2023-08-25T12:50:12.437Z",
            "readDate": "2023-08-25T12:50:12.437Z",
            "size": 0
          },
          "entity": {},
          "headers": {
            "additionalProp1": [
              "string"
            ],
            "additionalProp2": [
              "string"
            ],
            "additionalProp3": [
              "string"
            ]
          },
          "mediaType": {
            "type": "string",
            "subtype": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            },
            "wildcardType": true,
            "wildcardSubtype": true
          },
          "messageBodyWorkers": {},
          "providers": {},
          "bodyParts": [
            {
              "contentDisposition": {
                "type": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                },
                "fileName": "string",
                "creationDate": "2023-08-25T12:50:12.437Z",
                "modificationDate": "2023-08-25T12:50:12.437Z",
                "readDate": "2023-08-25T12:50:12.437Z",
                "size": 0
              },
              "entity": {},
              "headers": {
                "additionalProp1": [
                  "string"
                ],
                "additionalProp2": [
                  "string"
                ],
                "additionalProp3": [
                  "string"
                ]
              },
              "mediaType": {
                "type": "string",
                "subtype": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                },
                "wildcardType": true,
                "wildcardSubtype": true
              },
              "messageBodyWorkers": {},
              "providers": {},
              "parameterizedHeaders": {
                "additionalProp1": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ],
                "additionalProp2": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ],
                "additionalProp3": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ]
              }
            }
          ],
          "parameterizedHeaders": {
            "additionalProp1": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ],
            "additionalProp2": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ],
            "additionalProp3": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ]
          }
        },
        "providers": {},
        "name": "string",
        "value": "string",
        "simple": true,
        "formDataContentDisposition": {
          "type": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "fileName": "string",
          "creationDate": "2023-08-25T12:50:12.437Z",
          "modificationDate": "2023-08-25T12:50:12.437Z",
          "readDate": "2023-08-25T12:50:12.437Z",
          "size": 0,
          "name": "string"
        },
        "parameterizedHeaders": {
          "additionalProp1": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "additionalProp2": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "additionalProp3": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ]
        }
      }
    ],
    "additionalProp3": [
      {
        "contentDisposition": {
          "type": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "fileName": "string",
          "creationDate": "2023-08-25T12:50:12.437Z",
          "modificationDate": "2023-08-25T12:50:12.437Z",
          "readDate": "2023-08-25T12:50:12.437Z",
          "size": 0
        },
        "entity": {},
        "headers": {
          "additionalProp1": [
            "string"
          ],
          "additionalProp2": [
            "string"
          ],
          "additionalProp3": [
            "string"
          ]
        },
        "mediaType": {
          "type": "string",
          "subtype": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "wildcardType": true,
          "wildcardSubtype": true
        },
        "messageBodyWorkers": {},
        "parent": {
          "contentDisposition": {
            "type": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            },
            "fileName": "string",
            "creationDate": "2023-08-25T12:50:12.437Z",
            "modificationDate": "2023-08-25T12:50:12.437Z",
            "readDate": "2023-08-25T12:50:12.437Z",
            "size": 0
          },
          "entity": {},
          "headers": {
            "additionalProp1": [
              "string"
            ],
            "additionalProp2": [
              "string"
            ],
            "additionalProp3": [
              "string"
            ]
          },
          "mediaType": {
            "type": "string",
            "subtype": "string",
            "parameters": {
              "additionalProp1": "string",
              "additionalProp2": "string",
              "additionalProp3": "string"
            },
            "wildcardType": true,
            "wildcardSubtype": true
          },
          "messageBodyWorkers": {},
          "providers": {},
          "bodyParts": [
            {
              "contentDisposition": {
                "type": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                },
                "fileName": "string",
                "creationDate": "2023-08-25T12:50:12.437Z",
                "modificationDate": "2023-08-25T12:50:12.437Z",
                "readDate": "2023-08-25T12:50:12.437Z",
                "size": 0
              },
              "entity": {},
              "headers": {
                "additionalProp1": [
                  "string"
                ],
                "additionalProp2": [
                  "string"
                ],
                "additionalProp3": [
                  "string"
                ]
              },
              "mediaType": {
                "type": "string",
                "subtype": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                },
                "wildcardType": true,
                "wildcardSubtype": true
              },
              "messageBodyWorkers": {},
              "providers": {},
              "parameterizedHeaders": {
                "additionalProp1": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ],
                "additionalProp2": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ],
                "additionalProp3": [
                  {
                    "value": "string",
                    "parameters": {
                      "additionalProp1": "string",
                      "additionalProp2": "string",
                      "additionalProp3": "string"
                    }
                  }
                ]
              }
            }
          ],
          "parameterizedHeaders": {
            "additionalProp1": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ],
            "additionalProp2": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ],
            "additionalProp3": [
              {
                "value": "string",
                "parameters": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                }
              }
            ]
          }
        },
        "providers": {},
        "name": "string",
        "value": "string",
        "simple": true,
        "formDataContentDisposition": {
          "type": "string",
          "parameters": {
            "additionalProp1": "string",
            "additionalProp2": "string",
            "additionalProp3": "string"
          },
          "fileName": "string",
          "creationDate": "2023-08-25T12:50:12.437Z",
          "modificationDate": "2023-08-25T12:50:12.437Z",
          "readDate": "2023-08-25T12:50:12.437Z",
          "size": 0,
          "name": "string"
        },
        "parameterizedHeaders": {
          "additionalProp1": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "additionalProp2": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ],
          "additionalProp3": [
            {
              "value": "string",
              "parameters": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string"
              }
            }
          ]
        }
      }
    ]
  },
  "parameterizedHeaders": {
    "additionalProp1": [
      {
        "value": "string",
        "parameters": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        }
      }
    ],
    "additionalProp2": [
      {
        "value": "string",
        "parameters": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        }
      }
    ],
    "additionalProp3": [
      {
        "value": "string",
        "parameters": {
          "additionalProp1": "string",
          "additionalProp2": "string",
          "additionalProp3": "string"
        }
      }
    ]
  }
}
```