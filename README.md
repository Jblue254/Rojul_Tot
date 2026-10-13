# Rojul Tot Backend

Django REST Framework API for the Rojul Tot construction machinery, drawings, projects, rentals, and related services platform.

## Live deployment

- **Live frontend:** https://rojul-tot-frontend.vercel.app/
- **Backend API:** https://web-production-c75a0.up.railway.app/
- **Public machinery endpoint:** https://web-production-c75a0.up.railway.app/api/machinery/public/
- **Public drawings endpoint:** https://web-production-c75a0.up.railway.app/api/drawings/public/
- **Backend hosting:** Railway
- **Database and object storage:** Supabase

## Technology

- Python, Django, Django REST Framework
- Supabase PostgreSQL and Supabase Storage
- Gunicorn for production serving (confirm the Railway start command in the repository)

## API areas

| Area | Base path |
|---|---|
| Accounts/authentication | `/api/auth/` |
| Machinery | `/api/machinery/` |
| Rentals | `/api/rentals/` |
| Drawings | `/api/drawings/` |
| Orders | `/api/orders/` |
| Projects | `/api/projects/` |
| Notifications | `/api/notifications/` |
| Reviews | `/api/reviews/` |
| Analytics | `/api/analytics/` |
| Contacts | `/api/contacts/` |
| Payments | `/api/payments/` |

Check each app's `urls.py` for exact routes. Some endpoints require authentication.

## Local setup

Run commands from the folder containing `manage.py`.

### 1. Create a virtual environment

Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Git Bash:
```bash
python -m venv venv
source venv/Scripts/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, create it with `pip freeze > requirements.txt` and review it before committing.

### 3. Configure environment variables

Create `.env` beside `manage.py`. Example template:

```dotenv
SECRET_KEY=replace-with-a-strong-secret
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_SERVICE_ROLE_KEY=replace-with-your-service-role-key
```

Use the base Supabase URL only; do not append `/rest/v1/` or `/storage/v1/`. Add any other variables required by `config/settings.py`.

**Security:** Never commit `.env` or expose `SUPABASE_SERVICE_ROLE_KEY` to the frontend. Configure production secrets in Railway.

### 4. Check and migrate

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate
```

Confirm the configured database before running migrations. Do not reset or drop production data to troubleshoot deployment.

### 5. Run locally

```bash
python manage.py runserver
```

Default local URL: `http://127.0.0.1:8000/`.

## Supabase Storage

| Purpose | Bucket | Access |
|---|---|---|
| Machinery images | `machinery-images` | Public |
| Project images | `project-images` | Public |
| Drawing previews | `drawing-previews` | Public |
| Drawing documents | `drawing-files` | Private |
| Profile images | `profile-images` | Public |

Paths used during setup include `machinery/<filename>`, `projects/<filename>`, `drawings/previews/<filename>`, `drawings/files/<filename>`, and `profiles/<filename>`. Filenames and folders must match exactly, including spaces, underscores, and capitalization.

Public object URL format:
```text
https://YOUR_PROJECT_REF.supabase.co/storage/v1/object/public/BUCKET_NAME/OBJECT_PATH
```

The `drawing-files` bucket is private. Public drawing responses intentionally return `drawing_file: null`; purchased documents should use the authenticated backend download flow.

## Confirmed public endpoints

- `GET /api/machinery/public/` — public machinery records and image URLs.
- `GET /api/drawings/public/` — public drawing records and preview URLs.

A `401 Unauthorized` response from a protected endpoint without a bearer token is expected.

## Railway deployment

1. Push backend changes to the repository connected to Railway.
2. Configure required environment variables in Railway.
3. Set `SUPABASE_URL` to the base project URL.
4. Keep the service-role key only in backend secrets.
5. Deploy and inspect application logs.
6. Verify both public endpoints return `200 OK`.

## Troubleshooting

- **Image missing:** Open the exact URL returned by the API. Confirm bucket, folder, filename, and public access.
- **401 response:** The endpoint may require authentication.
- **500 response:** Inspect Railway logs for a traceback and verify environment variables.
- **Malformed Supabase URL:** Use the base project URL only.

## Before committing

- Keep `.env`, secrets, virtual environments, and `__pycache__` out of Git.
- Run `python manage.py check` and relevant tests.
- Do not reset production database data during routine deployment.

---

## Author and maintainer

- **Name:** Japheth Kiprono
- **Email:** japhethkiprono2020@gmail.com
- **GitHub:** https://github.com/Jblue254/
- **Live frontend:** https://rojul-tot-frontend.vercel.app/
- **Live backend:** https://web-production-c75a0.up.railway.app/

## MIT License

Copyright (c) 2026 Japheth Kiprono

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
