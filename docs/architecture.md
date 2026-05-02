# PowerTune Internal Architecture

This document defines the strict boundaries and data flow of the PowerTune platform. Our architecture is designed to guarantee safe, transactional execution of system optimizations.

## 🏗️ Layered Architecture

```mermaid
graph TD
    CLI[CLI Dispatcher Layer] --> |Routes Commands| Core[Core Execution Engine]
    CLI --> |Triggers Analysis| Diag[Diagnostics Engine]
    
    Core --> |Parses| Config[YAML Configuration DSL]
    Core --> |Requests Snapshot| Safe[Safety & Rollback Framework]
    Core --> |Delegates| Opt[Optimization Handlers]
    
    Opt --> |Applies| OS[Win32 API / OS Interfaces]
    Diag --> |Reads WMI/ETW| OS
    
    Safe --> |Reads/Writes| SnapDB[(Snapshot Store)]
```

### 1. CLI Dispatcher Layer (`powertune.ps1`)
The user-facing router. It handles argument parsing, basic privilege checking (UAC), and vendor hardware detection. It is deliberately kept lightweight.

### 2. Diagnostics Engine (`analyzers/`)
A collection of Python-based read-only probes. 
- **Rule**: Analyzers must never mutate state.
- **Rule**: Analyzers must output structured data (or strict JSON) for downstream consumption.

### 3. Core Execution Engine (`core/engine.py`)
The heart of the platform. It translates declarative YAML configurations into Object-Oriented Command classes.
- Implements the **Transaction-Based Optimization** model:
  `Backup -> Validate -> Apply -> Verify -> Commit`
- Catches exceptions and triggers automatic failure recovery.

### 4. Safety & Rollback Framework (`rollback/`)
Guarantees absolute system reversibility.
- Takes binary/hexadecimal snapshots of ACPI/Processor states before any optimization layer is invoked.

### 5. Optimization Handlers (`engine.py` Tweak Registry)
Specific, isolated classes (e.g., `CpuMinStateTweak`, `ServiceDisableTweak`) that map directly to exact Win32 subsystem calls. 
- Enforced by the **Intent Firewall**: Blocks hardcoded critical targets (e.g., Windows Defender) from being touched.
