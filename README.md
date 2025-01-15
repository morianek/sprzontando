# sprzątando

Sprzątando to kompleksowa aplikacja zaprojektowana do łączenia klientów z pracownikami. Klienci mogą tworzyć oferty na usługi, takie jak sprzątanie domu, a pracownicy mogą akceptować te oferty lub aplikować na inne wybrane przez siebie oferty.

## Funkcje

- **Zarządzanie klientami**: Klienci mogą tworzyć i zarządzać ofertami na różne usługi.
- **Zarządzanie pracownikami**: Pracownicy mogą przeglądać, aplikować i akceptować oferty.
- **Backend**: Zbudowany z użyciem Django do obsługi logiki po stronie serwera.
- **Frontend**: Zintegrowany z szablonami Django, aby zapewnić płynne doświadczenie użytkownika.

## Instalacja

Aby rozpocząć pracę z projektem sprzątando, wykonaj następujące kroki (zalecane jest użycie środowiska wirtualnego):

1. Sklonuj repozytorium:
    ```sh
    git clone https://github.com/morianek/sprzontando
    cd sprzontando
    ```

2. Zainstaluj wymagane zależności:
    ```sh
    pip install -r requirements.txt
    ```

3. Zastosuj migracje:
    ```sh
    python manage.py migrate
    ```

4. Uruchom serwer deweloperski:
    ```sh
    python manage.py runserver
    ```

## Użytkowanie

- **Klienci**: Utwórz konto, zaloguj się i utwórz oferty na potrzebne usługi.
- **Pracownicy**: Przeglądaj dostępne oferty, aplikuj na prace lub akceptuj oferty bezpośrednio.

## Wkład

Aby przyczynić się do projektu sklonuj repozytorium i utwórz nowy branch. Następnie zatwierdź zmiany i zapisz je w repozytorium. Na koniec utwórz nowego Pull Requesta.
