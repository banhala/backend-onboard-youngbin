import os
import sys
from pathlib import Path

import django

# 프로젝트 루트를 Python 경로에 추가
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Django 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()
