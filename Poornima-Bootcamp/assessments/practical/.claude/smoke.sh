#!/bin/bash
# Smoke test for Bookmarks API
# Verifies all 5 endpoints return expected status codes

set -e

BASE_URL="http://localhost:8000"
PASSED=0
FAILED=0

echo "🔥 Running Bookmarks API smoke tests..."
echo "Base URL: $BASE_URL"
echo ""

# Test 1: POST /bookmarks → 201
echo "1. POST /bookmarks (create) → 201"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/bookmarks" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://python.org", "title": "Python", "tag": "coding"}')
if [ "$STATUS" = "201" ]; then
  echo "   ✅ PASS (got 201)"
  ((PASSED++))
else
  echo "   ❌ FAIL (got $STATUS, expected 201)"
  ((FAILED++))
fi

# Test 2: GET /bookmarks → 200
echo "2. GET /bookmarks (list all) → 200"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/bookmarks")
if [ "$STATUS" = "200" ]; then
  echo "   ✅ PASS (got 200)"
  ((PASSED++))
else
  echo "   ❌ FAIL (got $STATUS, expected 200)"
  ((FAILED++))
fi

# Test 3: GET /bookmarks?tag=coding → 200
echo "3. GET /bookmarks?tag=coding (filter) → 200"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/bookmarks?tag=coding")
if [ "$STATUS" = "200" ]; then
  echo "   ✅ PASS (got 200)"
  ((PASSED++))
else
  echo "   ❌ FAIL (got $STATUS, expected 200)"
  ((FAILED++))
fi

# Test 4: GET /bookmarks/1 → 200
echo "4. GET /bookmarks/1 (get one) → 200"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/bookmarks/1")
if [ "$STATUS" = "200" ]; then
  echo "   ✅ PASS (got 200)"
  ((PASSED++))
else
  echo "   ❌ FAIL (got $STATUS, expected 200)"
  ((FAILED++))
fi

# Test 5: GET /bookmarks/999 → 404
echo "5. GET /bookmarks/999 (missing) → 404"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/bookmarks/999")
if [ "$STATUS" = "404" ]; then
  echo "   ✅ PASS (got 404)"
  ((PASSED++))
else
  echo "   ❌ FAIL (got $STATUS, expected 404)"
  ((FAILED++))
fi

# Test 6: DELETE /bookmarks/1 → 204
echo "6. DELETE /bookmarks/1 (delete) → 204"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE_URL/bookmarks/1")
if [ "$STATUS" = "204" ]; then
  echo "   ✅ PASS (got 204)"
  ((PASSED++))
else
  echo "   ❌ FAIL (got $STATUS, expected 204)"
  ((FAILED++))
fi

# Test 7: DELETE /bookmarks/999 → 404
echo "7. DELETE /bookmarks/999 (missing) → 404"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE_URL/bookmarks/999")
if [ "$STATUS" = "404" ]; then
  echo "   ✅ PASS (got 404)"
  ((PASSED++))
else
  echo "   ❌ FAIL (got $STATUS, expected 404)"
  ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: $PASSED passed, $FAILED failed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAILED -eq 0 ]; then
  echo "✅ All smoke tests PASSED"
  exit 0
else
  echo "❌ Some tests FAILED"
  exit 1
fi
