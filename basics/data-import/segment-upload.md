---
description: Upload a table segment in Apache Pinot.
---

# Upload a table segment from an external source

This procedure uploads one or more table segments that have been stored as Pinot segment binary files outside of Apache Pinot, such as if you had to close an original Pinot cluster and create a new one.

In this case, your data would not be in your new cluster and the source wouldn't be configured in your [table configuration](../../configuration-reference/table.md).

You have two options. Use the Pinot Admin script if your data is on a host where you have SSH access. You can use the Pinot Controller API for the same use case and also when data is on an external host, such as Amazon S3.

Before you upload, you must first check or do the following:

1. [Create a schema configuration](../../basics/getting-started/pushing-your-data-to-pinot#creating-a-schema) or confirm one exists that matches the segment you will upload.

1. [Create a table configuration](../../configuration-reference/table.md) or confirm one exists that matches the segment you will upload.

1. (If needed) Upload the schema and table configs.

## Use the Pinot Admin script to upload segments

Upload segment files to your Pinot server from controller using the Pinot Admin script as follows:

```bash
pinot-admin.sh UploadSegment -controllerHost localhost -controllerPort 9000 -segmentDir /path/to/local/dir -tableName myTable
```

All the options should be prefixed with `-` (hyphen)

| Option         | Description                               |
| -------------- | ----------------------------------------- |
| controllerHost | hostname or ip of the controller          |
| controllerPort | port of the controller                    |
| segmentDir     | local directory containing segment files  |
| tableName      | name of the table to push the segments in |

## Use the Pinot Controller API to upload segments

There are two API call versions. Use the one that corresponds to your installed version of the Pinot query engine.

The parameters for both versions are the same, as follows:

| Parameter Name | Description                               |
| -------------- | ----------------------------------------- |
| body                           | model, see example |
| tableName                      | name of the table  |
| tableType                      | type of the table  |
| enableParallelPushProtection   | Whether to enable parallel push protection (true/false) |
| allowRefresh                   | Whether to refresh if the segment already exists  |

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