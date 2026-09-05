# Neuromante - adattamento a fumetti

Questo repository contiene la lavorazione dell'adattamento italiano a fumetti di
*Neuromancer*. La fonte canonica è `Neuromancer - William Gibson(1).pdf`.

## Capitolo 1 completo

La versione 2.0 adatta il capitolo 1 (pagine PDF 3-29) in 14 tavole finite. Il
pacchetto comprende:

- Bibbia incrementale completa del capitolo 1: cast visibile, voci, luoghi,
  oggetti, cronologia, geometrie e lettering;
- reference visive per personaggi principali, secondari e comparse funzionali;
- reference degli ambienti primari, secondari e di flashback;
- registro di continuità pagina per pagina;
- scaletta, sceneggiatura tecnica e storyboard;
- quattordici tavole illustrate e letterate in italiano;
- tavola 14 ricostruita da un master spaziale unico e derivati controllati;
- lettering ricomposto in fasce editoriali separate dall'arte, con parlante
  identificato e nessuna sovrapposizione su volti, mani, armi o azioni;
- PDF solo-fumetto con copertina e 14 tavole:
  `editions/neuromante-capitolo-01-completo.pdf`.

Il precedente dossier pilota resta come archivio di produzione; non è incluso
nel PDF del fumetto completo.

La Bibbia cresce capitolo per capitolo: i nomi soltanto citati non ricevono un
volto finché la storia non li mostra.

## Regola fondamentale: continuità

Ogni elemento ricorrente possiede un ID stabile (`CHAR_*`, `LOC_*`, `PROP_*`).
Le tavole possono cambiare regia e illuminazione, ma non possono ridisegnare:

- volto, corporatura, capelli o età apparente dei personaggi;
- vestiti e oggetti all'interno della stessa sequenza temporale;
- geometria riconoscibile dei luoghi ricorrenti;
- palette e linguaggio grafico della realtà fisica e del cyberspazio.

Prima di approvare una tavola vanno verificati
`bible/ch01-production-bible.md` e `bible/continuity-ledger.md`. Le immagini
vengono prodotte senza testo incorporato. Dialoghi, pensieri e didascalie sono
collocati in fasce dedicate sopra la relativa immagine; gli effetti sonori sono
gli unici elementi ammessi sull'arte e restano ai margini dell'azione.

I dialoghi vengono riscritti per intenzione e sottotesto in italiano naturale,
non tradotti seguendo la sintassi inglese. Il pass è documentato in
`bible/ch01-dialogue-pass.md`.

## Struttura

```text
bible/              canone narrativo, visivo e lessicale
chapters/ch01/      outline, sceneggiatura, storyboard e tavole
assets/             reference sheet bloccati
prompts/            prompt e vincoli di generazione
editions/           PDF e altre edizioni esportate
scripts/            strumenti di impaginazione e verifica
```
