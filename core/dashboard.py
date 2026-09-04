import os
import sys
import json
import webbrowser
from telemetry import collect_telemetry

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PowerTune | Advanced Systems Observability</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons CDN -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Inter Font -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #060b13;
        }
        .scrollbar-thin::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .scrollbar-thin::-webkit-scrollbar-track {
            background: #090e18;
        }
        .scrollbar-thin::-webkit-scrollbar-thumb {
            background: #1b263b;
            border-radius: 3px;
        }
        .panel {
            background-color: #0c1322;
            border: 1px solid #1b263b;
        }
        .shadow-glow {
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.15);
        }
        .nav-item.active {
            background-color: rgba(56, 189, 248, 0.1);
            border-left: 2px solid #38bdf8;
            color: #ffffff;
        }
    </style>
</head>
<body class="overflow-hidden text-slate-200">

    <div class="flex h-screen w-screen overflow-hidden">
        <!-- SIDEBAR -->
        <aside class="w-64 bg-[#090e18] border-r border-[#1b263b] flex flex-col shrink-0">
            <!-- Header -->
            <div class="p-4 border-b border-[#1b263b] flex items-center gap-3">
                <div class="grid w-9 h-9 place-items-center rounded-md border border-cyan-500/30 bg-cyan-500/10 text-cyan-400">
                    <i data-lucide="gauge" class="w-5 h-5"></i>
                </div>
                <div>
                    <h2 class="text-sm font-black text-white tracking-wide">VoltMetrics Pro</h2>
                    <span class="text-[10px] font-semibold uppercase tracking-wider text-slate-400">Precision Observability</span>
                </div>
            </div>

            <!-- Navigation Groups -->
            <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-5 scrollbar-thin">
                <!-- Group: Mission -->
                <div>
                    <div class="px-2 text-[10px] font-bold uppercase text-slate-500 tracking-wider mb-2">Mission</div>
                    <div class="space-y-0.5">
                        <button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-item active flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="layout-dashboard" class="w-4 h-4"></i>
                            <span>Mission Control</span>
                        </button>
                        <button onclick="switchTab('observability')" id="nav-observability" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="radar" class="w-4 h-4"></i>
                            <span>Observability Center</span>
                        </button>
                        <button onclick="switchTab('diagnostics')" id="nav-diagnostics" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="brain-circuit" class="w-4 h-4"></i>
                            <span>Diagnostics Hub</span>
                        </button>
                    </div>
                </div>

                <!-- Group: Telemetry Data -->
                <div>
                    <div class="px-2 text-[10px] font-bold uppercase text-slate-500 tracking-wider mb-2">Telemetry Data</div>
                    <div class="space-y-0.5">
                        <button onclick="switchTab('battery')" id="nav-battery" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="battery-charging" class="w-4 h-4"></i>
                            <span>Battery Intelligence</span>
                        </button>
                        <button onclick="switchTab('cpu')" id="nav-cpu" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="cpu" class="w-4 h-4"></i>
                            <span>CPU Analytics</span>
                        </button>
                        <button onclick="switchTab('gpu')" id="nav-gpu" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="monitor" class="w-4 h-4"></i>
                            <span>GPU Intelligence</span>
                        </button>
                        <button onclick="switchTab('thermal')" id="nav-thermal" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="thermometer" class="w-4 h-4"></i>
                            <span>Thermal Analytics</span>
                        </button>
                    </div>
                </div>

                <!-- Group: Systems -->
                <div>
                    <div class="px-2 text-[10px] font-bold uppercase text-slate-500 tracking-wider mb-2">Systems</div>
                    <div class="space-y-0.5">
                        <button onclick="switchTab('timeline')" id="nav-timeline" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="history" class="w-4 h-4"></i>
                            <span>Event Timeline</span>
                        </button>
                        <button onclick="switchTab('optimization')" id="nav-optimization" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="sliders" class="w-4 h-4"></i>
                            <span>Optimization Center</span>
                        </button>
                    </div>
                </div>

                <!-- Group: Control -->
                <div>
                    <div class="px-2 text-[10px] font-bold uppercase text-slate-500 tracking-wider mb-2">Control</div>
                    <div class="space-y-0.5">
                        <button onclick="switchTab('safety')" id="nav-safety" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="shield-check" class="w-4 h-4"></i>
                            <span>Rollback & Safety</span>
                        </button>
                        <button onclick="switchTab('settings')" id="nav-settings" class="nav-item flex items-center gap-3 w-full h-9 px-3 rounded text-left text-xs font-medium text-slate-400 hover:bg-white/[0.04] hover:text-white transition-all">
                            <i data-lucide="settings" class="w-4 h-4"></i>
                            <span>Settings</span>
                        </button>
                    </div>
                </div>
            </nav>

            <!-- Sidebar Footer -->
            <div class="p-4 border-t border-[#1b263b] space-y-3">
                <button onclick="switchTab('diagnostics')" class="flex h-10 w-full items-center justify-center gap-2 rounded bg-gradient-to-r from-cyan-400 to-blue-600 text-xs font-bold text-slate-950 transition hover:brightness-110">
                    <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
                    Run Diagnostics
                </button>
                <div class="flex items-center gap-2 bg-white/5 p-2 rounded border border-[#1b263b]">
                    <div class="grid w-8 h-8 place-items-center rounded bg-slate-700 font-bold text-xs">SA</div>
                    <div class="min-w-0">
                        <div class="truncate text-xs font-semibold text-white">System Architect</div>
                        <div class="truncate text-[10px] text-slate-400">Admin session</div>
                    </div>
                </div>
            </div>
        </aside>

        <!-- MAIN WINDOW -->
        <main class="flex-1 flex flex-col min-w-0 bg-[#060b13] overflow-hidden">
            <!-- Topbar -->
            <header class="h-14 border-b border-[#1b263b] bg-[#090e18]/90 flex items-center px-6 gap-4 shrink-0">
                <div class="flex items-center gap-2 bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded text-xs font-bold border border-emerald-500/20">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>System Status: <span id="health-value">Optimal</span></span>
                </div>
                <div class="bg-white/5 border border-[#1b263b] px-3 py-1 rounded text-[11px] text-slate-300 font-semibold">Active Profile: Battery Mode</div>
                <div class="bg-white/5 border border-[#1b263b] px-3 py-1 rounded text-[11px] text-slate-300 font-semibold">Real-Time Ingestion</div>

                <div class="ml-auto flex items-center gap-2">
                    <div class="relative">
                        <input type="text" id="log-search" oninput="searchLogs()" placeholder="Search telemetry logs..." class="bg-[#0c1322] border border-[#1b263b] rounded px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 w-64 pl-8" />
                        <i data-lucide="search" class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5"></i>
                    </div>
                    <button onclick="location.reload()" class="grid w-8 h-8 place-items-center bg-white/5 rounded border border-[#1b263b] hover:text-cyan-400 transition" title="Refresh Live Data">
                        <i data-lucide="refresh-cw" class="w-4 h-4"></i>
                    </button>
                    <button onclick="switchTab('settings')" class="grid w-8 h-8 place-items-center bg-white/5 rounded border border-[#1b263b] hover:text-cyan-400 transition" title="Settings">
                        <i data-lucide="bell" class="w-4 h-4"></i>
                    </button>
                </div>
            </header>

            <!-- Dashboard Content Scroll Area -->
            <div class="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin">
                
                <!-- TOP HEADER -->
                <div class="flex items-end justify-between">
                    <div>
                        <div class="inline-flex items-center gap-1.5 rounded bg-cyan-500/10 border border-cyan-500/20 px-2 py-0.5 text-[10px] font-bold uppercase text-cyan-400 mb-2">
                            <i data-lucide="activity" class="w-3 h-3"></i>
                            <span id="page-eyebrow">Mission Control</span>
                        </div>
                        <h1 id="page-title" class="text-2xl font-black text-white tracking-wide">Intelligence Dashboard</h1>
                        <p id="page-desc" class="text-xs text-slate-400 mt-0.5">Real-time system diagnostics and optimization posture.</p>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="rounded border border-[#1b263b] bg-white/5 px-3 py-1.5 text-xs text-slate-300">Profile: Battery Mode</span>
                        <span class="rounded border border-cyan-500/30 bg-cyan-500/10 px-3 py-1.5 text-xs text-cyan-400 font-semibold shadow-glow">System Pulse Live</span>
                    </div>
                </div>

                <!-- METRICS STRIP -->
                <div class="grid grid-cols-4 gap-4">
                    <div class="panel rounded-md p-4 flex flex-col justify-between min-h-[110px] border border-[#1b263b] hover:border-cyan-500/40 transition">
                        <div class="flex items-start justify-between">
                            <span class="text-xs font-semibold text-slate-400">Optimization Score</span>
                            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                        </div>
                        <div class="mt-2 flex items-end gap-1">
                            <span id="metric-score" class="text-3xl font-black text-white leading-none">98</span>
                            <span class="text-xs text-slate-400 font-semibold">%</span>
                        </div>
                        <div class="text-[10px] text-slate-400 mt-1">+2.4% in 24h</div>
                    </div>
                    <div class="panel rounded-md p-4 flex flex-col justify-between min-h-[110px] border border-[#1b263b] hover:border-cyan-500/40 transition">
                        <div class="flex items-start justify-between">
                            <span class="text-xs font-semibold text-slate-400">Idle Efficiency</span>
                            <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
                        </div>
                        <div class="mt-2 flex items-end gap-1">
                            <span class="text-3xl font-black text-white leading-none">1.2</span>
                            <span class="text-xs text-slate-400 font-semibold">W</span>
                        </div>
                        <div class="text-[10px] text-slate-400 mt-1">Optimal avg drain</div>
                    </div>
                    <div class="panel rounded-md p-4 flex flex-col justify-between min-h-[110px] border border-[#1b263b] hover:border-cyan-500/40 transition">
                        <div class="flex items-start justify-between">
                            <span class="text-xs font-semibold text-slate-400">Deep Sleep</span>
                            <span class="w-2 h-2 rounded-full bg-yellow-400 animate-pulse"></span>
                        </div>
                        <div class="mt-2 flex items-end gap-1">
                            <span class="text-3xl font-black text-white leading-none">84</span>
                            <span class="text-xs text-slate-400 font-semibold">%</span>
                        </div>
                        <div class="text-[10px] text-slate-400 mt-1">22 wakeups last cycle</div>
                    </div>
                    <div class="panel rounded-md p-4 flex flex-col justify-between min-h-[110px] border border-[#1b263b] hover:border-cyan-500/40 transition">
                        <div class="flex items-start justify-between">
                            <span class="text-xs font-semibold text-slate-400">Thermal Index</span>
                            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                        </div>
                        <div class="mt-2 flex items-end gap-1">
                            <span class="text-3xl font-black text-white leading-none">A+</span>
                        </div>
                        <div class="text-[10px] text-slate-400 mt-1">Stable delta 4C</div>
                    </div>
                </div>

                <!-- DYNAMIC PAGE BODY -->
                <!-- PAGE: Dashboard (Mission Control) -->
                <div id="page-dashboard" class="page-content grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-8 min-h-[350px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">CPU Telemetry</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">Electronics Analysis</span>
                        </div>
                        <div class="h-64">
                            <canvas id="cpuTimelineChart"></canvas>
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-4 min-h-[350px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Developer CPU Residency</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">Cores</span>
                        </div>
                        <div class="space-y-4 mt-2" id="residency-list">
                            <!-- Injected by JS -->
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-6 min-h-[300px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Battery Overview</h2>
                            <span class="text-[10px] font-bold uppercase text-emerald-400 px-2 py-0.5 bg-emerald-500/10 rounded">Telemetry</span>
                        </div>
                        <div class="flex items-center justify-around h-48">
                            <div class="relative w-36 h-36">
                                <canvas id="batteryRadialChart"></canvas>
                                <div class="absolute inset-0 flex flex-col items-center justify-center">
                                    <span class="text-2xl font-black text-white leading-none">98%</span>
                                    <span class="text-[10px] text-slate-400 mt-1">Health</span>
                                </div>
                            </div>
                            <div class="space-y-2 text-xs">
                                <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded bg-emerald-400"></span> <span>Design Cap: 70Wh</span></div>
                                <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded bg-cyan-400"></span> <span>Current Cap: 68.4Wh</span></div>
                                <div class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded bg-yellow-400"></span> <span>Wear Rate: 2.1%</span></div>
                            </div>
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-6 min-h-[300px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Thermal Limits</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">Metrics</span>
                        </div>
                        <div class="grid grid-cols-2 gap-4 h-48 py-2">
                            <div class="bg-white/5 border border-[#1b263b] rounded p-4 flex flex-col justify-between">
                                <div class="text-xs text-slate-400 font-semibold">Package Temperature</div>
                                <div class="text-3xl font-black text-white leading-none mt-2">42<span class="text-base text-slate-400 font-bold">°C</span></div>
                                <div class="text-[10px] text-slate-500">Cooling Active</div>
                            </div>
                            <div class="bg-white/5 border border-[#1b263b] rounded p-4 flex flex-col justify-between">
                                <div class="text-xs text-slate-400 font-semibold">Core Hotspot</div>
                                <div class="text-3xl font-black text-white leading-none mt-2">68<span class="text-base text-slate-400 font-bold">°C</span></div>
                                <div class="text-[10px] text-slate-500">Below Throttling Limits</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- PAGE: Observability Center -->
                <div id="page-observability" class="page-content hidden grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-8 min-h-[500px] flex flex-col">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Wakeup Analysis Topology</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">Streaming</span>
                        </div>
                        <div class="flex-1 min-h-[350px]">
                            <canvas id="wakeupChart" class="w-full h-full"></canvas>
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-4 min-h-[500px] flex flex-col">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Live Event Console</h2>
                            <span class="text-[10px] font-bold uppercase text-rose-400 px-2 py-0.5 bg-rose-500/10 rounded border border-rose-500/20">Telemetry Ingest</span>
                        </div>
                        <div id="live-console-feed" class="flex-1 overflow-y-auto space-y-2 p-2 bg-[#080d15] rounded border border-[#1b263b] font-mono text-[10px] max-h-[380px] scrollbar-thin">
                            <!-- Injected by JS -->
                        </div>
                    </div>
                </div>

                <!-- PAGE: Diagnostics Hub -->
                <div id="page-diagnostics" class="page-content hidden space-y-4">
                    <div id="diagnostics-feed" class="space-y-4">
                        <!-- Injected by JS -->
                    </div>
                </div>

                <!-- PAGE: Battery Intelligence -->
                <div id="page-battery" class="page-content hidden grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-7 min-h-[350px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Capacity Degradation Curve</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">History</span>
                        </div>
                        <div class="h-64">
                            <canvas id="batteryDegradationChart"></canvas>
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-5 min-h-[350px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Process Write Attribution</h2>
                            <span class="text-[10px] font-bold uppercase text-yellow-400 px-2 py-0.5 bg-yellow-500/10 rounded">Active Drain</span>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead>
                                    <tr class="border-b border-[#1b263b] text-slate-400">
                                        <th class="py-2">Process</th>
                                        <th class="py-2">Active Impact</th>
                                        <th class="py-2">Est. Discharge</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-[#1b263b]/50">
                                    <tr><td class="py-3 font-semibold text-white">Google Chrome</td><td class="py-3 text-rose-400">+4.2W</td><td class="py-3 text-slate-400">1,246 mWh</td></tr>
                                    <tr><td class="py-3 font-semibold text-white">VS Code Helper</td><td class="py-3 text-yellow-400">+2.1W</td><td class="py-3 text-slate-400">899 mWh</td></tr>
                                    <tr><td class="py-3 font-semibold text-white">Discord Desktop</td><td class="py-3 text-yellow-400">+1.5W</td><td class="py-3 text-slate-400">629 mWh</td></tr>
                                    <tr><td class="py-3 font-semibold text-white">System Idle Process</td><td class="py-3 text-emerald-400">&lt;0.1W</td><td class="py-3 text-slate-400">42 mWh</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- PAGE: CPU Analytics -->
                <div id="page-cpu" class="page-content hidden grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-8 min-h-[350px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Package Power Timeline</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">Live Draw</span>
                        </div>
                        <div class="h-64">
                            <canvas id="cpuPowerChart"></canvas>
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-4 min-h-[350px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">P-State Distribution</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">Clocks</span>
                        </div>
                        <div class="h-64">
                            <canvas id="pstateChart"></canvas>
                        </div>
                    </div>
                </div>

                <!-- PAGE: GPU Intelligence -->
                <div id="page-gpu" class="page-content hidden grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-12">
                        <h2 class="text-sm font-bold text-white mb-4">dGPU Wake Attribution</h2>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead>
                                    <tr class="border-b border-[#1b263b] text-slate-400">
                                        <th class="py-2">Process</th>
                                        <th class="py-2">Wakeup Triggers</th>
                                        <th class="py-2">Status</th>
                                        <th class="py-2">Action</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-[#1b263b]/50">
                                    <tr><td class="py-3 font-semibold text-white">NVIDIA Container</td><td class="py-3 text-slate-300">42 wakes/hour</td><td class="py-3 text-rose-400">Aggressive</td><td class="py-3"><button class="px-2 py-1 bg-white/5 rounded border border-[#1b263b] hover:bg-rose-500/20">Restrict</button></td></tr>
                                    <tr><td class="py-3 font-semibold text-white">Steam.exe</td><td class="py-3 text-slate-300">12 wakes/hour</td><td class="py-3 text-yellow-400">Active Context</td><td class="py-3"><button class="px-2 py-1 bg-white/5 rounded border border-[#1b263b] hover:bg-yellow-500/20">Isolate</button></td></tr>
                                    <tr><td class="py-3 font-semibold text-white">Photoshop.exe</td><td class="py-3 text-slate-300">2 wakes/hour</td><td class="py-3 text-slate-400">Idle</td><td class="py-3"><span class="text-slate-500">None required</span></td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- PAGE: Thermal Analytics -->
                <div id="page-thermal" class="page-content hidden grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-8 min-h-[350px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Thermal Saturation Timeline</h2>
                            <span class="text-[10px] font-bold uppercase text-rose-400 px-2 py-0.5 bg-rose-500/10 rounded">Saturation</span>
                        </div>
                        <div class="h-64">
                            <canvas id="thermalSaturationChart"></canvas>
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-4 min-h-[350px]">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Fan Speed Response</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">Acoustics</span>
                        </div>
                        <div class="flex flex-col items-center justify-center h-48 gap-4 mt-8">
                            <div class="text-5xl font-black text-white">1200 <span class="text-base text-slate-400 font-bold">RPM</span></div>
                            <div class="text-xs text-slate-400 uppercase tracking-widest bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded">Acoustic Auto Mode</div>
                        </div>
                    </div>
                </div>

                <!-- PAGE: Event Timeline -->
                <div id="page-timeline" class="page-content hidden space-y-6">
                    <div class="panel rounded-md p-5">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Advanced Event Correlation Timeline</h2>
                            <span class="text-[10px] font-bold uppercase text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">Overlay Canvas</span>
                        </div>
                        
                        <div class="relative h-[480px] rounded border border-[#1b263b] bg-[#070b10] overflow-hidden">
                            <!-- Left Lanes Labels -->
                            <div class="absolute left-0 top-0 z-10 h-full w-48 border-r border-[#1b263b] bg-[#0c1322]">
                                <div class="flex h-[96px] flex-col justify-center border-b border-[#1b263b] px-4">
                                    <span class="text-xs font-bold text-cyan-400">Applications</span>
                                    <span class="text-[9px] text-slate-500 mt-0.5">Foreground activity</span>
                                </div>
                                <div class="flex h-[96px] flex-col justify-center border-b border-[#1b263b] px-4">
                                    <span class="text-xs font-bold text-cyan-400">Hardware State</span>
                                    <span class="text-[9px] text-slate-500 mt-0.5">dGPU/Timer status</span>
                                </div>
                                <div class="flex h-[96px] flex-col justify-center border-b border-[#1b263b] px-4">
                                    <span class="text-xs font-bold text-cyan-400">Thermals</span>
                                    <span class="text-[9px] text-slate-500 mt-0.5">Temp spikes</span>
                                </div>
                                <div class="flex h-[96px] flex-col justify-center border-b border-[#1b263b] px-4">
                                    <span class="text-xs font-bold text-cyan-400">Power Draw</span>
                                    <span class="text-[9px] text-slate-500 mt-0.5">Discharge transients</span>
                                </div>
                                <div class="flex h-[96px] flex-col justify-center px-4">
                                    <span class="text-xs font-bold text-cyan-400">Power State</span>
                                    <span class="text-[9px] text-slate-500 mt-0.5">C-states</span>
                                </div>
                            </div>

                            <!-- SVG Timeline Canvas -->
                            <svg viewBox="0 0 1000 480" class="absolute inset-y-0 left-48 right-0 h-full w-[calc(100%-12rem)]">
                                <!-- Lane divider lines -->
                                <line x1="0" x2="1000" y1="96" y2="96" stroke="rgba(148,163,184,.1)" />
                                <line x1="0" x2="1000" y1="192" y2="192" stroke="rgba(148,163,184,.1)" />
                                <line x1="0" x2="1000" y1="288" y2="288" stroke="rgba(148,163,184,.1)" />
                                <line x1="0" x2="1000" y1="384" y2="384" stroke="rgba(148,163,184,.1)" />
                                
                                <!-- Connection paths -->
                                <path d="M40 340 L360 330 L410 240 L520 260 L710 300 L950 340" stroke="#38bdf8" stroke-width="2.5" fill="none" opacity="0.8" />
                                <path d="M40 240 L360 230 L420 140 L515 160 L650 200 L950 190" stroke="#f87171" stroke-width="2" fill="none" opacity="0.8" />
                                
                                <!-- Events nodes -->
                                <g transform="translate(180, 48)">
                                    <circle r="6" fill="#38bdf8" />
                                    <rect x="12" y="-12" width="120" height="22" rx="3" fill="rgba(12,19,34,.9)" stroke="#38bdf8" stroke-width="1"/>
                                    <text x="18" y="3" fill="#ffffff" font-size="10" font-family="monospace">13:02 Chrome launched</text>
                                </g>
                                <g transform="translate(390, 144)">
                                    <circle r="6" fill="#fbbf24" />
                                    <rect x="12" y="-12" width="130" height="22" rx="3" fill="rgba(12,19,34,.9)" stroke="#fbbf24" stroke-width="1"/>
                                    <text x="18" y="3" fill="#ffffff" font-size="10" font-family="monospace">13:03 dGPU Activated</text>
                                </g>
                                <g transform="translate(560, 240)">
                                    <circle r="6" fill="#f87171" />
                                    <rect x="12" y="-12" width="125" height="22" rx="3" fill="rgba(12,19,34,.9)" stroke="#f87171" stroke-width="1"/>
                                    <text x="18" y="3" fill="#ffffff" font-size="10" font-family="monospace">13:06 High Core Temp</text>
                                </g>
                                <g transform="translate(780, 432)">
                                    <circle r="6" fill="#34d399" />
                                    <rect x="12" y="-12" width="110" height="22" rx="3" fill="rgba(12,19,34,.9)" stroke="#34d399" stroke-width="1"/>
                                    <text x="18" y="3" fill="#ffffff" font-size="10" font-family="monospace">13:12 Idle entered</text>
                                </g>

                                <!-- Red Scrub Line -->
                                <line x1="580" x2="580" y1="0" y2="480" stroke="#f87171" stroke-width="2" stroke-dasharray="4 4" opacity="0.8" />
                            </svg>
                        </div>
                    </div>
                </div>

                <!-- PAGE: Optimization Center -->
                <div id="page-optimization" class="page-content hidden grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-6 border border-[#1b263b] hover:border-cyan-500/40 transition">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Battery Save Profile</h2>
                            <span class="text-[10px] font-bold uppercase text-emerald-400 px-2 py-0.5 bg-emerald-500/10 rounded">Recommended</span>
                        </div>
                        <p class="text-xs text-slate-400 mb-4">Sets CPU min state, turns off RGB, and overrides high-frequency browser timers.</p>
                        <div class="grid grid-cols-3 gap-2 text-[11px] mb-4">
                            <div class="bg-white/5 p-2 rounded"><div class="text-slate-500">Impact</div><div class="font-bold text-emerald-400">-6.4W</div></div>
                            <div class="bg-white/5 p-2 rounded"><div class="text-slate-500">Risk</div><div class="font-bold text-slate-300">Low</div></div>
                            <div class="bg-white/5 p-2 rounded"><div class="text-slate-500">Rollback</div><div class="font-bold text-cyan-400">Supported</div></div>
                        </div>
                        <div class="flex gap-2">
                            <button class="px-3 py-1.5 bg-cyan-500 text-slate-950 font-bold rounded text-xs hover:brightness-110">Apply Profile</button>
                            <button class="px-3 py-1.5 bg-white/5 border border-[#1b263b] rounded text-xs hover:bg-white/10">Dry Run</button>
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-6 border border-[#1b263b] hover:border-cyan-500/40 transition">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-sm font-bold text-white">Gaming Performance</h2>
                            <span class="text-[10px] font-bold uppercase text-rose-400 px-2 py-0.5 bg-rose-500/10 rounded">Max Power</span>
                        </div>
                        <p class="text-xs text-slate-400 mb-4">Forces High Performance power scheme and caps thermal thresholds for maximum stable clock boost.</p>
                        <div class="grid grid-cols-3 gap-2 text-[11px] mb-4">
                            <div class="bg-white/5 p-2 rounded"><div class="text-slate-500">Impact</div><div class="font-bold text-rose-400">+FPS Stable</div></div>
                            <div class="bg-white/5 p-2 rounded"><div class="text-slate-500">Risk</div><div class="font-bold text-yellow-400">Medium</div></div>
                            <div class="bg-white/5 p-2 rounded"><div class="text-slate-500">Rollback</div><div class="font-bold text-cyan-400">Supported</div></div>
                        </div>
                        <div class="flex gap-2">
                            <button class="px-3 py-1.5 bg-cyan-500 text-slate-950 font-bold rounded text-xs hover:brightness-110">Apply Profile</button>
                            <button class="px-3 py-1.5 bg-white/5 border border-[#1b263b] rounded text-xs hover:bg-white/10">Dry Run</button>
                        </div>
                    </div>
                </div>

                <!-- PAGE: Rollback & Safety -->
                <div id="page-safety" class="page-content hidden grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-7">
                        <h2 class="text-sm font-bold text-white mb-4">Rollback History Snapshots</h2>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                                <thead>
                                    <tr class="border-b border-[#1b263b] text-slate-400">
                                        <th class="py-2">Snapshot Time</th>
                                        <th class="py-2">Target Profile</th>
                                        <th class="py-2">Changes Made</th>
                                        <th class="py-2">Status</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-[#1b263b]/50">
                                    <tr><td class="py-3 font-semibold text-white">04:35:12</td><td class="py-3 text-cyan-400">battery</td><td class="py-3 text-slate-300">CPU min + registry key tweaks</td><td class="py-3 text-emerald-400">Active / Safe</td></tr>
                                    <tr><td class="py-3 font-semibold text-white">03:58:44</td><td class="py-3 text-cyan-400">developer</td><td class="py-3 text-slate-300">CPU max state restriction</td><td class="py-3 text-slate-400">Reverted</td></tr>
                                    <tr><td class="py-3 font-semibold text-white">Yesterday</td><td class="py-3 text-cyan-400">silent</td><td class="py-3 text-slate-300">Registry fan thresholds</td><td class="py-3 text-slate-400">Reverted</td></tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="panel rounded-md p-5 col-span-5">
                        <h2 class="text-sm font-bold text-white mb-4">Transaction Guard Details</h2>
                        <div class="space-y-3 text-xs">
                            <div class="flex items-center justify-between p-3 bg-white/5 border border-[#1b263b] rounded">
                                <span>Anti-malware interference blocked</span>
                                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold uppercase text-[9px]">Secured</span>
                            </div>
                            <div class="flex items-center justify-between p-3 bg-white/5 border border-[#1b263b] rounded">
                                <span>Power state snapshot integrity check</span>
                                <span class="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold uppercase text-[9px]">Verified</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- PAGE: Settings -->
                <div id="page-settings" class="page-content hidden grid grid-cols-12 gap-6">
                    <div class="panel rounded-md p-5 col-span-8 space-y-4">
                        <h2 class="text-sm font-bold text-white mb-2">System Parameters</h2>
                        <div class="flex items-center justify-between p-4 bg-white/5 border border-[#1b263b] rounded">
                            <div>
                                <div class="text-xs font-bold text-white">Collect telemetry logs</div>
                                <div class="text-[10px] text-slate-500">Record system power indicators and C-States</div>
                            </div>
                            <div class="w-12 h-6 bg-cyan-500/20 border border-cyan-500/40 rounded-full p-1 cursor-pointer">
                                <div class="w-4 h-4 bg-cyan-400 rounded-full translate-x-6 transition-all"></div>
                            </div>
                        </div>
                        <div class="flex items-center justify-between p-4 bg-white/5 border border-[#1b263b] rounded">
                            <div>
                                <div class="text-xs font-bold text-white">Strict firewall rules</div>
                                <div class="text-[10px] text-slate-500">Enforce strict outbound telemetry blocking for privacy</div>
                            </div>
                            <div class="w-12 h-6 bg-cyan-500/20 border border-cyan-500/40 rounded-full p-1 cursor-pointer">
                                <div class="w-4 h-4 bg-cyan-400 rounded-full translate-x-6 transition-all"></div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </main>
    </div>

    <!-- Live Telemetry Data script -->
    <script>
        // Real gathered data
        const rawTelemetry = __TELEMETRY_JSON__;
        
        // Populate Sidebar active status
        function switchTab(key) {
            // Hide all pages
            document.querySelectorAll('.page-content').forEach(el => el.classList.add('hidden'));
            // Show page
            const targetPage = document.getElementById('page-' + key);
            if(targetPage) targetPage.classList.remove('hidden');

            // Style nav item
            document.querySelectorAll('.nav-item').forEach(el => {
                el.classList.remove('active', 'text-white');
                el.classList.add('text-slate-400');
            });
            const navBtn = document.getElementById('nav-' + key);
            if(navBtn) {
                navBtn.classList.add('active', 'text-white');
                navBtn.classList.remove('text-slate-400');
            }

            // Update Titles
            const titleMap = {
                dashboard: ["Mission Control", "Intelligence Dashboard", "Real-time system diagnostics and optimization posture."],
                observability: ["Global Observatory", "Observability Center", "Live execution telemetry, wakeups, timers, and causality streams."],
                diagnostics: ["Root-Cause Hub", "Diagnostics Hub", "Evidence-based failure explanations with rollback-aware recommendations."],
                battery: ["Battery Lab", "Battery Intelligence", "Deep analytics on degradation, drain attribution, standby loss, and lifespan."],
                cpu: ["Silicon Observatory", "CPU Analytics", "Package power, residency, P-states, interrupts, and scheduling behavior."],
                gpu: ["Residency Control", "GPU Intelligence", "dGPU wakeups, switching events, VRAM context, and rendering load."],
                thermal: ["Thermal Engineering", "Thermal Analytics", "Hotspot tracking, saturation, throttling, and fan-response telemetry."],
                timeline: ["Correlation Lab", "Advanced Event Correlation Timeline", "Linked event overlays across launches, wakeups, drain, timers, and thermals."],
                optimization: ["Controlled Optimization", "Optimization Center", "Explainable, reversible power profiles with expected impact and risk."],
                safety: ["Rollback Ledger", "Rollback & Safety", "Snapshots, transaction logs, config diffs, and validation history."],
                settings: ["Operator Controls", "Settings", "Telemetry configurations and dashboard parameters."]
            };

            if (titleMap[key]) {
                document.getElementById('page-eyebrow').innerText = titleMap[key][0];
                document.getElementById('page-title').innerText = titleMap[key][1];
                document.getElementById('page-desc').innerText = titleMap[key][2];
            }
        }

        // Search log functionality
        function searchLogs() {
            const query = document.getElementById('log-search').value.toLowerCase();
            document.querySelectorAll('.log-item-row').forEach(row => {
                const text = row.innerText.toLowerCase();
                if(text.includes(query)) {
                    row.classList.remove('hidden');
                } else {
                    row.classList.add('hidden');
                }
            });
        }

        // Initialize dynamic contents on page load
        window.addEventListener('DOMContentLoaded', () => {
            lucide.createIcons();

            // 1. Diagnostics and Console Stream
            const consoleFeed = document.getElementById('live-console-feed');
            const diagFeed = document.getElementById('diagnostics-feed');
            const residencyList = document.getElementById('residency-list');
            
            let highCount = 0;
            let medCount = 0;
            let infoCount = 0;

            rawTelemetry.forEach((item, index) => {
                const sev = (item.severity || 'info').toLowerCase();
                if(sev === 'high' || sev === 'critical') highCount++;
                else if (sev === 'medium' || sev === 'warn') medCount++;
                else infoCount++;

                // Append to Event Console
                const consoleRow = document.createElement('div');
                consoleRow.className = 'log-item-row mb-1 p-1 bg-white/5 rounded border border-[#1b263b]/50 flex gap-2';
                
                let colorClass = 'text-cyan-400';
                if(sev === 'high' || sev === 'critical') colorClass = 'text-rose-400';
                if(sev === 'medium' || sev === 'warn') colorClass = 'text-yellow-400';

                consoleRow.innerHTML = `
                    <span class="${colorClass} font-bold select-none">[${sev.toUpperCase()}]</span>
                    <span class="text-slate-300">${item.message}</span>
                `;
                consoleFeed.appendChild(consoleRow);

                // If critical or warning, generate an anomaly card in Diagnostics
                if(sev === 'high' || sev === 'critical' || sev === 'medium' || sev === 'warn') {
                    const diagCard = document.createElement('div');
                    diagCard.className = 'panel rounded-md p-5 border border-[#1b263b] flex justify-between items-center';
                    
                    let badgeBg = sev === 'high' || sev === 'critical' ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' : 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';

                    diagCard.innerHTML = `
                        <div class="space-y-1">
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-0.5 text-[9px] font-black uppercase rounded border ${badgeBg}">${sev}</span>
                                <h3 class="text-sm font-bold text-white">${item.category.toUpperCase()} Diagnostic Flag</h3>
                            </div>
                            <p class="text-xs text-slate-300 mt-2">${item.message}</p>
                            <div class="text-[10px] text-slate-500">Source: ${item.source} | Event index: #${index}</div>
                        </div>
                        <button onclick="switchTab('optimization')" class="px-3 py-1.5 bg-cyan-500 text-slate-950 font-bold rounded text-xs hover:brightness-110">Resolve</button>
                    `;
                    diagFeed.appendChild(diagCard);
                }
            });

            // Adjust health score
            const healthScore = Math.max(45, 100 - (highCount * 15) - (medCount * 5));
            document.getElementById('metric-score').innerText = healthScore;
            document.getElementById('topbar-health').innerText = healthScore + "%";
            
            const hsBadge = document.getElementById('health-value');
            if (healthScore < 80) {
                hsBadge.innerText = "Intervention Advised";
                hsBadge.parentElement.className = "flex items-center gap-2 bg-rose-500/10 text-rose-400 px-3 py-1 rounded text-xs font-bold border border-rose-500/20";
                hsBadge.previousElementSibling.className = "w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse";
            }

            // Fallback for empty diagnostics
            if (diagFeed.children.length === 0) {
                diagFeed.innerHTML = `
                    <div class="panel rounded-md p-8 text-center border border-[#1b263b]">
                        <i data-lucide="check-circle" class="w-8 h-8 text-emerald-400 mx-auto mb-2"></i>
                        <h3 class="text-sm font-bold text-white">No Issues Detected</h3>
                        <p class="text-xs text-slate-500 mt-1">Your system is optimally tuned and showing clean telemetry indicators.</p>
                    </div>
                `;
            }

            // Populate C-State Residency list
            const cStates = [
                { label: "C0 Active", val: 12.4 },
                { label: "C3 Light Sleep", val: 24.1 },
                { label: "C7 Deep Sleep", val: 48.2 },
                { label: "C10 Package Sleep", val: 15.3 }
            ];
            cStates.forEach(c => {
                const item = document.createElement('div');
                item.innerHTML = `
                    <div class="flex justify-between text-xs mb-1.5">
                        <span class="text-slate-400">${c.label}</span>
                        <span class="font-bold text-cyan-400">${c.val}%</span>
                    </div>
                    <div class="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                        <div class="bg-gradient-to-r from-cyan-400 to-blue-500 h-full rounded-full" style="width: ${c.val}%"></div>
                    </div>
                `;
                residencyList.appendChild(item);
            });

            // CHARTS INITIALIZATION
            // Chart 1: CPU Telemetry
            new Chart(document.getElementById('cpuTimelineChart'), {
                type: 'line',
                data: {
                    labels: ['13:00', '13:02', '13:04', '13:06', '13:08', '13:10', '13:12'],
                    datasets: [{
                        label: 'Power Draw (W)',
                        data: [15, 28, 22, 38, 14, 18, 12],
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56, 189, 248, 0.05)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(148, 163, 184, 0.08)' }, ticks: { color: '#64748b' } },
                        x: { grid: { display: false }, ticks: { color: '#64748b' } }
                    }
                }
            });

            // Chart 2: Battery Radial Score
            new Chart(document.getElementById('batteryRadialChart'), {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [98, 2],
                        backgroundColor: ['#34d399', 'rgba(148, 163, 184, 0.08)'],
                        borderWidth: 0
                    }]
                },
                options: {
                    cutout: '80%',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } }
                }
            });

            // Chart 3: Wakeup Analysis
            new Chart(document.getElementById('wakeupChart'), {
                type: 'line',
                data: {
                    labels: ['1s ago', '2s ago', '3s ago', '4s ago', '5s ago', '6s ago', '7s ago', '8s ago', '9s ago', '10s ago'],
                    datasets: [{
                        label: 'Interrupts',
                        data: [120, 240, 580, 860, 430, 220, 760, 1100, 590, 210],
                        borderColor: '#38bdf8',
                        borderWidth: 2,
                        tension: 0.4,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(148, 163, 184, 0.08)' }, ticks: { color: '#64748b' } },
                        x: { grid: { display: false }, ticks: { color: '#64748b' } }
                    }
                }
            });

            // Chart 4: Battery Degradation
            new Chart(document.getElementById('batteryDegradationChart'), {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'Capacity (Wh)',
                        data: [70, 69.8, 69.4, 69.1, 68.8, 68.4],
                        borderColor: '#fbbf24',
                        borderWidth: 2,
                        tension: 0.1,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(148, 163, 184, 0.08)' }, ticks: { color: '#64748b' } },
                        x: { grid: { display: false }, ticks: { color: '#64748b' } }
                    }
                }
            });

            // Chart 5: CPU Power
            new Chart(document.getElementById('cpuPowerChart'), {
                type: 'line',
                data: {
                    labels: ['13:00', '13:02', '13:04', '13:06', '13:08', '13:10', '13:12'],
                    datasets: [{
                        label: 'Power Draw (W)',
                        data: [8, 11, 17, 24, 38, 41, 18],
                        borderColor: '#38bdf8',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(148, 163, 184, 0.08)' }, ticks: { color: '#64748b' } },
                        x: { grid: { display: false }, ticks: { color: '#64748b' } }
                    }
                }
            });

            // Chart 6: P-State Clocks
            new Chart(document.getElementById('pstateChart'), {
                type: 'bar',
                data: {
                    labels: ['P0', 'P1', 'P2', 'P3'],
                    datasets: [{
                        data: [24, 54, 72, 88],
                        backgroundColor: '#38bdf8',
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(148, 163, 184, 0.08)' }, ticks: { color: '#64748b' } },
                        x: { grid: { display: false }, ticks: { color: '#64748b' } }
                    }
                }
            });

            // Chart 7: Thermal Saturation
            new Chart(document.getElementById('thermalSaturationChart'), {
                type: 'line',
                data: {
                    labels: ['10m ago', '8m ago', '6m ago', '4m ago', '2m ago', 'now'],
                    datasets: [{
                        label: 'Temp (°C)',
                        data: [42, 43, 46, 49, 47, 45],
                        borderColor: '#f87171',
                        borderWidth: 2,
                        tension: 0.2,
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(148, 163, 184, 0.08)' }, ticks: { color: '#64748b' } },
                        x: { grid: { display: false }, ticks: { color: '#64748b' } }
                    }
                }
            });
        });
    </script>
</body>
</html>"""


def generate_dashboard(root_dir="."):
    print("     [*] Generating HTML/JS Observability Dashboard...")
    
    reports_dir = os.path.join(root_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # 1. Collect live data
    data = collect_telemetry(root_dir)
    json_payload = json.dumps(data)
    
    # 2. Inject into HTML
    html_content = HTML_TEMPLATE.replace("__TELEMETRY_JSON__", json_payload)
    
    # 3. Save file
    output_path = os.path.join(reports_dir, "dashboard.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"     [+] Dashboard compiled successfully: {output_path}")
    
    # 4. Open in browser
    abs_path = os.path.abspath(output_path)
    file_uri = f"file:///{abs_path.replace(os.sep, '/')}"
    print(f"     [*] Launching browser: {file_uri}")
    webbrowser.open(file_uri)


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    generate_dashboard(root)
