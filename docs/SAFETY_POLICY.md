# PowerTune Safety & Ethics Policy

> **The 50 Rules of Professional System Optimization**

This document serves as the constitution for the PowerTune project. It defines the strict boundary between a "trusted engineering tool" and a "dangerous optimizer script." Every pull request, feature, and tweak must adhere strictly to these principles.

---

## 🔥 CATEGORY 1 — SYSTEM DAMAGE RISKS
**We never implement changes that risk system stability.**
1. **Breaking Windows Boot**: Never delete boot configs, modify BCD recklessly, or disable critical boot services.
2. **Disabling Essential Services**: Never touch RPC, DCOM, PlugPlay, Windows Audio, DHCP, or Winmgmt.
3. **Registry Corruption**: Never mass-delete registry keys or apply undocumented tweaks blindly.
4. **Permanent Irreversible Changes**: Every single change MUST support rollback, snapshot, and restore operations.
5. **Damaging Power Profiles**: Avoid configurations that prevent sleep, overheat the CPU, or reduce performance unexpectedly.
6. **Disabling Security Completely**: Never permanently disable Defender, silently disable the firewall, or block security updates.
7. **Breaking Windows Update**: Never permanently disable update services or corrupt the servicing stack.
8. **Causing Thermal Instability**: Never implement changes that overheat laptops or reduce hardware lifespan.
9. **Aggressive CPU Undervolting**: Avoid unsupported undervolting that can cause BSODs or resume failures.
10. **Causing Battery Calibration Issues**: Never manipulate battery firmware or fake charge states.

## 🔥 CATEGORY 2 — PERFORMANCE FALSE CLAIMS
**We measure and explain; we do not sell snake oil.**
11. **Fake RAM Cleaning**: No `EmptyWorkingSet` scripts. They worsen performance by forcing page faults.
12. **Fake FPS Boost Claims**: No "999% FPS BOOST" marketing. We benchmark, measure, and explain.
13. **Placebo Tweaks**: No "internet speed boost registry" hacks or "quantum TCP optimization".
14. **Fake CPU Optimization**: Do not manipulate priorities blindly without measuring the actual impact.

## 🔥 CATEGORY 3 — SECURITY RISKS
**We respect user data and security.**
15. **Running Untrusted Commands**: Never download remote scripts silently or execute arbitrary URLs.
16. **Credential Exposure**: Never log passwords, tokens, or browser secrets in our reports.
17. **Unsafe Admin Escalation**: Avoid hidden UAC bypasses or privilege escalation tricks.
18. **Telemetry Without Consent**: If collecting diagnostics, anonymize the data and ask for permission.
19. **Exposing Sensitive System Info**: Never publicly expose serial numbers, MAC addresses, or usernames in generated reports.

## 🔥 CATEGORY 4 — USER EXPERIENCE FAILURES
**We respect the user's intelligence.**
20. **No Rollback**: We ALWAYS support undo and restore.
21. **No Explanation**: Never just say "Optimization applied." Always explain *why* (e.g., "CPU minimum state reduced from 100% to 5%").
22. **Scary Console Spam**: Console outputs must be readable, formatted, and show progress.
23. **Silent Failures**: If something fails, explain why and suggest fixes.
24. **Over-Aggressive Defaults**: Never assume the user wants maximum battery or RGB off. Use profiles to let the user choose.

## 🔥 CATEGORY 5 — ARCHITECTURE FAILURES
**We are a systems-engineering tool, not a script kiddie repo.**
25. **Monolithic Scripts**: Avoid 5000-line PowerShell monsters. Use modular, YAML-driven design.
26. **Hardcoded Vendor Logic**: ASUS, Lenovo, and Dell require different, dedicated handling modules.
27. **No Compatibility Checks**: Must detect unsupported hardware, OS versions, or missing commands before running.
28. **No Logging**: We require structured JSON logs, timestamps, and operation tracking.
29. **No Test Framework**: Commits must pass tests to ensure rollbacks don't fail.
30. **Unclear Codebase**: No undocumented magic or random scripts.

## 🔥 CATEGORY 6 — POWER MANAGEMENT RISKS
**We understand modern Windows ACPI.**
31. **Preventing Sleep States**: Never apply tweaks that keep the CPU awake or destroy idle battery.
32. **Breaking Connected Standby**: Modern laptops rely on S0 sleep; never break it unknowingly.
33. **Disabling ASPM Incorrectly**: PCIe ASPM mistakes hurt battery life severely.
34. **Forcing High Timer Resolution**: Never accidentally keep the system timer at 1ms.
35. **dGPU Wakeups**: Improper handling keeps the NVIDIA/AMD dGPU active constantly, draining ~15W at idle.

## 🔥 CATEGORY 7 — OPEN SOURCE FAILURES
**We build a sustainable community.**
36. **No Documentation**: We maintain architecture docs, tuning rationale, and examples.
37. **No Contribution Guidelines**: PRs must follow our strict evidence-based rules.
38. **Unsafe Community Scripts**: Never merge unreviewed registry hacks.
39. **Unsupported Myths**: Avoid internet "gaming mode" nonsense.
40. **Benchmark Manipulation**: Never fake battery gains, FPS, or thermals.

## 🔥 CATEGORY 8 — LEGAL & ETHICAL RISKS
**We operate above board.**
41. **Violating Vendor Terms**: Be careful with proprietary firmware manipulation.
42. **Misleading Claims**: Never promise "battery doubled" or "fixes all laptops."
43. **Dangerous Kernel Tweaks**: Avoid undocumented kernel patches or memory hacks.
44. **Hidden Persistence**: Never secretly install background services or hidden tasks.
45. **Anti-User Behavior**: Never lock users into a profile or prevent manual control.

## 🔥 CATEGORY 9 — REPUTATION KILLERS
**We maintain professional credibility.**
46. **Looking Like Malware**: No obfuscation, hidden actions, or unexplained binaries.
47. **Over-Marketing**: Explain technically. Avoid hype.
48. **Copy-Pasted Internet Tweaks**: Every tweak must be individually vetted.
49. **No Evidence-Based Engineering**: Every single tweak must definitively answer: *Why does this help?*
50. **"One Script Fits All"**: Hardware, workloads, and vendors differ. We require dynamic tuning.

---

### 🧠 The Golden Rule
A professional optimization tool behaves like a diagnostics platform, an observability tool, and a controlled tuning framework—not a "magic performance booster."
