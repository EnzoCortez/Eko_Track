# Eko Track Implementation Plan

## Goal Description
Create "Eko Track", a Flask-based environmental habit tracking and issue reporting application. It features a Django-like admin interface for managing data, a user reporting system with criticality levels, and an intervention suggestion system based on a criticality matrix and municipal budget.

## User Review Required
> [!IMPORTANT]
> **Backend Validation**: The "Budget" (or cost) field will be treated as the sensitive data requiring strict backend validation in the Admin interface.
> **Foreign Keys**: Flask-Admin automatically handles Foreign Keys as dropdowns. We will ensure this behavior is explicit for the `ReportType` selection.

## Proposed Changes

### Project Structure
- `app/`: Main application package
    - `__init__.py`: App factory
    - `models.py`: Database models
    - `admin.py`: Flask-Admin configuration with custom validation
    - `routes.py`: User facing routes
    - `utils.py`: Prioritization logic
    - `templates/`: HTML templates
    - `static/`: CSS/JS
- `run.py`: Entry point
- `config.py`: Configuration

### Database Models (`app/models.py`)
#### [NEW] `models.py`
- `User`: Standard auth model.
- `ReportCategory`: Represents the type of report (e.g., "Waste", "Air Quality") with a base priority score.
- `Report`: The main entity.
    - Fields: `title`, `description`, `criticality` (High/Med/Low), `estimated_cost`, `status`.
    - Relationships: `user_id`, `category_id`.
- `MunicipalitySettings`: Singleton-like table to store the total `current_budget`.

### Admin Interface (`app/admin.py`)
#### [NEW] `admin.py`
- Use `flask_admin.contrib.sqla.ModelView`.
- **Validation**: Override `on_model_change` for the `Report` or `MunicipalitySettings` model to validate `estimated_cost` or `budget`. It must be positive and within reasonable limits.
- **Dropdowns**: Ensure `category_id` in `Report` view renders as a dropdown (standard behavior, but will verify).

### User Features (`app/routes.py`)
#### [NEW] `routes.py`
- `/`: Landing page / Dashboard showing high priority issues.
- `/report`: Form to submit a new report.
- `/login`, `/register`: Auth.

## Verification Plan

### Automated Tests
- None explicitly requested, but will run manual verification steps.

### Manual Verification
1. **Admin Validation**: Try to save a Report with a negative cost or a cost exceeding the budget via the Admin panel. Expect a backend error message.
2. **Dropdowns**: Verify that creating a Report in Admin shows a dropdown for Category.
3. **Prioritization**: Create reports with different criticality/categories and verify the "Suggested Interventions" list orders them correctly.
