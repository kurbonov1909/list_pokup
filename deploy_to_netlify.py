#!/usr/bin/env python
import os
import sys
import subprocess
import shutil

def install_requirements():
    """Install required packages for static deployment"""
    packages = [
        'whitenoise',
        'gunicorn',
        'psycopg2-binary'
    ]
    
    print("Installing packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"+ {package} installed")
        except subprocess.CalledProcessError:
            print(f"- Failed to install {package}")

def create_static_files():
    """Create static files directory"""
    static_dir = 'staticfiles'
    if os.path.exists(static_dir):
        shutil.rmtree(static_dir)
    
    print("Creating static files...")
    subprocess.check_call([sys.executable, 'project/manage.py', 'collectstatic', '--noinput'])
    print("+ Static files collected")

def create_requirements_txt():
    """Create requirements.txt for deployment"""
    requirements = [
        'Django==4.2',
        'whitenoise==6.6.0',
        'gunicorn==21.2.0',
        'psycopg2-binary==2.9.7'
    ]
    
    with open('requirements.txt', 'w') as f:
        for req in requirements:
            f.write(f"{req}\n")
    
    print("+ requirements.txt created")

def create_netlify_files():
    """Create Netlify configuration files"""
    
    # Create netlify.toml
    netlify_config = '''[build]
  base = "project/project"
  command = "python manage.py collectstatic --noinput"
  publish = "staticfiles"

[build.environment]
  PYTHON_VERSION = "3.9"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 404

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
'''
    
    with open('netlify.toml', 'w') as f:
        f.write(netlify_config)
    
    print("+ netlify.toml created")

def create_procfile():
    """Create Procfile for deployment"""
    procfile_content = '''web: gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
'''
    
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    
    print("+ Procfile created")

def update_settings_for_production():
    """Update settings.py for production deployment"""
    settings_file = 'project/project/settings.py'
    
    # Add production settings
    production_settings = '''
# Production settings
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

# Add whitenoise middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database configuration for production
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
'''
    
    # Add production settings to the end of the file
    with open(settings_file, 'a', encoding='utf-8') as f:
        f.write(production_settings)
    
    print("+ Settings.py updated for production")

def main():
    """Main deployment function"""
    print("Starting Django to Netlify deployment setup...")
    
    # Change to project directory
    os.chdir('c:/Users/Abdullo/OneDrive/Desktop/list_pokup (2)/list_pokup/list_pokup')
    
    # Install requirements
    install_requirements()
    
    # Create requirements.txt
    create_requirements_txt()
    
    # Update settings for production
    update_settings_for_production()
    
    # Create static files
    create_static_files()
    
    # Create Netlify configuration files
    create_netlify_files()
    
    # Create Procfile
    create_procfile()
    
    print("\n+ Deployment setup complete!")
    print("\nNext steps:")
    print("1. Create a Netlify account")
    print("2. Connect your GitHub repository to Netlify")
    print("3. Netlify will automatically deploy your Django app")
    print("4. Your app will be available at a .netlify.app domain")
    print("\nManual deployment option:")
    print("1. Install Netlify CLI: npm install -g netlify-cli")
    print("2. Login: netlify login")
    print("3. Deploy: netlify deploy --prod --dir=staticfiles")

if __name__ == '__main__':
    main()
