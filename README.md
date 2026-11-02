# FastAPI API Source

A project for learning FastAPI and for provide dummy API sources.

## Rules

> **Note**: Comments marked with `# --- ... ---` represent custom configurations defined for this project's setup.

## Tutorial: Alembic Setup

### 1. Installation

```bash
# Using uv
uv add sqlalchemy alembic psycopg2-binary psycopg

# Or using pip
pip install sqlalchemy alembic psycopg2-binary
```

### 2. Initialize Alembic

```bash
alembic init alembic
```

This generates:
* `alembic.ini`: Configuration file for Alembic settings and directory paths.
* `alembic/`: Directory holding `env.py` (runtime environment script) and `versions/` (migration script files).

### 3. Connect Alembic to FastAPI Models & Database (`alembic/env.py`)

Right after `alembic init alembic`, `alembic/env.py` is a disconnected template. You only need to add **5 custom lines** (marked with `# --- ... ---`):

```python
# --- 1. Get DATABASE_URL from .env settings ---
from app.config.core import settings

# --- 2. Get SQLAlchemy Declarative Base ---
from app.db.base import Base

# --- 3. Register all models so Base.metadata knows about them ---
import app.models

# (Alembic default code: config = context.config)

# --- 4. Override alembic.ini dummy URL with your .env setting ---
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# --- 5. Connect models metadata for autogenerate (replace target_metadata = None) ---
target_metadata = Base.metadata
```

> **Why are these 5 lines needed?**
> * **Line 1 & 4 (`settings.DATABASE_URL`):** Reads credentials safely from `.env` instead of hardcoding passwords in `alembic.ini`.
> * **Line 2, 3 & 5 (`Base`, `app.models`, `target_metadata`):** Triggers Python to load your model files (`user.py`, `post.py`) into `Base.metadata` so Alembic can detect your tables automatically.



### Alembic Cheat Sheet

| Command | What it does |
| :--- | :--- |
| `alembic revision --autogenerate -m "message"` | Detects changes in SQLAlchemy models and automatically creates a new migration file |
| `alembic revision -m "message"` | Creates an **empty** migration file for manual operations (column renames, data migrations, raw SQL) |
| `alembic upgrade head` | Applies **all** pending migrations up to the latest revision |
| `alembic upgrade +1` | Applies **only the next 1** migration forward (step-by-step testing) |
| `alembic downgrade -1` | Rolls back **only the last 1** migration backward |
| `alembic downgrade base` | Rolls back **all** migrations (reverts to completely empty schema) |
| `alembic current` | Shows the current migration revision hash of the database |
| `alembic history --verbose` | Lists all migrations in chronological order |

---

### Key Concepts & Important Gotchas

#### 1. Why use `upgrade +1` instead of `upgrade head`?
* **`upgrade head`**: Applies everything in one go. Ideal for production deploys or fresh development databases.
* **`upgrade +1`**: Applies migrations **one step at a time**. Ideal when testing multiple new migrations locally to verify each migration script individually.

#### 2. When to use `--autogenerate` vs Manual Revision (`alembic revision -m`)

| Capability | `--autogenerate` | Manual Revision |
| :--- | :---: | :---: |
| Adding or dropping tables | ✅ Auto-detects | ⚠️ Must write manually |
| Adding or dropping columns | ✅ Auto-detects | ⚠️ Must write manually |
| **Changing `nullable` (`NULL` $\leftrightarrow$ `NOT NULL`)** | ✅ **Auto-detects** | ✅ Can also write manually |
| **Renaming columns** | ❌ **CANNOT detect** (causes data loss!) | ✅ **Required** |
| **Renaming tables** | ❌ **CANNOT detect** (causes data loss!) | ✅ **Required** |
| **Data migrations (SQL UPDATE / Backfills)** | ❌ **CANNOT detect** | ✅ **Required** |

> ⚠️ **Danger of `--autogenerate` on Column Renames:**  
> If you rename a column in `models.py` (e.g., `name` to `full_name`) and run `--autogenerate`, Alembic thinks you deleted the old column and created an unrelated new one:
> 1. `op.drop_column('users', 'name')` ❌ **(Destroys all existing user data!)**
> 2. `op.add_column('users', sa.Column('full_name', ...))`
>
> To rename a column safely without losing data, use an empty manual migration.

#### 3. How to safely rename a column (Step-by-step):
1. **Generate an empty migration file:**
   ```bash
   alembic revision -m "rename name to full_name in users"
   ```
2. **Open the generated file in `alembic/versions/` and use `op.alter_column()`:**
   ```python
   def upgrade() -> None:
       # Safely rename the column without dropping data
       op.alter_column('users', 'name', new_column_name='full_name')

   def downgrade() -> None:
       # Revert column back to original name if rolled back
       op.alter_column('users', 'full_name', new_column_name='name')
   ```
3. **Apply the migration:**
   ```bash
   alembic upgrade +1
   ```

#### 4. SQLAlchemy 2.0 Nullable Rules (`Mapped[T]` vs `Mapped[T | None]`)

In modern SQLAlchemy 2.0, column nullability is **automatically inferred** from Python types:

* **`user_note: Mapped[str] = mapped_column(...)`**  
  👉 Automatically **`nullable=False`** (`NOT NULL`).
* **`user_note: Mapped[str | None] = mapped_column(...)`**  
  👉 Automatically **`nullable=True`** (`NULL`).

> ⚠️ **Warning on Type Conflicts:**  
> Avoid writing `Mapped[str] = mapped_column(..., nullable=True)`.  
> While the database allows `NULL`, your IDE/Python believes it can never be `None`. Calling methods like `user.user_note.lower()` will crash with `AttributeError: 'NoneType' object has no attribute 'lower'` at runtime!

#### 5. How to change a column from Nullable to NOT NULL

1. **Update your model:**
   ```python
   # app/models/user.py
   user_note: Mapped[str] = mapped_column(String(255))
   ```
2. **Autogenerate or manually create the migration:**
   ```bash
   alembic revision --autogenerate -m "make user_note not nullable"
   ```
3. **Apply it:**
   ```bash
   alembic upgrade head
   ```
   > 💡 **Notice:** If existing rows in your database already contain `NULL` in that column, PostgreSQL will block the change. You must either clear/fill those values first or supply a `server_default=""`.
