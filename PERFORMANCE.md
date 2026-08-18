## Optimizations Used
- **Asynchronous Tracing:** ETW parsing is offloaded to background threads to prevent GIL locking in Python.
- **SQLite WAL Mode:** Write-Ahead Logging allows the dashboard to read telemetry concurrently while the engine is writing.

## Bottlenecks Avoided
- Avoided polling heavy WMI classes (like Win32_PerfFormattedData) faster than 1-second intervals to prevent CPU overhead from the observer effect.
- Heavy computational tasks (like Modern Standby timeline generation) are lazy-loaded.
