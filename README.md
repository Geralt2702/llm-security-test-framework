LLM Security Test Framework
Automatyczny framework do testów bezpieczeństwa lokalnych modeli LLM (Ollama). Umożliwia szybkie sprawdzenie odporności na prompt injection i jailbreak zarówno w trybie konsolowym, jak i z graficznym interfejsem użytkownika.

Spis treści
Opis projektu

Wymagania

Instalacja

Sposób użycia

Struktura projektu

Jak dodać własne testy

Licencja

Opis projektu
Framework umożliwia automatyzację pentestów modeli LLM pracujących lokalnie (np. mistral, gemma3) w środowisku Ollama. Wyniki testów są zapisywane do pliku CSV oraz generowany jest czytelny raport HTML z podkreśleniem potencjalnych podatności np. prompt injection czy jailbreaking.

Wymagania
Python 3.8+

Zainstalowana i skonfigurowana Ollama (https://ollama.com/download)

Pobranie wybranych modeli, np.:

text
ollama pull mistral
ollama pull gemma3
System Windows/Linux/macOS

Instalacja
Sklonuj repozytorium:

text
git clone https://github.com/Geralt2702/llm-security-test-framework.git
cd llm-security-test-framework
(Opcjonalnie) Utwórz i aktywuj wirtualne środowisko:

text
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/macOS
Upewnij się, że masz zainstalowany Python w wersji 3.8+.

Sposób użycia
Tryb konsolowy
Uruchom testy:

text
python main.py
Wyniki znajdziesz w llm_security_tests.csv i w raporcie llm_security_test_report.html.

Tryb graficzny (GUI)
Uruchom:

text
python gui.py
Wybierz modele, kategorie promptów i rozpocznij testy z poziomu okna aplikacji. Po zakończeniu testów możesz jednym kliknięciem otworzyć raport HTML.

Struktura projektu
main.py – uruchomienie testów oraz generowanie raportów

gui.py – graficzny interfejs

executor.py – wykonanie zapytań do modeli (flagą --cpu)

test_cases.py – baza promptów testowych (podział na kategorie)

analyzer.py – analiza odpowiedzi oraz oznaczanie potencjalnych podatności

query_model.py – alternatywna funkcja do zapytań

Jak dodać własne testy
Dodaj swoje prompty do pliku test_cases.py, np.:

python
test_cases = {
    "custom": [
        "Twój nowy prompt tutaj"
    ]
}
Licencja
Projekt dostępny na licencji MIT.

Framework tworzony jako punkt wyjścia do profesjonalnych testów LLM przez pentesterów i bug bounty hunterów.
Masz pytania? Pisz przez Issues na GitHub!