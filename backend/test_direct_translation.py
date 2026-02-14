#!/usr/bin/env python
"""Direct test of translation"""

from services.translation_service import TranslationService

french_text = "ORDONNANCE MEDICALE Patient: Jean Dupont Medicament: LISINOPRIL 10mg"

print("Testing translation directly...")
print(f"Input text: {french_text}")
print(f"Language: French (fr)")

result = TranslationService.translate_to_english(french_text, "fr")

print(f"\nResult:")
print(f"  Success: {result['success']}")
print(f"  Error: {result.get('error')}")
print(f"  Translated: {result.get('translated_text')}")
