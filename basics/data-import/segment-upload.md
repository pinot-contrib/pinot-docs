---
description: Upload a table segment in Apache Pinot.
---

# Upload a table segment from an external source

This procedure uploads one or more table segments that have been stored as binary files outside of Apache Pinot. This means that the data source is not configured in your [table configuration](../../configuration-reference/table.md).

You have two options. Use the Pinot Admin script if your data is on a local host or use the Pinot Controller API for the same use case or when data is on an external host, such as Amazon S3.

## Use the Pinot Admin script to upload segments

To upload segment files to your Pinot server, use:

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

There are two API call version. Use the one that corresponds to your installed version of the Pinot query engine.

The parameters for both versions are the same, as follows:

| Parameter Name | Description                               |
| -------------- | ----------------------------------------- |
| body                           | model, see example |
| tableName                      | name of the table  |
| tableType                      | type of the table  |
| enableParallelPushProtection   | Whether to enable parallel push protection (true/false) |
| allowRefresh                   | Whether to refresh if the segment already exists  |

### v1

To upload a segment, use:

```
POST /segments
```

### v2

To upload a segment, use:

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