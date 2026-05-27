import {
  Activity,
  AlertTriangle,
  ArchiveRestore,
  BatteryCharging,
  Bell,
  BrainCircuit,
  Cpu,
  Database,
  FileText,
  Flame,
  Gauge,
  HardDrive,
  History,
  Laptop,
  Layers3,
  LineChart,
  Lock,
  MemoryStick,
  MonitorCog,
  PanelLeft,
  Play,
  Radar,
  RefreshCw,
  Search,
  Settings,
  ShieldCheck,
  SlidersHorizontal,
  Sparkles,
  Thermometer,
  Zap
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

type Severity = "healthy" | "info" | "warn" | "critical";
type NavKey =
  | "dashboard"
  | "observability"
  | "diagnostics"
  | "telemetry"
  | "battery"
  | "cpu"
  | "gpu"
  | "thermal"
  | "timeline"
  | "optimization"
  | "vendor"
  | "safety"
  | "reports"
  | "advanced"
  | "settings";

type NavItem = {
  key: NavKey;
  label: string;
  icon: LucideIcon;
  group: "Mission" | "Telemetry Data" | "Systems" | "Control";
};

type CardMetric = {
  label: string;
  value: string;
  unit?: string;
  status: string;
  accent?: Severity;
  points?: number[];
};

const navItems: NavItem[] = [
  { key: "dashboard", label: "Dashboard", icon: PanelLeft, group: "Mission" },
  { key: "observability", label: "Observability", icon: Radar, group: "Mission" },
  { key: "diagnostics", label: "Diagnostics", icon: BrainCircuit, group: "Mission" },
  { key: "telemetry", label: "Telemetry", icon: Database, group: "Telemetry Data" },
  { key: "battery", label: "Battery Intelligence", icon: BatteryCharging, group: "Telemetry Data" },
  { key: "cpu", label: "CPU Analytics", icon: Cpu, group: "Telemetry Data" },
  { key: "gpu", label: "GPU Intelligence", icon: MonitorCog, group: "Telemetry Data" },
  { key: "thermal", label: "Thermal Analytics", icon: Thermometer, group: "Telemetry Data" },
  { key: "timeline", label: "Event Timeline", icon: History, group: "Systems" },
  { key: "optimization", label: "Optimization Center", icon: SlidersHorizontal, group: "Systems" },
  { key: "vendor", label: "Vendor Intelligence", icon: Laptop, group: "Systems" },
  { key: "safety", label: "Rollback & Safety", icon: ShieldCheck, group: "Control" },
  { key: "reports", label: "Reports", icon: FileText, group: "Control" },
  { key: "advanced", label: "Advanced Mode", icon: Layers3, group: "Control" },
  { key: "settings", label: "Settings", icon: Settings, group: "Control" }
];

const lineA = [18, 20, 19, 21, 30, 28, 31, 37, 40, 38, 44, 42, 48, 47, 52];
const lineB = [8, 11, 17, 24, 38, 41, 40, 39, 35, 30, 26, 24, 22, 20, 18];
const thermalLine = [42, 43, 46, 49, 47, 45, 40, 41, 38, 35];
const wakeLine = [160, 270, 520, 860, 430, 220, 760, 1210, 590, 210, 990];
const timelineEvents = [
  { time: "13:02", label: "Discord launched", lane: "Applications", x: 16, severity: "info" as Severity },
  { time: "13:03", label: "NVIDIA GPU activated", lane: "Hardware State", x: 27, severity: "warn" as Severity },
  { time: "13:04", label: "Battery drain +3.1W", lane: "Power Draw", x: 42, severity: "warn" as Severity },
  { time: "13:06", label: "Chrome requested 1ms timer", lane: "Timers", x: 56, severity: "critical" as Severity },
  { time: "13:08", label: "Package temp spike", lane: "Thermals", x: 68, severity: "critical" as Severity },
  { time: "13:12", label: "Deep idle restored", lane: "Power State", x: 82, severity: "healthy" as Severity }
];

const eventStream = [
  ["INFO", "Chrome helper released foreground timer state."],
  ["WARN", "Discord activated NVIDIA rendering context."],
  ["INFO", "System idle entered C8 for 4.1s."],
  ["CRIT", "Timer resolution held at 1.0ms by browser process."],
  ["SYS", "Power plan shifted to balanced governor."],
  ["INFO", "Fan curve stabilized under acoustic threshold."],
  ["WARN", "Ambient drain increased above baseline."],
  ["INFO", "Telemetry sample persisted to local history."]
];

const pageCopy: Record<NavKey, { eyebrow: string; title: string; description: string }> = {
  dashboard: {
    eyebrow: "Mission Control",
    title: "Intelligence Dashboard",
    description: "Real-time system diagnostics and optimization posture."
  },
  observability: {
    eyebrow: "Global Observatory",
    title: "Observability Center",
    description: "Live execution telemetry, wakeups, timers, and causality streams."
  },
  diagnostics: {
    eyebrow: "Root-Cause Hub",
    title: "Diagnostics",
    description: "Evidence-based failure explanations with rollback-aware recommendations."
  },
  telemetry: {
    eyebrow: "Raw Channels",
    title: "Telemetry Explorer",
    description: "Advanced CPU, GPU, memory, power, and thermal sample analysis."
  },
  battery: {
    eyebrow: "Battery Lab",
    title: "Battery Intelligence",
    description: "Deep analytics on degradation, drain attribution, standby loss, and lifespan."
  },
  cpu: {
    eyebrow: "Silicon Observatory",
    title: "CPU Analytics",
    description: "Package power, residency, P-states, interrupts, and scheduling behavior."
  },
  gpu: {
    eyebrow: "Residency Control",
    title: "GPU Intelligence",
    description: "dGPU wakeups, switching events, VRAM context, and rendering load."
  },
  thermal: {
    eyebrow: "Thermal Engineering",
    title: "Thermal Analytics",
    description: "Hotspot tracking, saturation, throttling, and fan-response telemetry."
  },
  timeline: {
    eyebrow: "Correlation Lab",
    title: "Advanced Event Correlation Timeline",
    description: "Linked event overlays across launches, wakeups, drain, timers, and thermals."
  },
  optimization: {
    eyebrow: "Controlled Optimization",
    title: "Optimization Center",
    description: "Explainable, reversible power profiles with expected impact and risk."
  },
  vendor: {
    eyebrow: "OEM Intelligence",
    title: "Vendor Intelligence",
    description: "ASUS, Lenovo, Dell, and HP service behavior, firmware quirks, and tuning hints."
  },
  safety: {
    eyebrow: "Rollback Ledger",
    title: "Rollback & Safety",
    description: "Snapshots, transaction logs, config diffs, and validation history."
  },
  reports: {
    eyebrow: "Evidence Reports",
    title: "Reports",
    description: "Export-ready summaries for benchmarks, battery studies, vendors, and profiles."
  },
  advanced: {
    eyebrow: "Low-Level Mode",
    title: "Advanced Engineering Telemetry",
    description: "ETW streams, DPC latency, interrupts, scheduler traces, and raw power channels."
  },
  settings: {
    eyebrow: "Operator Controls",
    title: "Settings",
    description: "Telemetry permissions, logging, safety policy, updates, and developer options."
  }
};

const metricSeeds: Record<NavKey, CardMetric[]> = {
  dashboard: [
    { label: "Optimization Score", value: "98", unit: "%", status: "+2.4% in 24h", points: [60, 70, 77, 81, 90, 98] },
    { label: "Idle Efficiency", value: "1.2", unit: "W", status: "Optimal avg drain", points: [2, 1.7, 1.8, 1.4, 1.2] },
    { label: "Deep Sleep", value: "84", unit: "%", status: "22 wakeups last cycle", accent: "warn" },
    { label: "Thermal Index", value: "A+", status: "Stable delta 4C", accent: "healthy" }
  ],
  observability: [
    { label: "CPU Package", value: "12.4", unit: "W", status: "Live power draw", points: wakeLine },
    { label: "Active Wakeups", value: "342", unit: "/sec", status: "Streaming", accent: "warn" },
    { label: "System Latency", value: "0.8", unit: "ms", status: "Balanced", accent: "info" },
    { label: "Timer Pressure", value: "1.0", unit: "ms", status: "Chrome active", accent: "critical" }
  ],
  diagnostics: [
    { label: "Critical Findings", value: "1", status: "Thermal throttling", accent: "critical" },
    { label: "Warnings", value: "4", status: "Drain and wakeups", accent: "warn" },
    { label: "Rollback Coverage", value: "100", unit: "%", status: "Snapshot ready", accent: "healthy" },
    { label: "Root Cause Confidence", value: "92", unit: "%", status: "High correlation" }
  ],
  telemetry: [
    { label: "Samples/sec", value: "128", status: "Stable ingest" },
    { label: "Channels", value: "42", status: "CPU/GPU/Power" },
    { label: "Retention", value: "30", unit: "d", status: "Local SQLite" },
    { label: "Anomalies", value: "3", status: "Filtered view", accent: "warn" }
  ],
  battery: [
    { label: "Battery Health", value: "92.4", unit: "%", status: "8,536 mWh below design" },
    { label: "Lifespan", value: "2.8", unit: "yrs", status: "Degrading 0.4% faster", accent: "warn" },
    { label: "Cycle Count", value: "412", unit: "/1000", status: "+24 cycles last 30d" },
    { label: "Standby Drain", value: "3.8", unit: "%", status: "Overnight baseline", accent: "warn" }
  ],
  cpu: [
    { label: "Package Power", value: "38.4", unit: "W", status: "Peak transient", points: lineA },
    { label: "C10 Residency", value: "15.3", unit: "%", status: "Package sleep" },
    { label: "Wakeups/sec", value: "459", status: "Scheduler active", accent: "warn" },
    { label: "Efficiency", value: "8.4", unit: "/10", status: "Overall score" }
  ],
  gpu: [
    { label: "dGPU Awake", value: "18", unit: "%", status: "Last hour", accent: "warn" },
    { label: "Deep Sleep", value: "88.4", unit: "%", status: "RC6 residency" },
    { label: "VRAM", value: "1.2", unit: "GB", status: "Active contexts" },
    { label: "Switches", value: "7", status: "App triggered" }
  ],
  thermal: [
    { label: "CPU Package", value: "42", unit: "C", status: "Cooling active" },
    { label: "Hotspot", value: "68", unit: "C", status: "Below throttle" },
    { label: "Fan Speed", value: "1200", unit: "RPM", status: "Acoustic mode" },
    { label: "Saturation", value: "31", unit: "%", status: "Thermal headroom" }
  ],
  timeline: [
    { label: "Linked Events", value: "18", status: "Causality graph" },
    { label: "Power Spikes", value: "4", status: "Overlay enabled", accent: "warn" },
    { label: "Critical Edges", value: "2", status: "Timer + GPU", accent: "critical" },
    { label: "Confidence", value: "91", unit: "%", status: "Correlation score" }
  ],
  optimization: [
    { label: "Battery Mode", value: "-6.4", unit: "W", status: "Expected savings" },
    { label: "Gaming Mode", value: "Low", status: "Latency risk" },
    { label: "Developer Mode", value: "98", unit: "%", status: "CPU max cap" },
    { label: "Silent Mode", value: "70", unit: "%", status: "Thermal ceiling" }
  ],
  vendor: [
    { label: "Detected OEM", value: "ASUS", status: "ROG service profile" },
    { label: "Vendor Services", value: "7", status: "3 noisy candidates" },
    { label: "Firmware Hints", value: "4", status: "Battery and fan curves" },
    { label: "Quirk Score", value: "82", unit: "%", status: "Known behavior" }
  ],
  safety: [
    { label: "Snapshots", value: "14", status: "Newest 04:35" },
    { label: "Blocked Actions", value: "3", status: "Critical services" },
    { label: "Rollback Tests", value: "96", unit: "%", status: "Validation pass" },
    { label: "Diff Coverage", value: "100", unit: "%", status: "CPU/service state" }
  ],
  reports: [
    { label: "Battery Reports", value: "8", status: "Export ready" },
    { label: "Benchmarks", value: "12", status: "Before/after" },
    { label: "Vendor Studies", value: "4", status: "ASUS/Lenovo/Dell/HP" },
    { label: "Impact Delta", value: "-14", unit: "%", status: "Average drain" }
  ],
  advanced: [
    { label: "ETW Events", value: "9.8k", status: "Buffered" },
    { label: "DPC Latency", value: "0.42", unit: "ms", status: "Nominal" },
    { label: "Interrupts", value: "1.2k", unit: "/s", status: "USB + ACPI" },
    { label: "Raw Channels", value: "64", status: "Engineering mode" }
  ],
  settings: [
    { label: "Telemetry", value: "Local", status: "No remote sink" },
    { label: "Logging", value: "Verbose", status: "Diagnostics mode" },
    { label: "Safety", value: "Strict", status: "Firewall enforced" },
    { label: "Updates", value: "Manual", status: "Stable channel" }
  ]
};

function App() {
  const [active, setActive] = useState<NavKey>("dashboard");
  const [range, setRange] = useState("Real-time");
  const [query, setQuery] = useState("");
  const [expanded, setExpanded] = useState<string | null>("Thermal Throttling Detected");
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const timer = window.setInterval(() => setTick((value) => value + 1), 1600);
    return () => window.clearInterval(timer);
  }, []);

  const current = pageCopy[active];
  const metrics = metricSeeds[active];
  const filteredEvents = useMemo(
    () => eventStream.filter(([, message]) => message.toLowerCase().includes(query.toLowerCase())),
    [query]
  );

  return (
    <div className="flex h-full p-3 text-slate-100">
      <Sidebar active={active} onChange={setActive} />
      <main className="panel ml-3 flex min-w-0 flex-1 flex-col overflow-hidden rounded-md bg-[#08131e]/94">
        <TopBar range={range} setRange={setRange} query={query} setQuery={setQuery} />
        <section className="scrollbar-thin min-h-0 flex-1 overflow-auto p-5">
          <Header current={current} active={active} />
          <MetricStrip metrics={metrics} tick={tick} />
          <PageBody
            active={active}
            query={query}
            events={filteredEvents}
            expanded={expanded}
            setExpanded={setExpanded}
            tick={tick}
          />
        </section>
      </main>
    </div>
  );
}

function Sidebar({ active, onChange }: { active: NavKey; onChange: (key: NavKey) => void }) {
  const groups = Array.from(new Set(navItems.map((item) => item.group)));

  return (
    <aside className="panel flex w-[260px] shrink-0 flex-col rounded-md bg-[#0b1a28]/94">
      <div className="border-b border-line p-4">
        <div className="flex items-center gap-3">
          <div className="grid size-9 place-items-center rounded-md border border-telemetry/30 bg-telemetry/12 text-telemetry">
            <Gauge size={18} />
          </div>
          <div>
            <div className="text-sm font-bold text-white">VoltMetrics Pro</div>
            <div className="text-[10px] font-semibold uppercase tracking-wide text-slate-400">Precision Observability</div>
          </div>
        </div>
      </div>
      <nav className="scrollbar-thin min-h-0 flex-1 overflow-auto px-3 py-4">
        {groups.map((group) => (
          <div key={group} className="mb-5">
            <div className="mb-2 px-2 text-[10px] font-bold uppercase text-slate-500">{group}</div>
            <div className="space-y-1">
              {navItems
                .filter((item) => item.group === group)
                .map((item) => {
                  const Icon = item.icon;
                  const isActive = active === item.key;
                  return (
                    <button
                      key={item.key}
                      onClick={() => onChange(item.key)}
                      className={`flex h-9 w-full items-center gap-3 rounded px-3 text-left text-[13px] transition ${
                        isActive
                          ? "border-l-2 border-telemetry bg-telemetry/14 text-white shadow-glow"
                          : "text-slate-300 hover:bg-white/[0.06] hover:text-white"
                      }`}
                      title={item.label}
                    >
                      <Icon size={15} />
                      <span className="truncate">{item.label}</span>
                    </button>
                  );
                })}
            </div>
          </div>
        ))}
      </nav>
      <div className="border-t border-line p-3">
        <button className="flex h-10 w-full items-center justify-center gap-2 rounded bg-gradient-to-r from-cyan-400 to-cobalt text-xs font-bold text-slate-950 transition hover:brightness-110">
          <Play size={14} />
          Run Diagnostics
        </button>
        <div className="mt-3 flex items-center gap-2 rounded bg-white/5 p-2">
          <div className="grid size-8 place-items-center rounded bg-slate-700/60 text-xs font-bold">SA</div>
          <div className="min-w-0">
            <div className="truncate text-xs font-semibold">System Architect</div>
            <div className="truncate text-[10px] text-slate-400">Admin session</div>
          </div>
        </div>
      </div>
    </aside>
  );
}

function TopBar({
  range,
  setRange,
  query,
  setQuery
}: {
  range: string;
  setRange: (range: string) => void;
  query: string;
  setQuery: (query: string) => void;
}) {
  return (
    <header className="flex h-14 shrink-0 items-center gap-3 border-b border-line bg-[#0b1724]/95 px-5">
      <div className="flex items-center gap-2 rounded bg-healthy/10 px-3 py-1 text-[11px] font-bold text-healthy">
        <span className="pulse-dot size-2 rounded-full bg-healthy" />
        Health Score: 98%
      </div>
      <div className="rounded bg-white/5 px-3 py-1 text-[11px] text-slate-300">Battery Mode</div>
      <div className="rounded bg-white/5 px-3 py-1 text-[11px] text-slate-300">Active Telemetry</div>
      <div className="ml-auto flex min-w-[260px] items-center rounded border border-line bg-[#07111b] px-3 py-2">
        <Search size={14} className="text-slate-500" />
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="ml-2 w-full bg-transparent text-xs text-slate-200 outline-none placeholder:text-slate-600"
          placeholder="Search telemetry..."
        />
      </div>
      <div className="flex rounded border border-line bg-white/5 p-1">
        {["Real-time", "History", "Forecast"].map((item) => (
          <button
            key={item}
            onClick={() => setRange(item)}
            className={`h-7 rounded px-3 text-[11px] font-semibold transition ${
              range === item ? "bg-telemetry text-slate-950" : "text-slate-400 hover:text-white"
            }`}
          >
            {item}
          </button>
        ))}
      </div>
      <IconButton icon={RefreshCw} label="Refresh telemetry" />
      <IconButton icon={Bell} label="Notifications" />
      <IconButton icon={Lock} label="Safety status" />
    </header>
  );
}

function IconButton({ icon: Icon, label }: { icon: LucideIcon; label: string }) {
  return (
    <button
      className="grid size-8 place-items-center rounded border border-line bg-white/5 text-slate-300 transition hover:border-telemetry/50 hover:text-telemetry"
      title={label}
    >
      <Icon size={15} />
    </button>
  );
}

function Header({ current, active }: { current: (typeof pageCopy)[NavKey]; active: NavKey }) {
  return (
    <div className="mb-4 flex items-end justify-between">
      <div>
        <div className="mb-2 inline-flex items-center gap-2 rounded bg-telemetry/10 px-2 py-1 text-[10px] font-bold uppercase text-telemetry">
          <Activity size={12} />
          {current.eyebrow}
        </div>
        <h1 className="text-2xl font-bold text-white">{current.title}</h1>
        <p className="mt-1 max-w-3xl text-sm text-slate-400">{current.description}</p>
      </div>
      <div className="hidden items-center gap-2 lg:flex">
        <span className="rounded border border-line bg-white/5 px-3 py-2 text-xs text-slate-300">
          Profile: {active === "optimization" ? "Developer Mode" : "Battery Mode"}
        </span>
        <span className="rounded border border-line bg-white/5 px-3 py-2 text-xs text-telemetry">System Pulse Live</span>
      </div>
    </div>
  );
}

function MetricStrip({ metrics, tick }: { metrics: CardMetric[]; tick: number }) {
  return (
    <div className="mb-4 grid grid-cols-4 gap-3">
      {metrics.map((metric, index) => (
        <MetricCard key={metric.label} metric={metric} tick={tick + index} />
      ))}
    </div>
  );
}

function MetricCard({ metric, tick }: { metric: CardMetric; tick: number }) {
  const accent = colorFor(metric.accent ?? "info");

  return (
    <div className="panel min-h-[112px] rounded-md p-4 transition hover:border-telemetry/40 hover:bg-[#122033]">
      <div className="flex items-start justify-between">
        <div className="text-xs font-semibold text-slate-400">{metric.label}</div>
        <span className="size-2 rounded-full" style={{ background: accent }} />
      </div>
      <div className="mt-3 flex items-end gap-1">
        <span className="text-3xl font-black text-white">{metric.value}</span>
        {metric.unit && <span className="mb-1 text-sm font-bold text-slate-400">{metric.unit}</span>}
      </div>
      <div className="mt-1 text-[11px] text-slate-400">{metric.status}</div>
      <div className="mt-3 h-7">
        <MiniLine points={metric.points ?? [tick % 4, 4, 3, 6, 5, 8, 7]} color={accent} />
      </div>
    </div>
  );
}

function PageBody({
  active,
  query,
  events,
  expanded,
  setExpanded,
  tick
}: {
  active: NavKey;
  query: string;
  events: string[][];
  expanded: string | null;
  setExpanded: (id: string | null) => void;
  tick: number;
}) {
  if (active === "timeline") return <TimelinePage />;
  if (active === "observability") return <ObservabilityPage events={events} tick={tick} />;
  if (active === "diagnostics") return <DiagnosticsPage expanded={expanded} setExpanded={setExpanded} />;
  if (active === "optimization") return <OptimizationPage />;
  if (active === "safety") return <SafetyPage />;
  if (active === "settings") return <SettingsPage />;
  return <AnalyticsGrid active={active} query={query} />;
}

function AnalyticsGrid({ active, query }: { active: NavKey; query: string }) {
  const focus = focusFor(active);
  const rows = tableRows(active).filter((row) => row.join(" ").toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="grid grid-cols-12 gap-4">
      <Panel title={focus.primaryTitle} className="col-span-7 min-h-[310px]" action="Live">
        <AreaChart points={focus.chart} color={focus.color} />
      </Panel>
      <Panel title={focus.secondaryTitle} className="col-span-5 min-h-[310px]" action="Causality">
        <ResidencyList active={active} />
      </Panel>
      <Panel title={focus.tableTitle} className="col-span-6 min-h-[280px]" action="View all">
        <DataTable rows={rows} />
      </Panel>
      <Panel title={focus.detailTitle} className="col-span-3 min-h-[280px]">
        <RadialScore value={focus.score} label={focus.scoreLabel} color={focus.color} />
      </Panel>
      <Panel title={focus.barTitle} className="col-span-3 min-h-[280px]">
        <BarChart values={focus.bars} />
      </Panel>
    </div>
  );
}

function ObservabilityPage({ events, tick }: { events: string[][]; tick: number }) {
  return (
    <div className="grid grid-cols-12 gap-4">
      <Panel title="Wakeup Analysis Topology" className="col-span-8 min-h-[560px]" action="Streaming">
        <AreaChart points={wakeLine.map((point, index) => point + (index === tick % wakeLine.length ? 180 : 0))} color="#8ee7ff" tall />
      </Panel>
      <Panel title="Live Event Console" className="col-span-4 min-h-[560px]" action="Raw">
        <EventConsole events={events} />
      </Panel>
      <Panel title="Core Thermal Distribution" className="col-span-6 min-h-[220px]">
        <ThermalMatrix />
      </Panel>
      <Panel title="Active Correlations" className="col-span-6 min-h-[220px]">
        <CorrelationCards />
      </Panel>
    </div>
  );
}

function DiagnosticsPage({
  expanded,
  setExpanded
}: {
  expanded: string | null;
  setExpanded: (id: string | null) => void;
}) {
  const cards = [
    {
      title: "Thermal Throttling Detected",
      severity: "critical" as Severity,
      impact: "-15% Performance",
      explanation:
        "Sustained load on cores 4-7 pushed package temperature beyond 95C while aggressive boost clocks stayed active.",
      recommendation: "Apply Developer profile to cap extreme turbo transients and re-test."
    },
    {
      title: "Anomalous Drain Rate",
      severity: "warn" as Severity,
      impact: "+2W Continuous",
      explanation: "Background process is preventing C-state idle and causing elevated standby drain.",
      recommendation: "Isolate the process and verify timer-resolution behavior."
    },
    {
      title: "Page Fault Spikes",
      severity: "info" as Severity,
      impact: "+2.4GB Swap",
      explanation: "VRAM allocation thrashing detected in the GPU subsystem during browser playback.",
      recommendation: "Purge cache or disable hardware acceleration for the offender."
    }
  ];

  return (
    <div className="grid grid-cols-12 gap-4">
      {cards.map((card, index) => (
        <button
          key={card.title}
          onClick={() => setExpanded(expanded === card.title ? null : card.title)}
          className={`panel rounded-md p-5 text-left transition hover:border-telemetry/40 ${index === 0 ? "col-span-12" : "col-span-6"}`}
        >
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <SeverityBadge severity={card.severity} />
                <h2 className="text-lg font-bold text-white">{card.title}</h2>
              </div>
              <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-300">{card.explanation}</p>
              {expanded === card.title && (
                <div className="mt-4 grid grid-cols-3 gap-3 text-xs">
                  <div className="rounded border border-line bg-white/5 p-3">
                    <div className="text-slate-500">Estimated impact</div>
                    <div className="mt-1 font-bold text-warn">{card.impact}</div>
                  </div>
                  <div className="rounded border border-line bg-white/5 p-3">
                    <div className="text-slate-500">Recommendation</div>
                    <div className="mt-1 font-bold text-telemetry">{card.recommendation}</div>
                  </div>
                  <div className="rounded border border-line bg-white/5 p-3">
                    <div className="text-slate-500">Rollback support</div>
                    <div className="mt-1 font-bold text-healthy">Snapshot protected</div>
                  </div>
                </div>
              )}
            </div>
            <div className="rounded bg-white/5 px-3 py-2 text-sm font-bold text-slate-300">{card.impact}</div>
          </div>
        </button>
      ))}
    </div>
  );
}

function TimelinePage() {
  const [scrub, setScrub] = useState(58);

  return (
    <div className="grid grid-cols-12 gap-4">
      <Panel title="Correlation Canvas" className="col-span-12 min-h-[610px]" action="1H">
        <div className="mb-4 flex items-center gap-3 text-xs text-slate-400">
          <span className="text-telemetry">Applications</span>
          <span className="text-warn">GPU Wake</span>
          <span className="text-critical">Thermal Spike</span>
          <input
            type="range"
            min="8"
            max="92"
            value={scrub}
            onChange={(event) => setScrub(Number(event.target.value))}
            className="ml-auto w-80 accent-telemetry"
          />
        </div>
        <CorrelationTimeline scrub={scrub} />
      </Panel>
    </div>
  );
}

function OptimizationPage() {
  const profiles = [
    ["Battery Mode", "-6.4W", "Low", "CPU min state, RGB services, timer pressure"],
    ["Gaming Mode", "+FPS stability", "Low", "High Performance plan and boost stability"],
    ["Developer Mode", "-9C peaks", "Low", "CPU max 98% to reduce compile thermal overshoot"],
    ["Silent Mode", "-1200RPM", "Medium", "CPU cap 70% for fanless acoustic target"]
  ];

  return (
    <div className="grid grid-cols-12 gap-4">
      {profiles.map(([name, impact, risk, systems]) => (
        <Panel key={name} title={name} className="col-span-6 min-h-[230px]" action="Explain">
          <div className="grid grid-cols-3 gap-3">
            <InfoTile label="Expected impact" value={impact} />
            <InfoTile label="Risk level" value={risk} />
            <InfoTile label="Rollback" value="Supported" />
          </div>
          <p className="mt-4 text-sm leading-6 text-slate-300">{systems}</p>
          <div className="mt-5 flex gap-3">
            <button className="rounded border border-telemetry/40 bg-telemetry/10 px-4 py-2 text-xs font-bold text-telemetry">
              Preview Diff
            </button>
            <button className="rounded bg-white/[0.08] px-4 py-2 text-xs font-bold text-slate-300">Dry Run</button>
          </div>
        </Panel>
      ))}
    </div>
  );
}

function SafetyPage() {
  return (
    <div className="grid grid-cols-12 gap-4">
      <Panel title="Rollback History" className="col-span-7 min-h-[410px]" action="Snapshots">
        <DataTable
          rows={[
            ["04:35", "battery", "CPU min + service state", "Verified"],
            ["03:58", "developer", "CPU max state", "Verified"],
            ["Yesterday", "silent", "Thermal ceiling", "Verified"],
            ["May 22", "gaming", "Power scheme", "Verified"]
          ]}
        />
      </Panel>
      <Panel title="Transaction Diff" className="col-span-5 min-h-[410px]" action="Guarded">
        <div className="space-y-3">
          {["WinDefend disable blocked", "Power scheme snapshot captured", "CPU P-state restored", "Service state checksum matched"].map(
            (item, index) => (
              <div key={item} className="flex items-center justify-between rounded border border-line bg-white/5 p-3">
                <span className="text-sm text-slate-300">{item}</span>
                <SeverityBadge severity={index === 0 ? "critical" : "healthy"} />
              </div>
            )
          )}
        </div>
      </Panel>
    </div>
  );
}

function SettingsPage() {
  const settings = ["Telemetry permissions", "Logging verbosity", "Optimization aggressiveness", "Safety controls", "Update channel", "Developer traces"];

  return (
    <div className="grid grid-cols-12 gap-4">
      <Panel title="Operator Settings" className="col-span-8 min-h-[460px]" action="Strict Mode">
        <div className="space-y-3">
          {settings.map((setting, index) => (
            <div key={setting} className="flex items-center justify-between rounded border border-line bg-white/5 p-4">
              <div>
                <div className="text-sm font-bold text-white">{setting}</div>
                <div className="mt-1 text-xs text-slate-500">Policy controlled for local workstation operation.</div>
              </div>
              <button className={`h-7 w-14 rounded-full p-1 ${index === 2 ? "bg-warn/40" : "bg-healthy/30"}`}>
                <span className={`block size-5 rounded-full bg-white transition ${index === 2 ? "translate-x-7" : "translate-x-0"}`} />
              </button>
            </div>
          ))}
        </div>
      </Panel>
      <Panel title="Developer Channel" className="col-span-4 min-h-[460px]" action="Local">
        <RadialScore value={88} label="Safety posture" color="#5ee6a7" />
      </Panel>
    </div>
  );
}

function Panel({
  title,
  action,
  className,
  children
}: {
  title: string;
  action?: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <section className={`panel rounded-md p-4 ${className ?? ""}`}>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-sm font-bold text-white">{title}</h2>
        {action && <span className="rounded bg-telemetry/10 px-2 py-1 text-[10px] font-bold uppercase text-telemetry">{action}</span>}
      </div>
      {children}
    </section>
  );
}

function MiniLine({ points, color }: { points: number[]; color: string }) {
  const d = linePath(points, 110, 28);
  return (
    <svg viewBox="0 0 110 28" className="h-full w-full overflow-visible">
      <path d={d} fill="none" stroke={color} strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

function AreaChart({ points, color, tall = false }: { points: number[]; color: string; tall?: boolean }) {
  const height = tall ? 470 : 225;
  const width = 720;
  const d = linePath(points, width, height - 26);
  const area = `${d} L ${width} ${height} L 0 ${height} Z`;

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="fine-grid h-full min-h-[220px] w-full rounded bg-[#081019]">
      <defs>
        <linearGradient id={`area-${color.replace("#", "")}`} x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.38" />
          <stop offset="100%" stopColor={color} stopOpacity="0.02" />
        </linearGradient>
      </defs>
      <path d={area} fill={`url(#area-${color.replace("#", "")})`} />
      <path d={d} fill="none" stroke={color} strokeWidth="5" strokeLinecap="round" />
      <line x1="0" x2={width} y1={height - 48} y2={height - 48} stroke="rgba(148,163,184,.16)" strokeDasharray="8 8" />
    </svg>
  );
}

function BarChart({ values }: { values: number[] }) {
  const max = Math.max(...values);
  return (
    <div className="flex h-[190px] items-end gap-3 rounded bg-[#081019] p-5">
      {values.map((value, index) => (
        <div key={`${value}-${index}`} className="flex flex-1 flex-col items-center gap-2">
          <div
            className="w-full rounded-t bg-gradient-to-t from-telemetry to-[#b6b4ff]"
            style={{ height: `${(value / max) * 150}px` }}
          />
          <span className="text-[10px] text-slate-500">C{index}</span>
        </div>
      ))}
    </div>
  );
}

function ResidencyList({ active }: { active: NavKey }) {
  const rows =
    active === "gpu"
      ? [["RC6 Deep Sleep", 88.4], ["RC0 Active", 11.2], ["Wait/Stall", 0.4]]
      : [["C0 Active", 12.4], ["C3 Light Sleep", 24.1], ["C7 Deep Sleep", 48.2], ["C10 Package", 15.3]];

  return (
    <div className="space-y-4">
      {rows.map(([label, value]) => (
        <div key={String(label)}>
          <div className="mb-2 flex justify-between text-xs">
            <span className="text-slate-300">{label}</span>
            <span className="font-bold text-telemetry">{value}%</span>
          </div>
          <div className="h-2 rounded-full bg-white/[0.08]">
            <div className="h-full rounded-full bg-gradient-to-r from-telemetry to-[#b6b4ff]" style={{ width: `${value}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

function DataTable({ rows }: { rows: string[][] }) {
  return (
    <div className="overflow-hidden rounded border border-line">
      {rows.map((row, index) => (
        <div key={row.join("-")} className="grid grid-cols-4 gap-3 border-b border-line bg-white/[0.03] p-3 text-xs last:border-b-0">
          {row.map((cell, cellIndex) => (
            <span key={cell} className={cellIndex === row.length - 1 ? "font-bold text-telemetry" : "text-slate-300"}>
              {cell}
            </span>
          ))}
          {index === 0 && <span className="sr-only">first row</span>}
        </div>
      ))}
    </div>
  );
}

function EventConsole({ events }: { events: string[][] }) {
  return (
    <div className="h-[500px] overflow-hidden rounded border border-line bg-[#090d12] p-3 font-mono text-[11px]">
      {events.map(([type, message], index) => (
        <div key={`${message}-${index}`} className="stream-row mb-2 grid grid-cols-[56px_1fr] gap-2 rounded border border-line bg-white/[0.03] p-2">
          <span className={type === "CRIT" ? "text-critical" : type === "WARN" ? "text-warn" : "text-telemetry"}>{type}</span>
          <span className="text-slate-300">{message}</span>
        </div>
      ))}
    </div>
  );
}

function CorrelationTimeline({ scrub }: { scrub: number }) {
  const lanes = ["Applications", "Hardware State", "Thermals", "Power Draw", "Power State"];

  return (
    <div className="relative h-[520px] overflow-hidden rounded border border-line bg-[#070b10]">
      <div className="absolute left-0 top-0 z-10 h-full w-52 border-r border-line bg-[#111820]">
        {lanes.map((lane, index) => (
          <div key={lane} className="flex h-[104px] flex-col justify-center border-b border-line px-5">
            <span className="text-xs font-bold text-telemetry">{lane}</span>
            <span className="mt-1 text-[10px] text-slate-500">{["Foreground state", "GPU/CPU activity", "Package temp", "Discharge rate", "C-state transition"][index]}</span>
          </div>
        ))}
      </div>
      <svg viewBox="0 0 1000 520" className="absolute inset-y-0 left-52 right-0 h-full w-[calc(100%-13rem)]">
        {[0, 1, 2, 3, 4].map((lane) => (
          <line key={lane} x1="0" x2="1000" y1={lane * 104 + 104} y2={lane * 104 + 104} stroke="rgba(148,163,184,.12)" />
        ))}
        <path d="M40 382 L360 378 L410 250 L520 280 L710 318 L950 360" stroke="#8ee7ff" strokeWidth="3" fill="none" />
        <path d="M40 300 L360 292 L420 188 L515 205 L650 248 L950 230" stroke="#ff9f8d" strokeWidth="2" fill="none" />
        <path d="M40 214 L370 212 L420 160 L570 166 L700 205 L950 206" stroke="#ffc857" strokeWidth="2" fill="none" />
        {timelineEvents.map((event) => (
          <g key={event.label} transform={`translate(${event.x * 9.6}, ${laneY(event.lane)})`}>
            <circle r="7" fill={colorFor(event.severity)} />
            <rect x="12" y="-16" width="126" height="24" rx="3" fill="rgba(16,24,32,.92)" stroke={colorFor(event.severity)} />
            <text x="20" y="0" fill="#d9f6ff" fontSize="12" fontFamily="monospace">
              {event.time} {event.label}
            </text>
          </g>
        ))}
        <line x1={scrub * 9.6} x2={scrub * 9.6} y1="0" y2="520" stroke="#ff8d8d" strokeWidth="2" opacity=".7" />
      </svg>
    </div>
  );
}

function RadialScore({ value, label, color }: { value: number; label: string; color: string }) {
  const dash = 2 * Math.PI * 58;

  return (
    <div className="flex h-[210px] flex-col items-center justify-center">
      <svg viewBox="0 0 150 150" className="size-40">
        <circle cx="75" cy="75" r="58" stroke="rgba(148,163,184,.16)" strokeWidth="12" fill="none" />
        <circle
          cx="75"
          cy="75"
          r="58"
          stroke={color}
          strokeWidth="12"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={dash}
          strokeDashoffset={dash - (dash * value) / 100}
          transform="rotate(-90 75 75)"
        />
        <text x="75" y="72" textAnchor="middle" fill="#fff" fontSize="26" fontWeight="800">
          {value}
        </text>
        <text x="75" y="92" textAnchor="middle" fill="#94a3b8" fontSize="11">
          {label}
        </text>
      </svg>
    </div>
  );
}

function ThermalMatrix() {
  return (
    <div className="grid grid-cols-4 gap-3">
      {["CPU Package", "CPU Core", "System Fans", "VRM"].map((item, index) => (
        <div key={item} className="min-h-[150px] rounded border border-line bg-[#08131d] p-4">
          <div className="text-xs text-slate-400">{item}</div>
          <div className="mt-12 text-3xl font-black text-white">{[42, 38, 1200, 51][index]}</div>
          <div className="text-xs text-slate-500">{index === 2 ? "RPM" : "C"}</div>
        </div>
      ))}
    </div>
  );
}

function CorrelationCards() {
  return (
    <div className="grid grid-cols-3 gap-3">
      {timelineEvents.slice(1, 4).map((event) => (
        <div key={event.label} className="rounded border border-line bg-white/5 p-4">
          <SeverityBadge severity={event.severity} />
          <div className="mt-3 text-sm font-bold text-white">{event.label}</div>
          <div className="mt-2 text-xs text-slate-500">Linked at {event.time} with power-state transition evidence.</div>
        </div>
      ))}
    </div>
  );
}

function InfoTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded border border-line bg-white/5 p-3">
      <div className="text-[11px] text-slate-500">{label}</div>
      <div className="mt-1 text-lg font-black text-white">{value}</div>
    </div>
  );
}

function SeverityBadge({ severity }: { severity: Severity }) {
  return (
    <span
      className="inline-flex items-center gap-1 rounded px-2 py-1 text-[10px] font-black uppercase"
      style={{ background: `${colorFor(severity)}22`, color: colorFor(severity) }}
    >
      {severity === "critical" && <AlertTriangle size={11} />}
      {severity}
    </span>
  );
}

function linePath(points: number[], width: number, height: number) {
  const min = Math.min(...points);
  const max = Math.max(...points);
  const span = max - min || 1;
  return points
    .map((point, index) => {
      const x = (index / (points.length - 1)) * width;
      const y = height - ((point - min) / span) * (height - 10) + 5;
      return `${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`;
    })
    .join(" ");
}

function laneY(lane: string) {
  const laneMap: Record<string, number> = {
    Applications: 78,
    "Hardware State": 174,
    Thermals: 260,
    "Power Draw": 372,
    "Power State": 462
  };

  return laneMap[lane] ?? 80;
}

function colorFor(severity: Severity) {
  return {
    healthy: "#5ee6a7",
    info: "#8ee7ff",
    warn: "#ffc857",
    critical: "#ff6b6b"
  }[severity];
}

function focusFor(active: NavKey) {
  const base = {
    chart: active === "battery" ? lineB : active === "thermal" ? thermalLine : lineA,
    color: active === "thermal" ? "#ff9f8d" : "#8ee7ff",
    primaryTitle: "Package Power Timeline",
    secondaryTitle: "C-State Residency",
    tableTitle: "Process Drain Attribution",
    detailTitle: "Efficiency Score",
    barTitle: "P-State Distribution",
    score: 90,
    scoreLabel: "Health",
    bars: [24, 54, 72, 88]
  };

  const overrides: Partial<Record<NavKey, Partial<typeof base>>> = {
    battery: { primaryTitle: "Capacity Degradation Curve", secondaryTitle: "Standby Drain Heatmap", score: 92, scoreLabel: "Battery" },
    gpu: { primaryTitle: "GPU Residency Timeline", secondaryTitle: "Switching Activity", tableTitle: "dGPU Wake Attribution", score: 88, scoreLabel: "RC6" },
    thermal: { primaryTitle: "Thermal Saturation Timeline", secondaryTitle: "Fan Response Curve", tableTitle: "Thermal Events", score: 84, scoreLabel: "Thermal" },
    reports: { primaryTitle: "Optimization Impact Report", secondaryTitle: "Benchmark Comparison", tableTitle: "Generated Reports", score: 94, scoreLabel: "Ready" },
    advanced: { primaryTitle: "ETW Event Stream Density", secondaryTitle: "Interrupt Classes", tableTitle: "Raw Channels", score: 78, scoreLabel: "Signal" }
  };

  return { ...base, ...(overrides[active] ?? {}) };
}

function tableRows(active: NavKey) {
  const common = [
    ["Chrome Helper", "+4.2 W", "1,246 mWh", "High"],
    ["VS Code Helper", "+2.1 W", "899 mWh", "Medium"],
    ["Discord Desktop", "+1.5 W", "629 mWh", "Medium"],
    ["System UI Server", "<0.1 W", "42 mWh", "Low"]
  ];

  const special: Partial<Record<NavKey, string[][]>> = {
    vendor: [
      ["ASUS LightingService", "Polling", "RGB controller", "Review"],
      ["Lenovo Vantage", "Wake timer", "Battery policy", "Monitor"],
      ["Dell Optimizer", "Telemetry", "Background agent", "Review"],
      ["HP Support Assistant", "Scheduler", "Update checks", "Monitor"]
    ],
    reports: [
      ["Battery report", "PDF/HTML", "Today", "Ready"],
      ["Benchmark delta", "JSON", "Yesterday", "Ready"],
      ["Vendor analysis", "Markdown", "May 22", "Ready"],
      ["Thermal study", "CSV", "May 20", "Draft"]
    ]
  };

  return special[active] ?? common;
}

export default App;
