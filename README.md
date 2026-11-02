# Butter Club

En dansk reservationsside til en aften med butter chicken. Lavet som et almindeligt projekt, der kan åbnes og redigeres i VS Code. Kræver kun Python 3; ingen pakker skal installeres.

## Åbn siden

Åbn `butter-club.code-workspace` i VS Code. Du kan vælge **Terminal → Run Task → Start Butter Club** eller bruge terminalen nedenfor. Åbn **Terminal → New Terminal**, og kør:

```sh
python3 server.py
```

Åbn http://localhost:8000 i browseren. Stop serveren med Ctrl+C.

## Se hvem der kommer

Åbn en ny terminal i samme mappe:

```sh
python3 server.py --list
```

Eksporter en gæsteliste, der kan åbnes i Excel:

```sh
python3 server.py --export
```

Reservationer bliver gemt i `data/reservations.sqlite3`, også efter genstart. Navne og allergioplysninger vises ikke offentligt. Serveren skal køre for at tage imod reservationer. Åbning af HTML-filen alene eller med VS Code Live Server viser designet, men kan ikke gemme reservationer.

## Del med vennerne

Denne udgave er lokal og er ikke lagt på internettet. `localhost` virker kun på din egen computer. For venner på samme Wi-Fi kan du starte med `python3 server.py --host 0.0.0.0` og dele computerens lokale IP-adresse efterfulgt af `:8000`. Computeren skal være tændt, og netværket skal tillade forbindelsen. For tilmelding hjemmefra skal projektet lægges på en Python-webhost med vedvarende disk og HTTPS, eller have en sikker tunnel til din server.

## Ret indholdet

- `public/index.html`: tekster, menu, standardtidspunkt og formular.
- `public/style.css`: farver, layout og mobilvisning.
- `public/app.js`: formular og bekræftelse.
- `server.py`: validering og lagring af tilmeldinger.

Tidspunktet er et frit valg mellem kl. 16.00 og 23.30 med kl. 19.00 som forslag. Stedet står som “Grønnegade”. Google Fonts hentes online; siden bruger lokale reservefonte uden internet.


## GitHub og publicering

Dette projekt indeholder en Dockerfile til hosting af både siden og reservationerne. GitHub opbevarer kildekoden; **GitHub Pages kan ikke køre Python-serveren eller gemme reservationer**.

Når repositoryet er oprettet på din GitHub-konto, kan det forbindes til en webhost med Docker-understøttelse:

1. Vælg repositoryet og Dockerfile som opsætning.
2. Lad hosten sende trafik til serverens `PORT` (standard: 8000).
3. Tilføj en vedvarende disk på `/data`. Uden den kan reservationer forsvinde ved genstart eller en ny udgivelse. Den mappe skal være skrivbar for containerens bruger `butter`.
4. Publicer via hosten, og del dens HTTPS-link med vennerne.

`HOST`, `PORT` og `DATABASE_PATH` kan indstilles som miljøvariabler. Containeren lytter på `0.0.0.0`, og databasen ligger på `/data/reservations.sqlite3`. Gæstelisten læses på hosten med `python server.py --list`.

Databaser, gæsteliste-eksport og hemmelige miljøfiler er udeladt fra Git og Docker-bygningen. Hosting og en vedvarende disk kan koste penge; der er ikke oprettet noget hostingabonnement.
