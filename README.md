# Neuromante - adattamento a fumetti

Questo repository contiene la lavorazione dell'adattamento italiano a fumetti di
*Neuromancer*. La fonte canonica è `Neuromancer - William Gibson(1).pdf`.

## Pilota: capitolo 1

Il primo pilota adatta il capitolo 1 (pagine PDF 3-29) in 14 tavole. La revisione
0.2 comprende:

- Bibbia incrementale completa del capitolo 1: cast visibile, voci, luoghi,
  oggetti, cronologia, geometrie e lettering;
- reference visive per personaggi principali, secondari e comparse funzionali;
- reference degli ambienti primari, secondari e di flashback;
- registro di continuità pagina per pagina;
- scaletta, sceneggiatura tecnica e storyboard;
- tre tavole campione finite: apertura, fuga dall'arcade e incontro con Molly;
- dossier PDF del pilota.

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
vengono prodotte senza testo incorporato; balloon, didascalie ed effetti sonori
sono aggiunti in aree sicure già previste nello storyboard.

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
