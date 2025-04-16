# 📝 Aplikacja do Zarządzania Zadaniami (To-Do List)

## **📜 Opis projektu**
Zaprojektuj i zaimplementuj aplikację To-Do List do zarządzania codziennymi zadaniami z graficznym interfejsem użytkownika opartym na Tkinter, zgodnie z architekturą MVC (Model-View-Controller). Dane mają być przechowywane w pliku .json, a aplikacja ma wykorzystywać zasady programowania obiektowego, dziedziczenie oraz zaawansowane zagadnienia z Pythona (sortowanie, filtrowanie, datetime, powiadomienia, testy jednostkowe).

---

## **🎮 Funkcjonalności**
** ➕ Dodawanie zadań **:
- Użytkownik może dodać nowe zadanie zawierające:
- Tytuł
- Opis (opcjonalny)
- Termin realizacji (data/czas)
- Priorytet: wysoki, średni, niski
- Status (domyślnie: „oczekujące”)

** 📋 Lista zadań **:
- Wyświetlenie zadań w przejrzystej formie:
- Lista zawiera kolumny: [Tytuł, Termin, Priorytet, Status]
- Kolory lub ikony dla różnych priorytetów i statusów

**✅ Oznaczanie jako wykonane **:
- Przycisk do oznaczenia wybranego zadania jako „wykonane”
- Zmiana statusu i (opcjonalnie) stylu wizualnego w GUI

**🗑️ Usuwanie zadań**:
- Trwałe usuwanie zadania z listy i pliku

**💾 Trwałe przechowywanie danych**:
- Zadania zapisywane do pliku .json (np. tasks.json)
- Dane wczytywane automatycznie przy starcie aplikacji
- Obsługa błędów i brakujących plików

**⭐ Priorytety i filtrowanie**:
- Możliwość filtrowania zadań po:
  - Priorytecie
  - Statusie (wykonane, oczekujące)
  - Terminie realizacji (np. tylko zadania „na dziś”)

**🔔 Powiadomienia**:
Jeśli termin zadania zbliża się (np. dziś lub za < 1h), aplikacja informuje użytkownika (np. label lub popup)

---

## **🛠️ Technologie**
- **Python 3.8+**
- **Tkinter** – biblioteka do tworzenia graficznego interfejsu użytkownika.
- **JSON** – do zapisywania i wczytywania listy zadań.

---

## **📋 Wymagania**
- Python 3.8 lub nowszy.
- Edytor kodu lub IDE (np. PyCharm, VS Code).
- Opcjonalnie: Wirtualne środowisko Python (`venv`).

---

## **📦 Instalacja**
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/uzytkownik/to-do-list-app.git
   cd to-do-list-app

--- 

## **🔍 Zaawansowane zagadnienia Python**:
- datetime i timedelta – sprawdzanie terminów
- json – serializacja i deserializacja danych
- tkinter.messagebox – interaktywne powiadomienia
- sorted() i lambda – sortowanie listy zadań
- Walidacja danych – np. nieprawidłowy format daty
- Testy jednostkowe – np. poprawność działania TaskRepository
- Walidacja GUI – blokada przycisków, jeśli dane są niekompletne

---

## **🚀 Pomysły na rozszerzenia (dla ambitnych)**:
- Edytowanie istniejących zadań
- Zadania cykliczne (np. codzienne, tygodniowe)
- Eksport do CSV lub PDF
- Synchronizacja z chmurą (np. Firebase lub Google Tasks)
- Przeciąganie zadań myszką (drag & drop w GUI)
- Motywy kolorystyczne (dark mode/light mode)
