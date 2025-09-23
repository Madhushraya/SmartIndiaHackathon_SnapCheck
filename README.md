# 📸 SnapCheck

> **AI-powered, fraud-proof attendance system** — combining **Face ID + device binding + geolocation / proximity checks** and adaptive verification for **offline (in-person)** and **online (remote)** classes.
> **One student → One device → One face.**

---

## 🚀 One-line

**Face ID + Device Binding + Context-aware checks (BLE/RSSI / GPS / Continuous liveness) — secure attendance for hybrid classrooms.**

---

## 🔑 Key Features

* One-time registration (username, email, password, face scan)
* Persistent login (app stays logged in unless explicitly logged out)
* **Offline (in-person)** mode: Face ID + liveness + device binding + proximity checks (BLE+RSSI or micro-geofence) + session window
* **Online (remote)** mode: Face ID + initial liveness + continuous/random re-checks + engagement signals for final attendance scoring
* Optional teacher controls: start/stop session, broadcast rotating token (BLE) or display rotating QR on projector
* Device binding with proof-of-possession (token or signed nonce) and device management (list/revoke/rebind)
* Audit trails, evidence storage (images/embeddings), and analytics dashboard

---

## Why SnapCheck?

Manual registers are time-consuming and prone to proxy attendance. SnapCheck removes roll-calls and adds strong, layered identity & presence verification while keeping UX smooth for students and teachers.

---

## How it works — Modes & Validation Pipelines

### Offline (in-person) — Primary flow

**Goal:** prove the user is *the right person* and *physically in the classroom*.
**Checks required (recommended):**

1. **Device binding** (device registered to user)
2. **Face ID + liveness** (one-shot at check-in)
3. **Session active & time window** (attendance only allowed during the set time)
4. **Proximity evidence** — one or more of:

   * **BLE rotating token + RSSI threshold** (teacher device advertises ephemeral token; student detects token and RSSI must be above threshold), OR
   * **Micro-geofence** (accurate indoor location / seat beacon), OR
   * **Projector-QR fallback** (rotating QR shown by teacher; used when BLE fails)
5. **Optional mid-class re-check** to prevent "mark-and-leave".

**Result:** If all checks pass → mark `present`. If weak evidence → `tentative` / `flagged` for teacher review.

---

### Online (remote) — Primary flow

**Goal:** verify identity remotely and measure engagement to avoid proxy/video spoofing.
**Checks recommended:**

1. **Device binding**
2. **Initial Face ID + liveness** at join
3. **Session join only via SnapCheck (WebRTC/in-app)** so camera is controlled by SnapCheck
4. **Random / continuous re-checks** during class (blink/turn-head prompt or sampled frame verification)
5. **Engagement signals** (window focus, heartbeat, short in-class interactions/polls)
6. **Attendance scoring**: compute `attendance_score = passed_checks / attempted_checks`. If `score >= threshold` (e.g., 0.7) → present; else flagged for review.

**Result:** Determination can be immediate (if policy allows) or computed at session end.

---

## Teacher controls & fallbacks

* **Start session** (choose `mode: offline | online`)
* **Broadcast BLE rotating token** (teacher phone or small beacon) + optional projector rotating QR (visual fallback)
* **Teacher mobile app**: start/stop session, see live attendee list, approve flagged cases
* **Fallbacks**: PIN announced by teacher, QR, or teacher verification UI if student device fails checks

---

## Security & anti-spoofing (summary)

* **Device binding**: per-device token or public key stored server-side (challenge-response proof)
* **Face + liveness**: models to detect replay/photo/video spoofing; random prompts for online mode
* **Rotating ephemeral tokens**: BLE / QR rotate every 15–30s (HMAC(seed, slot)), server-side validation to prevent replay
* **RSSI filtering**: block weak BLE signals to avoid doorway detection (tune per environment)
* **One-time use / replay protection**: server marks token use and prevents reuse
* **Audit logs & evidence**: store short-lived images/embeddings, logs for disputes (configure retention policy)

---

## Minimal API schemas (examples)

### Start session

`POST /session/start`
Payload:

```json
{
  "course_id": 45,
  "mode": "offline",       // or "online"
  "start": "2025-09-25T09:00:00Z",
  "end": "2025-09-25T09:15:00Z",
  "require_proximity": true
}
```

Return includes `session_id` and server `seed` for rotating tokens.

---

### Attendance check (offline example)

`POST /attendance/check` (multipart/form-data)

* `session_id`
* `device_id`
* `device_proof` (signature or device token)
* `face_image` (or embedding)
* `face_liveness_result` (pass/score)
* `ble_token` (optional)
* `ble_rssi` (optional)
* `timestamp` (ISO)

Server actions: validate device, validate face & liveness, recompute/validate HMAC token using session seed & timeslot, check RSSI threshold, check time-window → mark present/tentative/flagged.

---

### Attendance check (online example)

`POST /attendance/check`

* `session_id`
* `device_id`
* `device_proof`
* `face_image` (or embedding)
* `face_liveness_result`
* `check_type`: `join` or `recheck`
* `engagement_metrics` (optional: focus, mic activity)
  Server records each check. Final attendance decision based on aggregate.

---

## Tech stack (recommended)

* Frontend: React (dashboard), React Native 
* Backend: FastAPI (Python) or Node (Express/Fastify)
* DB: PostgreSQL + pgvector (embeddings)
* Storage: S3 (images/evidence)
* Face models: FaceNet / ArcFace or `face_recognition` for prototype; liveness models as a service or model inference
* Deployment: Docker + docker-compose, GitHub Actions CI

---

## Quick install (dev)

```bash
# Backend (example FastAPI)
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

---

## Demo checklist (before you present)

* Teacher session flow tested (start session, broadcast BLE / show rotating QR)
* Student devices registered + device tokens / keypairs provisioned
* Sample user accounts with face images pre-registered for quick demo
* Demo fallback (rotating QR on projector) recorded as video in case BLE advertising has issues on iOS
* Dashboard live updates working (attendance shows up)

---

## Roadmap / optional enhancements

* Seat-level beacons for stricter micro-location
* Advanced liveness (continuous face tracking)
* LMS / SIS integration (Moodle, ERP)
* Notifications to parents/guardians with opt-in
* Edge inference (embeddings on-device) to reduce server load

---

## Team & Contact

Built by **Team \[Your Team Name]** for SIH (Project PS Number: SIH25016) — SnapCheck.
GitHub: `https://github.com/your-username/snapcheck`
Contact: `your.email@example.com`

---

## License

MIT License — see `LICENSE` file.

---
