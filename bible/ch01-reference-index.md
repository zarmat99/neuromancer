# Indice delle reference visive — Capitolo 1

Versione 1.0. L'ordine indicato qui sostituisce etichette generate dentro le
immagini, che non vengono mai affidate al modello visivo.

## Personaggi

| File | Posizione | ID |
|---|---|---|
| `assets/characters/case-v1.png` | foglio completo | `CHAR_CASE_V1` |
| `assets/characters/molly-v1.png` | foglio completo | `CHAR_MOLLY_V1` |
| `assets/characters/supporting-cast-v1.png` | sinistra / centro / destra | `CHAR_LINDA_V1` / `CHAR_RATZ_V1` / `CHAR_WAGE_V1` |
| `assets/characters/ch01-supporting-a-v2.png` | alto sx / alto dx / basso sx / basso dx | `CHAR_DEANE_V1` / `CHAR_ZONE_V1` / `CHAR_SHIN_V1` / `CHAR_KURT_V1` |
| `assets/characters/ch01-supporting-b-v2.png` | riga 1 | `CHAR_JOEBOYS_V1` / `CHAR_CLERK_V1` / `CHAR_SHOPKEEPER_V1` |
| `assets/characters/ch01-supporting-b-v2.png` | riga 2 | `CHAR_RECEPTIONIST_V1` / `CHAR_RENTACOP_V1` / `CHAR_ZONE_WORKER_V1` |
| `assets/characters/ch01-supporting-b-v2.png` | riga 3 | `CHAR_NAVAL_V1` / cliente australiano / sarariman M-G |

## Ambienti

| File | Griglia | Contenuto |
|---|---|---|
| `assets/environments/ch01-locations-v1.png` | 2 × 2 | Chatsubo / Ninsei / corridoio arcade / corte Cheap Hotel |
| `assets/environments/ch01-locations-secondary-v2.png` | 2 × 2 | Jarre de Thé / ufficio Deane / banco Shiga / negozio armi |
| `assets/environments/ch01-locations-flashbacks-v2.png` | riga 1 | porto di Chiba / hotel di Memphis / capsula povera del porto |
| `assets/environments/ch01-locations-flashbacks-v2.png` | riga 2 | Harajuku-pachinko / boutique chirurgica / esterno Cheap Hotel |
| `assets/environments/capsule-92-layout-v2.svg` | pianta + sezione | geometria dimensionale vincolante del numero 92 |
| `assets/environments/capsule-92-scene-master-v2.png` | master unico | Case al portello e Molly sulla testata di fondo |
| `assets/environments/capsule-92-holster-v2.png` | continuazione | Molly non si sposta e ripone la fletcher |

## Gerarchia delle fonti

1. Pianta dimensionale e Bibbia di produzione.
2. Reference del personaggio o dell'ambiente.
3. Master shot della sequenza.
4. Prompt della singola tavola.

Un'immagine di livello inferiore non può correggere o reinterpretare un vincolo
di livello superiore. Se emerge un conflitto, si rigenera la scena invece di
aggiornare retroattivamente la Bibbia per giustificare l'errore.
