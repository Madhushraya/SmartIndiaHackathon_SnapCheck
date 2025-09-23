
---

# 📸 SnapCheck

> **AI-powered, fraud-proof attendance system** — combining **QR codes, geolocation, and Face ID with liveness detection** to make college attendance secure, seamless, and tamper-free.
>
> **One student → One device → One face.**

---

## 🚀 Overview

SnapCheck is a **smart attendance monitoring system** built for colleges.
Students register **once** with their credentials and face image. After that, they remain logged in unless they explicitly log out.

When marking attendance:

1. Student must be inside the **authorized campus location** (geo-fenced).
2. Student scans a **dynamic QR code** shown in class.
3. System verifies identity with **Face ID + liveness detection** to prevent proxies.

✅ No roll calls.
✅ No manual registers.
✅ No proxy attendance.

---

## 🔑 Key Features

* **One-time Registration** → username, email, password, face scan.
* **Persistent Login** → stays logged in until user logs out.
* **Attendance Marking**

  * Works only in campus (geo-fenced).
  * Requires scanning session-specific QR code.
  * Validated with **Face ID + liveness detection**.
* **Proxy Prevention** → one device = one student ID = one face.
* **Analytics Dashboard** → teachers get real-time reports, attendance trends, and alerts.
* **Audit & Security**

  * Anti-spoofing checks (photo/video attacks blocked).
  * Encrypted storage and secure API endpoints.

---

## 🏗️ System Architecture (High-level)

```
[ Student App ]
   |  (QR scan + Face ID + Geo)
   v
[ Backend API ]  <-- JWT Auth + Liveness Detection + Geo Validation
   | 
   v
[ Database ]  <-- Students, Attendance Logs, Device Binding
   |
   v
[ Admin Dashboard ] <-- Analytics, Reports, Exports
```

---

## 💻 Tech Stack

**Frontend**

* React (TypeScript) for web dashboards
* React Native / PWA for student mobile app
* TailwindCSS + Recharts for UI & charts

**Backend**

* FastAPI (Python) or Node.js (Express)
* PostgreSQL + pgvector (for embeddings & search)
* JWT-based authentication
* Face recognition (FaceNet/ArcFace) + liveness detection model

**Infrastructure**

* Docker + Docker Compose
* S3-compatible storage (for images)
* CI/CD with GitHub Actions

---

## 📲 Usage Flow

**Student side**

1. Register account → username, email, password, face scan.
2. Login → only required once (session stays active).
3. In class → scan QR code shown by teacher.
4. System checks → location + Face ID + liveness.
5. Attendance marked ✅

**Admin side**

1. Create sessions & generate QR codes.
2. View live attendance dashboard.
3. Export monthly/weekly reports.
4. Spot absentee patterns and fraud attempts.

---

## ⚡ Installation (for local dev)

```bash
# clone repo
git clone https://github.com/your-username/snapcheck.git
cd snapcheck

# backend setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend setup
cd frontend
npm install
npm run dev
```

---

## 📊 Example Screens (to add later)

* ✅ Student registration page
* ✅ QR scan + face verification
* ✅ Admin dashboard (attendance % graph, heatmap, reports)



---

## 🔮 Future Enhancements

* Push notifications for students (reminders for classes).
* Integration with LMS/ERP systems.
* Advanced liveness detection (eye-blink/motion tracking).
* Multi-device admin monitoring.

---

## 👨‍💻 Team

Built as part of **Smart India Hackathon 2025** by Team *\[Your Team Name]*.

---

## 📜 License

MIT License — feel free to use and adapt for research or educational purposes.

---
