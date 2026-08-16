# ilming Platform Architecture & Flow Documentation

> **Demo page:** [ilming.io/demo-platform/](https://ilming.io/demo-platform/)  
> **Product video:** [ilming.io/ilming.mp4](https://ilming.io/ilming.mp4) (embedded on demo page)  
> **Presenter script:** [app.ilming.io/demo-guide](https://app.ilming.io/demo-guide)

Last updated: August 2026

---

## 1. Executive Summary

**ilming** is a multi-tenant Islamic Learning Management System (LMS) for madrassas, schools, and Tahfiz institutes. The platform consists of four repositories:

| Repository | Type | URL | Purpose |
|------------|------|-----|---------|
| **Ilming-api** | Backend API | `api.ilming.io` | Single source of truth — auth, academics, exams, tahfiz, fees, messaging |
| **Ilming-crm** | Web app (Next.js) | `app.ilming.io` | Role-based portals for admin, institute, teacher, student, guardian |
| **Ilming-student-mobile** | Mobile app (Expo) | iOS / Android | Student-first Tahfiz practice + academy features; guardian mode |
| **ilming** | Marketing site | `ilming.io` | Positioning, pricing, blog, demo documentation |

**Regions:** UK, UAE, India, GCC  
**Languages:** English, Arabic (RTL), Urdu, and 7+ more

---

## 2. System Architecture

```
┌─────────────────┐     HTTPS/REST      ┌──────────────────┐
│  Ilming-crm     │ ──────────────────► │   Ilming-api     │
│  (Next.js)      │     JWT + cookies   │   (Express)      │
│  app.ilming.io  │ ◄── Socket.IO ────► │   api.ilming.io  │
└─────────────────┘                     └────────┬─────────┘
                                                 │
┌─────────────────┐     HTTPS/REST              │ MongoDB
│ Ilming-student- │ ────────────────────────────┤ Redis
│ mobile (Expo)   │     Bearer JWT + Socket.IO  │ S3/GCS
└─────────────────┘                             Firebase FCM
```

### Ilming-api (Backend)

- **Stack:** Node.js 24+, Express 4, TypeScript, MongoDB (Mongoose), Redis, BullMQ, Socket.IO
- **Entry:** `src/start.ts` → port 8080
- **Routes:** 52 modules under `/api/*`
- **Models:** 53 Mongoose schemas
- **Auth:** JWT + bcrypt, httpOnly refresh cookie (`authToken`)
- **AI:** OpenAI (Whisper for recitation, chat, quiz generation)
- **Deploy:** Docker + PM2 on AWS Lightsail (`me-central-1`), Helm chart available

### Ilming-crm (Web Frontend)

- **Stack:** Next.js 15, React 19, Redux Toolkit + Saga, Tailwind 4
- **Routes:** 129 pages under role prefixes (`/admin`, `/institute`, `/teacher`, `/student`, `/guardian`)
- **API client:** Axios with CSRF, token refresh, request caching
- **Real-time:** Socket.IO for messaging; WebSocket for exam proctoring
- **i18n:** next-intl (10+ languages)

### Ilming-student-mobile

- **Stack:** Expo SDK 57, React Native 0.86, Expo Router
- **Auth:** SecureStore for JWT
- **Hero feature:** Virtual Ustadh — live Socket.IO practice with AI scoring
- **Tabs:** Home, Hifz, Sabk (center mic), Academy, More
- **Guardian mode:** Separate tab bar with child picker

---

## 3. User Roles

| Role | API `user.role` | CRM Portal | Key capabilities |
|------|-----------------|------------|------------------|
| Platform admin | `admin` | `/admin/` | Multi-institute oversight, packages, CMS |
| Institute admin | `institute` | `/institute/` | Full institute ops, addons, branding |
| Sub-admin staff | `subadmin` | `/institute/` | Scoped by `staffPermissions` |
| Teacher | `tutor` | `/teacher/` | Assigned batches, exams, tahfiz review |
| Student | `student` | `/student/` | Exams, materials, tahfiz, fees |
| Guardian | `guardian` | `/guardian/` | Linked students, progress, fees |

### Institute Addon Gating

Institutes enable modules via `/institute/addons`:

| Addon | Modules |
|-------|---------|
| `academics` | courses, subjects, batches, teachers, students, families, import |
| `tahfiz` | tahfiz desk, attendance |
| `learning` | course materials |
| `exams` | questions, exams, results, certificates |
| `communication` | messages, notifications, live meetings |
| `finance` | fees, payouts (default off) |

---

## 4. Tahfiz / Recitation Flow (Core Differentiator)

### API Endpoints (`/api/recitation`)

| Actor | Key endpoints |
|-------|---------------|
| Teacher | `POST /assignments`, `GET /queue`, `POST /attempts/:id/review` |
| Student | `GET /assignments/mine`, `POST /attempts`, `GET /revision` |
| Institute | `GET /institute/overview`, `GET /institute/weekly-trend` |
| Guardian | `GET /progress/:studentId`, `GET /weekly-report`, `GET /term-report` |

### End-to-End Sequence

1. **Teacher/Institute** creates assignment (surah, ayah range, due date, optional reference audio)
2. **Student** sees assignment in Tahfiz desk (web `/student/tahfiz` or mobile `/practice/[id]`)
3. **Student** records recitation via microphone
4. **API** sends audio to OpenAI Whisper → word-match scoring → instant feedback
5. If score passes gate → attempt enters **teacher review queue**
6. **Teacher** plays audio, approves or requests re-record
7. **Student** receives push notification on approval (`practice:approval` socket event)
8. **Revision plan** auto-updates; **Hifz progress** stats recalculate
9. **Guardian** sees progress + weekly AI report

### Socket.IO Events (Live Practice)

| Direction | Event | Purpose |
|-----------|-------|---------|
| Client → Server | `practice:join`, `practice:start`, `practice:level`, `practice:stop` | Join session, stream audio levels |
| Server → Client | `practice:update`, `practice:complete`, `practice:approval`, `practice:error` | Live feedback, final score, teacher approval |

---

## 5. Authentication Flow

### Web (Ilming-crm)

1. `POST /auth/login` with email + password
2. Response: user object + optional Bearer token
3. httpOnly refresh cookie set automatically (`withCredentials: true`)
4. Redux stores user; redirect to role dashboard
5. On 401: Axios interceptor calls `POST /auth/refresh` → retries request
6. Logout: `POST /auth/logout` + clear storage

### Mobile (Ilming-student-mobile)

1. `POST /auth/login` → JWT stored in SecureStore
2. `GET /auth/profile` on app launch to validate session
3. `AuthGate` routes by role: student → `/(tabs)`, guardian → `/(guardian-tabs)`
4. Push token registered via `POST /notification/update-fcm-token`

### OAuth

- Google/Facebook via `POST /oauth/google`, `POST /oauth/facebook`

---

## 6. Key User Journeys

### Institute Onboarding

```
Book demo → Platform admin creates institute → Institute admin login
→ Enable addons → Setup courses/batches → Enroll students + guardians
→ Daily operations (exams, tahfiz, fees, live classes)
```

### Student Exam Flow

1. Institute/teacher creates exam + question paper
2. Exam published to student portal
3. Student takes exam at `/student/examPage/[id]` (web) or `/exam/[id]` (mobile)
4. Attempts auto-saved; proctoring via WebSocket (web)
5. Teacher reviews → publishes results
6. Student downloads certificate if enabled

### Fee Payment

1. Institute sets fee structure
2. Student/guardian sees pending fees
3. `POST /fees/pay/order` → Razorpay checkout (WebView on mobile)
4. `POST /fees/pay/verify` on success

### Guardian Family Invite

1. Institute creates family + sends invite
2. Guardian receives link: `/auth/family-invite/:token`
3. Guardian registers/logs in → `POST /auth/accept-family-invite`
4. Linked students appear in guardian portal

---

## 7. API Module Reference

| Prefix | Module |
|--------|--------|
| `/api/auth` | Register, login, refresh, password reset, profile, family invites |
| `/api/institute` | Institutes, settings, addons, families, live meetings |
| `/api/course`, `/api/subject`, `/api/batch` | Academic hierarchy |
| `/api/student`, `/api/tutor`, `/api/guardian` | People management |
| `/api/exam`, `/api/attempt`, `/api/result` | Exam lifecycle |
| `/api/recitation` | Tahfiz / Hifz workflow |
| `/api/tahfiz-attendance` | Tahfiz attendance |
| `/api/certificate` | PDF certificates + public verification |
| `/api/fees` | Fee structures, Razorpay payments |
| `/api/notification`, `/api/message`, `/api/communication` | Alerts & messaging |
| `/api/chat`, `/api/ai` | AI chat, quiz generation, recommendations |
| `/api/plan`, `/api/package`, `/api/subscription` | SaaS billing |

Full Swagger docs: `https://api.ilming.io/api-docs`

---

## 8. Module Coverage Matrix

| Module | API | CRM Web | Mobile |
|--------|-----|---------|--------|
| Tahfiz / Recitation | ✓ | ✓ | ✓ |
| Exams & results | ✓ | ✓ | ✓ |
| Course materials | ✓ | ✓ | ✓ |
| Live meetings | ✓ | ✓ | ✓ |
| Messaging | ✓ | ✓ | ✓ |
| Fees (Razorpay) | ✓ | ✓ | ✓ |
| Certificates | ✓ | ✓ | ✓ |
| Guardian portal | ✓ | ✓ | ✓ |
| Institute admin | ✓ | ✓ | — |
| Teacher tools | ✓ | ✓ | — |
| Bulk import | ✓ | ✓ | — |
| Platform admin | ✓ | ✓ | — |

---

## 9. Demo Quick Reference

### URLs

| Service | URL |
|---------|-----|
| CRM | https://app.ilming.io |
| API | https://api.ilming.io |
| Demo script | https://app.ilming.io/demo-guide |
| Platform flow doc | https://ilming.io/demo-platform/ |

### Credentials

| Role | Email | Password | Start page |
|------|-------|----------|------------|
| Student | `student@sanadacademy.com` | `student123` | `/student/tahfiz` |
| Teacher | `tutor1@sanadacademy.com` | `tutor123` | `/teacher/tahfiz` |
| Parent | `parent@sanadacademy.com` | `parent123` | `/guardian/tahfiz` |
| Institute | `admin@ilming.com` | `institute123` | `/institute/tahfiz` |

### 15-Minute Demo Path

1. **Institute** → Tahfiz overview (2 min)
2. **Teacher** → Create assignment (2 min)
3. **Student** → Guided practice + AI score (5 min) ← hero moment
4. **Teacher** → Review + approve (2 min)
5. **Parent** → Progress + weekly report (2 min)
6. **Optional** → Exams, fees, mobile app (2 min)

### Pre-Demo Checklist

- [ ] Chrome browser (microphone required)
- [ ] Allow mic when prompted
- [ ] Open demo-platform page + CRM demo-guide in tabs
- [ ] Log out between role switches
- [ ] Seeded data verified (student assignments, teacher pending review)

---

## 10. Local Development

```bash
# Terminal 1 — Marketing site
cd ilming && python3 -m http.server 8000

# Terminal 2 — CRM
cd Ilming-crm && pnpm dev          # :3000

# Terminal 3 — API
cd Ilming-api && pnpm dev          # :8080

# Terminal 4 — Mobile (optional)
cd Ilming-student-mobile && pnpm start
```

| Env var | Local default |
|---------|---------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8080/api` |
| `EXPO_PUBLIC_API_URL` | `https://api.ilming.io/api` (or local) |
| `EXPO_PUBLIC_SOCKET_URL` | `http://localhost:8080` |

---

## 11. Deployment

| Component | Host | Region |
|-----------|------|--------|
| ilming.io | Static hosting | — |
| app.ilming.io | Ilming-crm (standalone Next.js) | AWS Lightsail |
| api.ilming.io | Ilming-api (Docker + PM2) | AWS Lightsail `me-central-1` |

---

## 12. Roadmap (Phase 2)

- Deeper acoustic Tajweed analysis (Makharij, Madd, Waqf)
- Hifz sync improvements between web and mobile
- Video avatar for Virtual Ustadh
- WhatsApp fee reminders
- Printable term reports (UI exists, full PDF pipeline pending)

---

## Related Documentation

- `Ilming-api/README.md` — API setup and env vars
- `Ilming-api/DATABASE_STRUCTURE.md` — MongoDB schema reference
- `Ilming-crm/README.md` — CRM setup
- `Ilming-crm/src/data/demoGuideContent.ts` — Full presenter script (EN/AR)
- `ilming/README-ILMING.md` — Marketing site guide
