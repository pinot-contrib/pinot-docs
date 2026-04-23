# Querying Pinot Using Cursors

Cursors enable clients to fetch large result sets from Pinot in chunks, similar to database cursors. This reduces memory consumption for both the client and server.

## Architecture Overview

Cursor responses are now managed at the **broker level**, with each broker running its own local cleanup scheduled executor. The controller no longer manages cursor response cleanup.

## Configuration

### Broker Cursor Cleanup Configuration

Add these properties to your broker configuration:

- `pinot.broker.response_store.cleanup_interval_ms`: Interval in milliseconds for the broker to clean up expired cursor responses (default: 3600000, i.e., 1 hour)
- `pinot.broker.response_store.max_age_ms`: Maximum age in milliseconds before a cursor response is considered expired

### Example Broker Configuration

```properties
pinot.broker.response_store.cleanup_interval_ms=3600000
pinot.broker.response_store.max_age_ms=604800000
```

## REST API

### Fetch Cursor Response

Fetch the next chunk of results using a cursor ID.

**Endpoint:** `GET /responseStore/{requestId}`

**Query Parameters:**
- `requestId` (required): The cursor/response ID

**Example:**
```bash
curl -X GET "http://localhost:8099/responseStore/my-cursor-id"
```

### Delete a Specific Cursor Response

Delete a specific cursor response by ID.

**Endpoint:** `DELETE /responseStore/{requestId}`

**Example:**
```bash
curl -X DELETE "http://localhost:8099/responseStore/my-cursor-id"
```

### Batch Delete Expired Cursor Responses (NEW)

Delete all cursor responses that have expired by a cutoff time. This is useful for operators who want to manually trigger cleanup instead of waiting for the scheduled cleanup.

**Endpoint:** `DELETE /responseStore/`

**Query Parameters:**
- `expiredBefore` (optional): Epoch millisecond cutoff time. Responses with `expirationTimeMs` at or before this value will be deleted. If omitted, defaults to the current time.

**Example:**
```bash
# Delete all responses expired before current time
curl -X DELETE "http://localhost:8099/responseStore/"

# Delete all responses expired before a specific timestamp (e.g., one hour ago)
curl -X DELETE "http://localhost:8099/responseStore/?expiredBefore=1682083200000"
```

**Response:**
```json
{
  "message": "Deleted 42 expired response(s)."
}
```

## Backward-Incompatible Change

> **WARNING:** As of Apache Pinot version with PR #18203, cursor response cleanup has been moved from the controller to each broker. The controller no longer runs the `ResponseStoreCleaner` periodic task.
>
> **Operational Impact during Rolling Upgrades:**
> - Controllers upgraded first will no longer clean up cursor responses
> - Brokers must be upgraded to the new version to enable their own cleanup
> - Temporary accumulation of expired cursor responses may occur if brokers are not upgraded promptly
> - **Recommendation:** Ensure all brokers are upgraded to the new version shortly after upgrading controllers
> - If manual cleanup is needed during the transition, use the new batch delete API: `DELETE /responseStore/`

## Usage Example: Fetching Large Result Sets with Cursors

```python
import requests
import json

BASE_URL = "http://localhost:8099"

# Execute query and get initial results
response = requests.get(f"{BASE_URL}/query", params={
    "sql": "SELECT * FROM my_table LIMIT 1000000"
})

data = response.json()
cursor_id = data.get("responseId")
results = data.get("resultTable", {}).get("rows", [])

print(f"Cursor ID: {cursor_id}")
print(f"Initial rows: {len(results)}")

# Fetch next chunks using cursor
while cursor_id:
    response = requests.get(f"{BASE_URL}/responseStore/{cursor_id}")
    if response.status_code != 200:
        break
    
    data = response.json()
    results = data.get("rows", [])
    cursor_id = data.get("nextCursorId")
    
    print(f"Fetched {len(results)} more rows")
    # Process results...

# Clean up: delete cursor when done (optional, cleaned up automatically)
# requests.delete(f"{BASE_URL}/responseStore/{cursor_id}")
```

## Related Configuration

See [Pinot Broker Configuration](../../../reference/configuration-reference/broker.md) for a complete list of broker properties.
