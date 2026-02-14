#!/usr/bin/env python
"""Quick test of translation service"""

from services.translation_service import TranslationService
from services.language_detection_service import LanguageDetectionService

# Test French text
french_text = """ORDONNANCE MEDICALE
Patient: Jean Dupont

Medicament: LISINOPRIL 10mg
Lot LN-2024-567850

Date d'Expiration: 06/15/2026
Fabricant: Medicaments Cardiaques
Instructions:

Prendre 1 comprime par our

Quantite: 80 comprimes

Renoellement:2

Pharmacie: Pharmacie Centrale"""

print("=" * 80)
print("TRANSLATION SERVICE TEST")
print("=" * 80)

# Test language detection
print("\n1. Testing Language Detection...")
lang_result = LanguageDetectionService.detect_language(french_text)
print(f"   Result: {lang_result}")

# Test translation
print("\n2. Testing Translation...")
trans_result = TranslationService.translate_to_english(french_text, "fr")
print(f"   Success: {trans_result['success']}")
print(f"   Error: {trans_result.get('error')}")
print(f"   Translated Text (first 200 chars):\n   {trans_result['translated_text'][:200]}")

print("\n" + "=" * 80)
