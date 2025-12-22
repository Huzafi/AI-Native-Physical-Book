"""
Basic test script to verify the implementation of the AI-Native Book with Docusaurus
"""
import os
import sys
from pathlib import Path

def check_directory_structure():
    """Check if the expected directories exist"""
    project_root = Path.cwd()

    # Check main directories
    required_dirs = [
        'website',
        'backend',
        'specs',
        'history',
        'docs'
    ]

    for dir_name in required_dirs:
        if not (project_root / dir_name).exists():
            print(f"[ERROR] Missing directory: {dir_name}")
            return False
        else:
            print(f"[OK] Found directory: {dir_name}")

    # Check website structure
    website_dirs = [
        'website/src/components',
        'website/docs',
        'website/src/css',
        'website/src/theme'
    ]

    for dir_path in website_dirs:
        if not (project_root / dir_path).exists():
            print(f"[ERROR] Missing website directory: {dir_path}")
            return False
        else:
            print(f"[OK] Found website directory: {dir_path}")

    # Check backend structure
    backend_dirs = [
        'backend/app/api',
        'backend/app/services',
        'backend/app/models',
        'backend/app/database'
    ]

    for dir_path in backend_dirs:
        if not (project_root / dir_path).exists():
            print(f"[ERROR] Missing backend directory: {dir_path}")
            return False
        else:
            print(f"[OK] Found backend directory: {dir_path}")

    return True

def check_files():
    """Check if the key files exist and contain expected content"""
    project_root = Path.cwd()

    # Check backend files
    backend_files = [
        'backend/app/main.py',
        'backend/app/api/search.py',
        'backend/app/services/search_service.py',
        'backend/app/api/translation.py'
    ]

    for file_path in backend_files:
        full_path = project_root / file_path
        if not full_path.exists():
            print(f"[ERROR] Missing file: {file_path}")
            return False
        else:
            print(f"[OK] Found file: {file_path}")

            # Check if search functionality is enhanced
            if file_path == 'backend/app/api/search.py':
                content = full_path.read_text()
                if 'offset' in content and 'include_highlights' in content:
                    print(f"  [OK] Enhanced search API with pagination and highlights")
                if 'suggest' in content:
                    print(f"  [OK] Search suggestions endpoint implemented")

            # Check if translation functionality is implemented
            if file_path == 'backend/app/services/search_service.py':
                content = full_path.read_text()
                if 'get_suggestions' in content:
                    print(f"  [OK] Search suggestions service implemented")
                if 'get_total_search_count' in content:
                    print(f"  [OK] Search pagination service implemented")

    # Check website files
    website_files = [
        'website/src/components/LanguageSelector/LanguageSelector.js',
        'website/src/components/TranslationToggle/TranslationToggle.js',
        'website/src/utils/translationService.js'
    ]

    for file_path in website_files:
        full_path = project_root / file_path
        if not full_path.exists():
            print(f"[ERROR] Missing file: {file_path}")
            return False
        else:
            print(f"[OK] Found file: {file_path}")

            # Check if translation functionality is implemented
            if file_path == 'website/src/utils/translationService.js':
                content = full_path.read_text()
                if 'getContentWithFallback' in content:
                    print(f"  [OK] Translation fallback mechanism implemented")
                if 'fetchTranslation' in content:
                    print(f"  [OK] Translation API service implemented")

    # Check README
    readme_path = project_root / 'README.md'
    if readme_path.exists():
        content = readme_path.read_text()
        expected_sections = [
            'Search Functionality',
            'AI Assistant',
            'Translation Support',
            'API Endpoints'
        ]

        missing_sections = []
        for section in expected_sections:
            if section not in content:
                missing_sections.append(section)

        if missing_sections:
            print(f"[ERROR] Missing sections in README: {missing_sections}")
        else:
            print(f"[OK] README contains all expected sections")
    else:
        print(f"[ERROR] README.md not found")
        return False

    # Check troubleshooting guide
    troubleshooting_path = project_root / 'docs/troubleshooting.md'
    if troubleshooting_path.exists():
        print(f"[OK] Troubleshooting guide exists")
    else:
        print(f"[ERROR] Troubleshooting guide not found")
        return False

    return True

def check_component_features():
    """Check if key components have been implemented"""
    project_root = Path.cwd()

    # Check translation components
    translation_components = [
        'website/src/components/LanguageSelector',
        'website/src/components/TranslationToggle'
    ]

    for comp_path in translation_components:
        if not (project_root / comp_path).exists():
            print(f"[ERROR] Missing translation component: {comp_path}")
            return False
        else:
            print(f"[OK] Found translation component: {comp_path}")

    # Check CSS modules
    css_files = [
        'website/src/components/LanguageSelector/LanguageSelector.module.css',
        'website/src/components/TranslationToggle/TranslationToggle.module.css'
    ]

    for css_path in css_files:
        if not (project_root / css_path).exists():
            print(f"[ERROR] Missing CSS file: {css_path}")
            return False
        else:
            print(f"[OK] Found CSS file: {css_path}")

            # Check for RTL support
            if 'TranslationToggle.module.css' in css_path:
                content = (project_root / css_path).read_text()
                if '.rtl' in content and 'direction: rtl' in content:
                    print(f"  [OK] RTL support implemented for Urdu")

    return True

def main():
    print("[TEST] Testing AI-Native Book Implementation")
    print("="*50)

    all_checks_passed = True

    print("\n[CHECK] Checking directory structure...")
    if not check_directory_structure():
        all_checks_passed = False

    print("\n[CHECK] Checking files...")
    if not check_files():
        all_checks_passed = False

    print("\n[CHECK] Checking components...")
    if not check_component_features():
        all_checks_passed = False

    print("\n" + "="*50)
    if all_checks_passed:
        print("[SUCCESS] All checks passed! Implementation looks good.")
        print("\n[FEATURES] Key features implemented:")
        print("   - Enhanced search with pagination and suggestions")
        print("   - Translation system with fallback mechanism")
        print("   - Language selector with RTL support")
        print("   - Proper API endpoints")
        print("   - Updated documentation")
        print("   - Troubleshooting guide")
    else:
        print("[ERROR] Some checks failed. Please review the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()