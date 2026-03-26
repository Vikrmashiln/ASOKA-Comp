# ASOKA-Comp

**An open-source, AI-native node-based compositor.**
Built for small studios and independent VFX artists who need professional-grade tools without professional-grade licensing costs.

> *Local-first. AI-native. No subscription. No sorrow.*

---

## The Problem

A small studio running five Nuke seats pays upwards of **$25,000–$30,000 per year** in licensing alone — before a single frame is rendered. Fusion requires DaVinci Resolve as its host. Cloud-based alternatives demand that your client's footage leave your facility.

For small studios, this is not a workflow problem. It is a survival problem.

ASOKA is being built to change that.

---

## What ASOKA Is

ASOKA is a professional node-based compositor designed from the ground up to be:

- **Local-first** — all processing runs on your hardware, on your GPU. Client footage stays in your facility.
- **AI-native** — artificial intelligence is not a plugin or an add-on. It is embedded directly into the compositing pipeline.
- **Open-source** — licensed under Apache 2.0. Free to use, free to modify, free to deploy commercially. Forever.
- **Cloud-capable** — optional AWS integration for burst rendering when local resources are insufficient.

---

## Current Status

ASOKA is in early development. The table below reflects the current build state.

| Component | Status |
|---|---|
| Node-based compositing workspace | 🔨 In Development |
| Local GPU image processing (EXR, JPG, PNG) | 🔨 In Development |
| AI-assisted rotoscoping (local inference) | 📋 Planned — Phase 3 |
| AI-assisted keying (local inference) | 📋 Planned — Phase 3 |
| Natural language node generation | 📋 Planned — Phase 3 |
| AWS cloud-hybrid render pipeline | 📋 Planned — Phase 4 |
| Python scripting API | 📋 Planned — Phase 4 |

---

## Roadmap

### Phase 1 — Foundation *(Active)*
- [x] Repository established under Apache 2.0
- [ ] Node graph workspace launches (NodeGraphQt)
- [ ] Image viewer supporting JPG and EXR
- [ ] Read node: loads an image into the graph

### Phase 2 — Core Compositor
- [ ] Reformat node — GPU-accelerated resize
- [ ] Merge node — over, add, multiply operations
- [ ] Grade node — lift, gamma, gain controls
- [ ] Write node — export to file

### Phase 3 — AI Integration
- [ ] Local AI rotoscoping assist
- [ ] Local AI keying assist
- [ ] Natural language node generation ("add a grade and warm the shadows")

### Phase 4 — Cloud & Extensibility
- [ ] AWS cloud render bridge
- [ ] Community plugin API
- [ ] Pipeline integration tools for small studio environments

---

## Tech Stack

| Layer | Technology |
|---|---|
| Application | Python 3.11+ |
| Node Graph | NodeGraphQt |
| Image Processing | Kornia (GPU-accelerated) |
| AI Inference | PyTorch (local) |
| Cloud Rendering | AWS (Phase 4) |

---

## Why Apache 2.0

Apache 2.0 was chosen deliberately. It includes an explicit patent grant, which means studios and their legal teams can adopt, integrate, and build on ASOKA without licensing risk. Open-source only works if it is safe to use professionally.

---

## Contributing

ASOKA is at an early stage. Contributions from both developers and VFX professionals are welcome and needed.

**For developers:**
- Review open [Issues](https://github.com/Vikrmashiln/ASOKA-Comp/issues) for tasks tagged `good first issue`
- Fork the repository, create a feature branch, and submit a pull request
- Follow PEP 8 style guidelines for Python contributions

**For VFX artists and studio leads:**
- Open an [Issue](https://github.com/Vikrmashiln/ASOKA-Comp/issues) describing a workflow problem you want ASOKA to solve
- Start a [Discussion](https://github.com/Vikrmashiln/ASOKA-Comp/discussions) to share how your studio currently handles compositing
- Your operational knowledge is as valuable as code

---

## Design Principles

1. **Facility security first.** Client footage must never leave the artist's machine without explicit action.
2. **AI as infrastructure, not novelty.** Every AI feature must solve a real compositing problem faster than the manual alternative.
3. **Zero licensing cost, always.** No freemium tiers. No enterprise paywalls. Apache 2.0 in perpetuity.
4. **Built by practitioners.** Feature decisions are made by working VFX artists, not product managers.

---

## License

[Apache 2.0](LICENSE) — free to use, modify, and distribute, including for commercial studio use.

---

## Contact

Maintained by [@Vikrmashiln](https://github.com/Vikrmashiln) — VFX artist and ASOKA project lead.

For questions, partnership inquiries, or studio feedback: [open an issue](https://github.com/Vikrmashiln/ASOKA-Comp/issues) or start a [Discussion](https://github.com/Vikrmashiln/ASOKA-Comp/discussions).
