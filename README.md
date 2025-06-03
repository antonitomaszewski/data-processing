# data-processing
alterdata.io

Na co będziemy zwracać uwagę:

1. dobre praktyki (np. SOLID w miarę możliwości).
2. Testy: Pokrycie kodu testami (jednostkowymi, integracyjnymi) jest bardzo ważne. Użyj pytest.
3. Obsługa błędów i przypadków brzegowych: Jak Twoje rozwiązanie radzi sobie z nieoczekiwanymi danymi lub sytuacjami.
4. Dokumentacja: Krótki opis rozwiązania w pliku README.md (jak uruchomić, jakie decyzje projektowe podjąłeś, ewentualne kompromisy).

Wymagania techniczne:


1. Testy: pytest.

ZADANIE : System Przetwarzania i Agregacji Danych o Transakcjach
- Kontekst: Firma Z analizuje duże ilości danych transakcyjnych pochodzących z różnych systemów. Potrzebujemy narzędzia backendowego, które pozwoli na importowanie danych o transakcjach, ich walidację, proste przetwarzanie oraz udostępnianie zagregowanych wyników poprzez API.

Wymagania:

1. Agregacja Danych:
- Zaimplementuj endpoint API (GET /reports/product-summary/{product_id}), który zwróci podsumowanie dla danego produktu:
--> Całkowita sprzedana ilość produktu.
--> Całkowity przychód wygenerowany przez produkt (w PLN, jak wyżej).
--> Liczba unikalnych klientów, którzy kupili ten produkt.

1. Co będzie dodatkowym atutem (Bonus):
- Asynchroniczne przetwarzanie importu pliku CSV (np. z użyciem Celery lub mechanizmów async FastAPI).
- Obsługa błędów i logowanie na produkcyjnym poziomie.
- Prosty mechanizm uwierzytelniania API (np. token w nagłówku).
- Możliwość generowania raportów dla zakresu dat.