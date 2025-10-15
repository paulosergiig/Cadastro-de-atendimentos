import os

# Estrutura de diretórios
dirs = [
    "clinicmanager/clinicmanager",
    "accounts/migrations",
    "accounts/templates/accounts",
    "patients/migrations",
    "patients/templates/patients",
    "auditlog/migrations",
    "core/templates/core",
    "fixtures",
    "templates/registration",
]

# Estrutura de arquivos
files = [
    "clinicmanager/clinicmanager/__init__.py",
    "clinicmanager/clinicmanager/asgi.py",
    "clinicmanager/clinicmanager/settings.py",
    "clinicmanager/clinicmanager/urls.py",
    "clinicmanager/clinicmanager/wsgi.py",
    "accounts/__init__.py",
    "accounts/admin.py",
    "accounts/apps.py",
    "accounts/forms.py",
    "accounts/models.py",
    "accounts/signals.py",
    "accounts/urls.py",
    "accounts/views.py",
    "accounts/migrations/__init__.py",
    "accounts/templates/accounts/password_change_form.html",
    "accounts/templates/accounts/password_change_done.html",
    "accounts/templates/accounts/therapist_confirm_delete.html",
    "accounts/templates/accounts/therapist_form.html",
    "accounts/templates/accounts/therapist_list.html",
    "patients/__init__.py",
    "patients/admin.py",
    "patients/apps.py",
    "patients/forms.py",
    "patients/models.py",
    "patients/urls.py",
    "patients/views.py",
    "patients/migrations/__init__.py",
    "patients/templates/patients/patient_detail.html",
    "patients/templates/patients/patient_form.html",
    "patients/templates/patients/patient_list.html",
    "patients/templates/patients/evolution_form.html",
    "patients/templates/patients/export_form.html",
    "auditlog/__init__.py",
    "auditlog/admin.py",
    "auditlog/apps.py",
    "auditlog/models.py",
    "auditlog/signals.py",
    "auditlog/migrations/__init__.py",
    "core/__init__.py",
    "core/urls.py",
    "core/views.py",
    "core/templates/core/home.html",
    "fixtures/initial_data.json",
    "templates/base.html",
    "templates/registration/login.html",
    ".env.example",
    "Dockerfile",
    "docker-compose.yml",
    "install_local.bat",
    "manage.py",
    "README.md",
    "requirements.txt",
    "run_dev.bat",
]

# Criar diretórios
for d in dirs:
    os.makedirs(d, exist_ok=True)

# Criar arquivos
for f in files:
    if not os.path.exists(f):
        open(f, "w").close()

print("✅ Estrutura criada com sucesso!")
