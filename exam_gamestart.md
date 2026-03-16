# Exam: gamestart
# Generated: 2026-02-20
# Total Sprints: 2
# Pass: 60% per sprint | Retakes: unlimited
# Voice-Ready: yes

---

## Sprint 1: Gamescope & Wine
Target: 3 min | Pass: 60% | 20 XP
Voice-compatible: yes

### Q1. [RECALL] Easy — 10 XP
What is gamescope's primary purpose?

- A) A game download manager
- B) A Wayland compositor optimized for gaming with features like VRR and FSR
- C) A Wine replacement
- D) An anti-cheat system

### Q2. [COMPREHENSION] Medium — 10 XP
Why does the launcher kill existing Wine/Gamescope processes before starting?

- A) To free up RAM
- B) To prevent conflicts from orphaned processes affecting the new game session
- C) Wine requires exclusive access to the GPU
- D) It's a Windows requirement

---

## Sprint 2: AMD GPU Optimization
Target: 3 min | Pass: 60% | 20 XP
Voice-compatible: yes

### Q1. [RECALL] Easy — 10 XP
What does DXVK translate DirectX calls to?

- A) OpenGL
- B) Vulkan
- C) Metal
- D) DirectX 12

### Q2. [COMPREHENSION] Medium — 10 XP
The script sets many RADV environment variables. What is RADV?

- A) A game engine
- B) AMD's open-source Vulkan driver in Mesa
- C) A remote desktop protocol
- D) A VR headset

---

## 🔑 Answer Key

### Sprint 1

**Q1. Answer: B** — 10 XP
Hint: It "scopes" games in their own compositor.
Full: Gamescope is a micro-compositor that provides gaming features like variable refresh rate (VRR), FSR upscaling, and display management.

**Q2. Answer: B** — 10 XP
Hint: Orphaned processes can hold resources.
Full: Previous Wine or gamescope processes may hold GPU resources or window focus, causing conflicts. Clean slate ensures reliable launch.

### Sprint 2

**Q1. Answer: B** — 10 XP
Hint: DXVK = DirectX to Vulkan.
Full: DXVK translates DirectX 9/10/11 API calls to Vulkan, enabling Windows games to run efficiently on Linux.

**Q2. Answer: B** — 10 XP
Hint: RADV = Radeon Vulkan.
Full: RADV is AMD's open-source Vulkan driver in the Mesa graphics stack, optimized for RDNA/RDNA2 GPUs.

---

## Study Resources (unlocked after attempt)

- [Gamescope GitHub](https://github.com/ValveSoftware/gamescope)
- [DXVK](https://github.com/doitsujin/dxvk)
