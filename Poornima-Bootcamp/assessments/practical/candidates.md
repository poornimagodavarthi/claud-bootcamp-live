# Candidates Evaluation

## Candidate A: Modern FastAPI Patterns ⭐ WINNER

**Score: 9/9**

**Strengths:**
- Uses modern `lifespan` context manager (FastAPI 0.93+) — future-proof
- Pydantic response models for type safety and automatic validation
- Clean context manager pattern with `try/finally` for database connections
- Unused import (`asynccontextmanager`) is minor and easily fixed

**Weaknesses:**
- `.dict()` method deprecated in Pydantic v2 (easy migration to `.model_dump()`)
- No explicit error handling in `init_db()`

**Implementation:**
```
- 99 lines, single file
- 5 endpoints (POST, GET all/filtered/by-ID, DELETE)
- Pydantic models for request/response validation
- Proper 404 error handling
```

**Why chosen:** Demonstrates best practices in modern FastAPI development. Pydantic response models catch type errors early; lifespan pattern is the recommended approach going forward. Code is production-ready with minimal issues.

---

## Candidate B: Pragmatic Approach

**Score: 8.5/9**

**Strengths:**
- Explicit query parameter handling with `Query(default=None)`
- Helper function `row_to_dict()` is DRY and clean
- Defensive pre-check before DELETE (validates existence before delete)
- Clean imports — only what's needed

**Weaknesses:**
- Uses deprecated `@app.on_event("startup")` (removed in FastAPI 1.0)
- Untyped dicts instead of Pydantic response models (less validation)
- No explicit error handling in database initialization

**Implementation:**
```
- 103 lines, single file  
- 5 endpoints (same as Candidate A)
- Manual dict conversion (works but loses type safety)
- Proper 404 error handling
```

**Why not chosen:** Pragmatic and readable, but uses deprecated patterns. Loss of type safety with untyped dicts means errors surface later (at serialization, not validation). Better for a quick prototype; not ideal for production.

---

## Comparison Summary

| Criterion | Candidate A | Candidate B |
|-----------|-------------|------------|
| **Correctness** | 3/3 ✅ | 3/3 ✅ |
| **Simplicity** | 3/3 ✅ | 3/3 ✅ |
| **Fit (Modern)** | 3/3 ✅ | 2.5/3 ⚠️ |
| **Total** | **9/9** | **8.5/9** |
| Future-proof | Yes (lifespan) | No (deprecated startup) |
| Type Safety | High (Pydantic models) | Medium (dicts) |
| Error Handling | Basic | Basic |

---

## Decision

**Candidate A selected as winner** for:
1. **Future compatibility** — uses modern lifespan, not deprecated `@app.on_event()`
2. **Type safety** — Pydantic response models catch errors early
3. **Production-ready** — 0.5 point difference on "Fit" reflects architectural choices that matter

Both implementations are functionally correct and well-structured. Candidate B is perfectly valid for a quick build; Candidate A is preferred for maintainability and future-proofing.
