## HTMX + API-only Django — Best practices for accessRating.info

This document captures recommended patterns, contracts, and small code snippets for using an API-only Django/DRF backend together with a static HTML + HTMX frontend.

Keep this short and actionable. Use it as a checklist and reference while implementing business list/detail pages and HTMX fragment swaps.

---

## Quick checklist

- [ ] Keep Django/DRF as the canonical JSON API for resources (e.g. `/api/v1/businesses/<id>/`).
- [ ] Provide a minimal HTML fragment endpoint for HTMX swaps (e.g. `/api/v1/businesses/<id>/fragment/`).
- [ ] Use plural resource paths consistently across JSON and fragment endpoints.
- [ ] Ensure HTMX-friendly responses for fragment endpoints: fragments must be partial HTML only (no full layout) and use correct status codes on errors.
- [ ] Frontend: anchor tags should have real `href` values for progressive enhancement. Use `hx-get` with `hx-push-url` to swap fragments and update URL.
- [ ] Implement a small “on-load router” in the static frontend to fetch fragment when `location.pathname` matches a resource path.
- [ ] Add global HTMX event listeners for `htmx:responseError`, `htmx:sendError`, and `htmx:targetError` to show friendly UI messages and for logging.
- [ ] Ensure CSRF tokens are attached to HTMX requests (session auth) or use token auth for API-only flows.
- [ ] Vote/helpful endpoints should be idempotent, authenticated, and return the updated count + user_has_voted. Rate-limit these endpoints.
- [ ] Add unit tests for fragment endpoints and vote endpoints (happy path + auth/permission failures + idempotency).
- [ ] Add CORS config or host frontend on same origin for prod. Add dev CORS rules for local front-end testing.

---

## Contract (tiny API contract)

- JSON resource
  - GET /api/v1/businesses/<id>/ -> 200 JSON
  - 401 if auth required, 404 if not found

- Fragment (HTMX)
  - GET /api/v1/businesses/<id>/fragment/ -> 200 with partial HTML (only the inner markup to insert into `#main-content`)
  - If 404/401 -> return appropriate status code; body can be an error snippet (small HTML) so HTMX can swap or your global handler can render a message.

- Voting
  - POST /api/v1/businesses/<id>/reviews/<review_id>/vote/ -> 200 JSON with { helpful_count, user_has_voted }
  - Implement as toggle or explicit add/remove. If toggle, ensure idempotency: repeated calls should not cause incorrect increments.

Error modes to handle on the frontend: network failure, 401 (show login), 404 (show not-found), 500 (retry / friendly error).

---

## Server-side patterns (Django + DRF)

- Use DRF ViewSets for the JSON API.
- For fragment HTML, use one of these simple options:
  - a dedicated lightweight Django view that loads the same serializer/context and returns a TemplateResponse for the fragment; or
  - content-negotiation in the ViewSet (if Accept header contains `text/html`) and return TemplateResponse. (This is more subtle; prefer the dedicated view.)

- Fragment views must return only the partial template (no base layout). For example `business_detail_fragment.html` should contain only the inner content to be swapped into `#main-content`.

- Voting endpoints: keep them isolated on the API (sub-route on review or review action on viewset). Require authentication and CSRF for session auth.

- Always return JSON for API requests, and HTML for fragment endpoints. Explicitly set status codes for error cases.

Example URL layout (recommended):

- /api/v1/businesses/            (list, JSON)
- /api/v1/businesses/<id>/       (retrieve, JSON)
- /api/v1/businesses/<id>/fragment/  (HTMX HTML fragment)
- /api/v1/businesses/<id>/reviews/<review_id>/vote/  (POST toggle)

---

## Frontend snippets (HTMX + static host)

1) Progressive anchors

 - Use a real `href="/businesses/123"` so keyboard users and crawlers have a valid link. Add HTMX attributes to the same link for dynamic behavior:

```html
<a href="/businesses/123"
   hx-get="/api/v1/businesses/123/fragment/"
   hx-target="#main-content"
   hx-push-url="/businesses/123">
  View details
</a>
```

2) Initial-load router (very small). Place in your `businesses.html` static frontend.

```html
<script>
document.addEventListener('DOMContentLoaded', function () {
  const path = location.pathname;
  const match = path.match(/^\/businesses\/(\d+)\/?$/);
  if (match) {
    const id = match[1];
    const fragmentUrl = `/api/v1/businesses/${id}/fragment/`;
    fetch(fragmentUrl, { credentials: 'include' })
      .then(r => {
        if (!r.ok) throw r;
        return r.text();
      })
      .then(html => {
        document.getElementById('main-content').innerHTML = html;
        if (window.htmx) htmx.process(document.getElementById('main-content'));
      })
      .catch(err => {
        console.error('Failed to load business fragment', err);
        // render a small friendly message
        document.getElementById('main-content').innerHTML = '<div class="error">Unable to load page.</div>';
      });
  }
});
</script>
```

3) HTMX global handlers (CSRF + error UI)

 - CSRF header (Django session auth): read cookie and attach header for HTMX/fetch requests.

```html
<script>
function getCookie(name) {
  const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return v ? v.pop() : '';
}
if (window.htmx) {
  htmx.on('htmx:configRequest', (evt) => {
    const token = getCookie('csrftoken');
    if (token) evt.detail.headers['X-CSRFToken'] = token;
  });
}

// global error handling
document.body.addEventListener('htmx:responseError', function (evt) {
  // evt.detail.xhr.status, evt.detail.xhr.responseText
  const status = evt.detail.xhr && evt.detail.xhr.status;
  console.warn('HTMX response error', status, evt.detail);
  // Simple UI feedback — adapt to your UI system
  const banner = document.getElementById('global-banner');
  if (banner) banner.textContent = 'Something went wrong. Please try again.';
});

document.body.addEventListener('htmx:targetError', function (evt) {
  console.error('HTMX target error', evt);
  const banner = document.getElementById('global-banner');
  if (banner) banner.textContent = 'Display error: unable to insert content.';
});
</script>
```

4) Helpful-vote pattern (frontend)

 - POST to the vote endpoint and replace the vote control HTML on success. Use `hx-post` and `hx-swap="outerHTML"` on the vote button/form so the server returns the updated button and count.

```html
<form hx-post="/api/v1/businesses/123/reviews/456/vote/" hx-swap="outerHTML" hx-target="this">
  <button type="submit">Helpful (<span class="count">3</span>)</button>
</form>
```

Server should return the updated snippet (button + count) so the swap is simple and idempotent.

---

## Testing guidance

- Unit tests (pytest-django): add tests for the fragment view (GET returns 200 and contains an element with known id/class), and for vote endpoints (authenticated user toggles vote; repeated toggles behave correctly). 
- Integration: simulate Accept header or request the fragment URL directly.

Example tests to add under `backend/apps/businesses/tests/`:
- test_fragment_view.py (happy path + 404)
- test_vote_endpoint.py (happy path + unauthenticated)

---

## Deployment / Ops notes

- CORS: if serving static frontend from a distinct origin, add `django-cors-headers` and allow the frontend origin in production/staging. For dev, allow `http://localhost:5500` (or whatever Live Server uses).
- Caching: fragment endpoints may be cacheable for anonymous users. Use conservative cache headers and cache keys that include relevant user state (e.g. whether user has voted) when serving personalized fragments.
- Rate-limiting: use a simple throttle for vote endpoints (DRF throttles or nginx-level rate limits) to avoid abuse.

---

## SEO and accessibility

- If SEO is important, either:
  - Provide server-rendered full pages for critical routes, or
  - Use prerendering for crawlers, or
  - Provide JSON-LD and sitemaps so search engines can index important data.

- Keep anchors with `href` and use ARIA roles where needed. Ensure fragment swaps set focus appropriately after swap for screen readers.

---

## Next steps / Implementation suggestions

1. Add the HTMX global handlers and initial-load router to `accessRating.info_frontend/businesses.html` (low risk).
2. Verify fragment endpoint path in backend; if needed, add `/api/v1/businesses/<id>/fragment/` and small tests.
3. Add a test for vote endpoint and a small HTMX-friendly snippet template for the vote button.
4. Add dev CORS config to `accessibility_api/dev_settings.py` (or equivalent) so the static frontend can call the API during local development.

If you want, I can implement steps 1 and 2 now and run the tests. Pick which step(s) to do next.

---

Document created: keep this iterative — add examples from the actual codebase as we implement.
