# Registro di continuità - Capitolo 1 — v1.0

Questo documento prevale sui prompt e sulle singole tavole. Gli elementi sono
definiti in `bible/ch01-production-bible.md`; ogni revisione che modifica un
elemento bloccato deve aggiornare prima quella Bibbia.

## Cronologia

La storia occupa una sola notte di venerdì fino all'alba di sabato.

| Tavola | Ora relativa | Luogo | Personaggi | Stato e oggetti in entrata | Stato e oggetti in uscita |
|---:|---|---|---|---|---|
| 1 | 22:30 | `LOC_CHAT_V1` | Case, Ratz | Case sobrio solo in apparenza; nessuna arma | Ratz nomina Wage |
| 2 | 22:40 / ricordo | Chat + matrice/Memphis | Case | stesso outfit | stabilito il danno neurologico |
| 3 | 23:10 | `LOC_NINSEI_V1`, `LOC_JARRE_V1` | Case | assume `PROP_DEX_V1` | inizio alterazione percettiva |
| 4 | ricordo + 23:20 | arcade/Harajuku/Jarre | Case, Linda | Linda con outfit bloccato | Linda avverte della minaccia |
| 5 | 23:25 | Jarre/Ninsei | Case, Linda | Case possiede banconota da 50 | Linda prende i 50; Case esce solo |
| 6 | 23:40 | Ninsei, vetrina, `LOC_DEANE_V1` | Case, Deane | Case disarmato | nessuna conferma da Deane |
| 7 | 00:05 | boutique chirurgica/Shiga | Case, Molly in riflesso, Shin | Molly solo silhouette coerente | Case compra `PROP_COBRA_V1` |
| 8 | 00:25 | Chat/Ninsei | Case, Zone, Molly in coda | cobra nascosto sotto giacca | Case individua di nuovo la coda |
| 9 | 00:35 | `LOC_ARCADE_V1` | Case, Molly fuori campo | cobra esteso | Case rompe finestra e prepara trappola |
| 10 | 00:40 | cubicolo/vicolo | Case, Molly | cobra in mano | caduta: dolore alla caviglia sinistra; cobra poi gettato |
| 11 | 01:10 | Shiga/`LOC_COFFIN_92_V2` | Case | ha `PROP_PISTOL_V1`; seconda dex | Hitachi, ghiacciaia e fiasca verificati |
| 12 | 03:50 | Capsula 92/Chat | Case, Ratz, Kurt, Wage, Joeboy | pistola e fiasca in tasche separate | Wage arriva; arma ancora carica |
| 13 | 04:00-04:50 | Chat/Shiga/alba | Case, Ratz, Kurt, Wage, Shin | Ratz scarica la pistola | fiasca ceduta; debito chiuso; .22 e cartucce restituite; Case disarmato |
| 14 | 05:00 | `LOC_COFFIN_92_V2` | Case, Molly | Linda ha rubato Hitachi; Case zoppica e non ha armi | fletcher riposta; lame di Molly esposte |

## Continuità dei danni e della recitazione

- Tavole 1-2: Case controllato, stanchezza evidente.
- Tavole 3-6: pupille più aperte, sudore alle mani, attenzione iperfocalizzata.
- Tavole 7-9: euforia paranoide; movimenti rapidi e postura inclinata in avanti.
- Tavola 10: paura autentica; dopo la caduta favorisce la gamba destra e zoppica
  sulla caviglia sinistra.
- Tavole 11-14: seconda dose, tremore fine, sudore e crollo progressivo; la
  zoppia resta visibile.

## Continuità delle mani e delle armi

- Case tiene spesso la mano destra sull'arma dentro la tasca; non è mancino
  stabilito, quindi le azioni a due mani sono preferibili quando possibile.
- Il cobra è presente soltanto nelle tavole 7-10.
- La pistola .22 compare soltanto nelle tavole 11-13. Dopo lo scontro Case la
  restituisce a Shin e rivende le cartucce: nella tavola 14 è disarmato.
- Molly impugna la fletcher con entrambe le mani all'inizio della tavola 14.
- Le lame di Molly escono da tutte e dieci le dita; le unghie restano borgogna.

## Continuità spaziale della capsula 92

- Pianta obbligatoria: `assets/environments/capsule-92-layout-v2.svg`.
- Ingombro interno: 3,00 × 1,00 × 1,45 m; nessun personaggio può stare in piedi.
- Case resta presso il portello, entro 0,75 m dalla testata vicina.
- Molly resta seduta contro la testata di fondo nelle vignette 14.1-14.3.
- Terminale a sinistra e pannello regole a destra guardando verso Molly.
- Le prime quattro vignette della tavola 14 sono ritagli dello stesso master shot;
  non cambiano scala, asse, distanza o lato dei personaggi.
- La fletcher resta puntata fino alla 14.4 e viene riposta nella 14.5, prima
  delle lame.

## Continuità del dialogo

- La domanda di Molly sulla pistola riceve risposta dopo che Case ha bloccato il
  portello: l'ha restituita a Shin.
- Linda non ha mandato Molly e Molly non lavora per Wage.
- Case collega da solo i due fatti; la scena deve rendere evidente l'errore di
  interpretazione senza un monologo esplicativo.
- L'ultimo avvertimento è concreto e asciutto; non vengono aggiunte battute
  generiche da film d'azione.

## Checklist obbligatoria per ogni immagine

- [ ] ID di personaggio e luogo dichiarati nel prompt.
- [ ] Volto, capelli, corporatura e outfit confrontati con la reference.
- [ ] Ora, palette e meteo coerenti con la tavola.
- [ ] Oggetti posseduti compatibili con la tabella.
- [ ] Ferite, sudore, dose di dex e zoppia corretti.
- [ ] Direzione dello sguardo e asse d'azione leggibili.
- [ ] Pianta e scala dell'ambiente coerenti con la vignetta precedente.
- [ ] Aree `SAFE_*` libere da volti, mani, armi e landmark.
- [ ] Ogni domanda operativa ha una risposta o una reazione chiara.
- [ ] Nessun testo generato nell'illustrazione.
- [ ] Nessun elemento di capitoli successivi.
