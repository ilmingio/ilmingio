# Proposal team — Quran AI / OpenAI cost

Internal only. Not a customer price list.

**Rule:** A one-time payment must not include unlimited Quran AI. Whisper is billed every time a student records. At 500+ students we cannot afford “AI included forever”.

---

## What we pay (our cost)

| Service | When it runs | What OpenAI charges us |
| --- | --- | --- |
| **Whisper** (`whisper-1`) | Each Record & submit | **$0.006 per minute** of audio |
| **GPT coach** | Same submit (short text) | ~**$0.0002** per attempt |
| Word-match score | On our server | **$0** |

Typical student: 40s clip × 4 times/school day × 22 days ≈ **59 audio minutes / month** → **~$0.38 we pay per reciting student / month**.

Heavy retries: ~**$0.82** / student / month. Long 2-minute clips many times a day: **~$2+** / student / month.

---

## Our OpenAI bill by institute size

| Reciting students | Typical / month | Typical / year | Heavy / month |
| --- | --- | --- | --- |
| 50 | $19 | $228 | $41 |
| 150 | $56 | $675 | $123 |
| **500** | **$188** | **$2,250** | **$410** |
| 1,000 | $375 | $4,500 | $820 |

If 500 students all use practice, we pay OpenAI **about $2,250 every year** on typical use — **after** any one-time fee is already spent.

---

## Why one-time + 500 students fails

Example: **$5,000 one-time** and “AI included”.

| Usage | OpenAI / month | $5,000 lasts | Then |
| --- | --- | --- | --- |
| Typical | $188 | ~26 months | We pay from our pocket forever |
| Heavy | $410 | ~12 months | Same |
| Long retries | $1,077 | ~5 months | Fee gone in one term |

A **$2,000** all-in quote lasts **~10 months** of typical 500-student AI use.

---

## What may be one-time vs recurring

| Item | One-time OK? | Bill as |
| --- | --- | --- |
| Setup, training, import | Yes | Implementation |
| LMS (attendance, exams, fees) | Only with an end date | Annual licence preferred |
| **Quran AI / Whisper** | **No — not unlimited** | Monthly/yearly + cap, or prepaid credits that run out |

---

## What to charge the client (selling price)

About **4× our cost**. Fair use: **80 recitations / student / month**. Extra: **$0.02** each.

| Active AI students | Monthly quote |
| --- | --- |
| Up to 50 | $49 |
| 51–150 | $149 |
| 151–300 | $279 |
| 301–500 | $449 |
| 500+ | **$0.90 / student** (500 × $0.90 = $450 / mo) |

---

## Paste into the proposal

> Quran AI usage: student recitations are transcribed with OpenAI Whisper ($0.006 per audio minute). This is a **recurring usage fee**, not part of the one-time implementation. For up to 500 reciting students: **$449 / month**, including 80 scored recitations per student per month. Additional recitations $0.02 each.

**Never write:** lifetime AI, unlimited practice inside the one-time fee, AI free forever after setup.

If they insist on paying AI once: sell a **prepaid credit pack** (e.g. $3,000 ≈ 4 months typical for 500 students). When credits hit zero, AI scoring pauses until they top up. Do not call that lifetime.

---

Rates: OpenAI public list, Aug 2026. Re-check [platform.openai.com/docs/pricing](https://platform.openai.com/docs/pricing) before a signed quote.

Internal page: `/docs/proposal-ai-cost/`
