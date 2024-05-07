Kod źródłowy projektu pt. *Badanie wpływu urządzenia rozpoznającego emocje na jakość komunikacji osób niewidomych i niedowidzących*

## `server.py`
Program, który ma być uruchomiony na serwerze działającym na dowolnej dystrybucji Linuksa.
Wymagania:
- Program musi być uruchomiony przez użytkownika o nazwie `jan`
- Repozytorium musi się znajdować pod ścieżką `/home/jan/naukolatek`
- Na serwerze musi być skonfigurowane bezpośrednie połączenie Wi-Fi, gdzie serwer ma adres IP `10.42.0.1`
- Należy zainstalować wszystkie wymagane biblioteki Pythona

## `client.py`
Program, który ma być uruchomiony na kliencie, czyli Raspberry Pi Zero 2 na najnowszym Raspberry Pi OS
Wymagania:
- Program musi być wywołany w pliku `/etc/rc.local`, żeby uruchomić go po włączeniu urządzenia
- Na urządzeniu musi istnieć użytkownik o nazwie `pi`
- Repozytorium musi się znajdować pod ścieżką `/home/pi/naukolatek`
- Klient musi być połączony z siecią Wi-Fi serwera i mieć adres IP `10.42.0.2`
- Należy zainstalować wszystkie wymagane biblioteki Pythona

## Klucze SSH
Należy skonfigurować następujące klucze SSH:
- między `jan@10.42.1` a `pi@10.42.0.2`
- między `root@10.42.0.2` a `jan@10.42.0.1`
