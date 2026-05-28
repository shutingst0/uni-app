# CLAUDE.md

## Naming conventions
- No abbreviated variable names. Write the full name every time.
  - `student_data_repository` not `repository`, `repo`, or `student_repo`
  - `student_dict` not `d`
  - `student` not `s`
  - `file` not `f` in `with open(...) as file:`
- Use snake_case for all variables, functions, and file names.

## Code style
- Do not use abbreviations anywhere — variables, parameters, or method names.
- Prefer explicit, readable names over short ones.
- No shorthand syntax. Use explicit for loops instead of comprehensions or set/dict expressions.
- Store method call results in a named variable before using in an if statement.
  - `is_valid = self.validate(email, password)` then `if not is_valid:` — not `if not self.validate(email, password):`
  - `existing_student = self.repository.find_by_email(email)` then `if existing_student:` — not `if self.repository.find_by_email(email):`
  - `for student in students: existing_ids.append(student.id)` not `{student.id for student in students}`
  - `for student in students: result.append(student.to_dict())` not `[student.to_dict() for student in students]`

## Architecture
- `database.py` — legacy raw JSON layer (being drained, do not add new usages)
- `student_data_repository.py` — new repository layer, returns `Student` instances
- `file.py` — handles all file I/O, used by `StudentDataRepository`
- `account_service.py` — uses dependency injection, takes a `StudentDataRepository` instance
- `uni_cli_app.py` — app entry point and all menu/handler functions
- `utils.py` — helper functions
- `constants.py` — app-wide constants
