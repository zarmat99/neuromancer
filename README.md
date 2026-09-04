# Neuromante - adattamento a fumetti

Questo repository contiene la lavorazione dell'adattamento italiano a fumetti di
*Neuromancer*. La fonte canonica è `Neuromancer - William Gibson(1).pdf`.

## Pilota: capitolo 1

Il primo pilota adatta il capitolo 1 (pagine PDF 3-29) in 14 tavole. Il pacchetto
comprende:

- bibbia narrativa e glossario italiano;
- bibbia visiva con design bloccati;
- registro di continuità pagina per pagina;
- scaletta, sceneggiatura tecnica e storyboard;
- reference sheet dei personaggi e degli ambienti;
- tre tavole campione finite: apertura, fuga dall'arcade e incontro con Molly;
- dossier PDF del pilota.

## Regola fondamentale: continuità

Ogni elemento ricorrente possiede un ID stabile (`CHAR_*`, `LOC_*`, `PROP_*`).
Le tavole possono cambiare regia e illuminazione, ma non possono ridisegnare:

- volto, corporatura, capelli o età apparente dei personaggi;
- vestiti e oggetti all'interno della stessa sequenza temporale;
- geometria riconoscibile dei luoghi ricorrenti;
- palette e linguaggio grafico della realtà fisica e del cyberspazio.

Prima di approvare una tavola va verificato `bible/continuity-ledger.md`. Le
immagini vengono prodotte senza testo incorporato; balloon, didascalie ed effetti
sonori sono aggiunti in impaginazione per garantire un italiano corretto.

## Struttura

```text
bible/              canone narrativo, visivo e lessicale
chapters/ch01/      outline, sceneggiatura, storyboard e tavole
assets/             reference sheet bloccati
prompts/            prompt e vincoli di generazione
editions/           PDF e altre edizioni esportate
scripts/            strumenti di impaginazione e verifica
```

