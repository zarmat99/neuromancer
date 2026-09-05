# Bibbia di produzione incrementale — Capitolo 1

Versione 2.0. Questo documento è l'autorità creativa e tecnica per il capitolo
1. In caso di conflitto prevale su prompt, storyboard e tavole. Il registro di
continuità conserva invece lo stato minuto per minuto.

L'ordine delle figure nei fogli senza etichette è registrato in
`bible/ch01-reference-index.md`.

## Regola di crescita

La Bibbia segue la storia, non la anticipa.

- Qui sono bloccati soltanto elementi mostrati o nominati nel capitolo 1.
- Un personaggio menzionato ma non visibile riceve una funzione narrativa, non
  un volto inventato.
- Quando un capitolo successivo aggiungerà informazioni, si creerà una nuova
  versione dell'elemento senza contraddire ciò che il lettore ha già visto.
- Le scelte non esplicitate dalla fonte sono marcate come scelte di produzione e
  possono cambiare soltanto prima della prima tavola finita che le usa.

## Canone e perimetro

- Fonte: `Neuromancer - William Gibson(1).pdf`.
- Sezione: Parte I, capitolo 1, pagine PDF 3-29.
- Tempo diegetico: una notte di venerdì, dalle 22:30 circa all'alba di sabato.
- Punto di vista: Case, salvo establishing shot e dettagli necessari alla
  chiarezza dell'azione.
- Conoscenza concessa al lettore: Molly resta una coda anonima fino alla tavola
  14; la sua affiliazione e il suo mandante non vengono anticipati.

## Promessa narrativa

Il capitolo non racconta semplicemente una fuga. Racconta un uomo che interpreta
ogni segnale secondo il proprio desiderio di autodistruzione. Linda innesca la
paranoia, Case costruisce da solo la minaccia, Molly attraversa quel delirio con
freddezza professionale. Il cliffhanger funziona quando il lettore capisce che
Case ha sbagliato quasi tutto, ma che il suo errore lo ha condotto a un'offerta.

### Arco emotivo di Case

| Fase | Tavole | Stato interno | Recitazione visibile |
|---|---:|---|---|
| Controllo artificiale | 1-2 | cinismo, lutto per la matrice | spalle chiuse, sguardo basso |
| Accelerazione | 3-6 | dex, desiderio, sospetto | sudore, pupille aperte, fuoco sui dettagli |
| Paranoia operativa | 7-9 | il pericolo sembra una corsa | busto in avanti, gesti precisi e rapidi |
| Paura animale | 10 | il gioco torna reale | occhi larghi, respiro corto, fuga cieca |
| Crollo | 11-13 | seconda dose, sonno, falsa resa dei conti | tremore, zoppia, sorriso vuoto |
| Disarmo | 14 | scoperta dell'errore e curiosità | accovacciato, esausto, sarcasmo residuo |

## Grammatica visiva

- Retrofuturo industriale e analogico; superfici usate, riparate, vendibili.
- China precisa, neri profondi, colore pittorico controllato; niente estetica
  anime, supereroistica o fantascienza sterile.
- Realtà fisica: gutter bianco sporco. Ricordo della matrice: gutter nero.
- La distorsione da dex può alterare riflessi e prospettiva soggettiva, mai la
  fisionomia, la taglia di una stanza o la posizione di un personaggio.
- Una sequenza nello stesso ambiente parte sempre da una pianta e da un asse di
  ripresa. I campi stretti sono ritagli o avvicinamenti coerenti, non nuovi set.

### Palette della notte

| Ambito | Base | Accenti | Luce |
|---|---|---|---|
| Porto / Ninsei | antracite, oliva, grigio TV | rosso e ciano | pioggia, quarzo, neon |
| Chatsubo | bruno, verde bottiglia | ambra, rosa protesi | lampade basse e sporche |
| Jarre de Thé | plastica perla opaca | rosso neon, blu Linda | specchi velati |
| Deane | legno finto, verde scuro | ottone, rosa quarzo | lampada da scrivania |
| Arcade / vicolo | blu sporco, nero | bianco d'allarme | fluorescente intermittente |
| Cheap Hotel | vetroresina bianca | verde plastica, marrone | fluorescente freddo |
| Alba | grigio che vira al rosa sporco | neon che muore | cielo diffuso |

## Registro dei personaggi

### Personaggi visibili e bloccati

| ID | Presenza | Firma immediata | Stato nel capitolo |
|---|---|---|---|
| `CHAR_CASE_V1` | tavole 1-14 | magro, giacca kaki, volto insonne | POV; zoppica dalla 10 |
| `CHAR_MOLLY_V1` | riflessi 7-8, tavole 10 e 14 | lenti argento innestate, nero opaco | coda; si presenta alla fine |
| `CHAR_LINDA_V1` | tavole 3-5, ricordi | tuta blu, fascia di seta, sanpaku | avverte Case e ruba l'Hitachi |
| `CHAR_RATZ_V1` | tavole 1-2, 12-13 | mole, denti d'acciaio, protesi rosa | protegge la neutralità del Chat |
| `CHAR_WAGE_V1` | tavole 12-13 | seta canna di fucile, occhi verde mare | creditore, non mandante dell'agguato |
| `CHAR_DEANE_V1` | tavola 6 | volto rosa levigato, sartoria d'epoca | informatore opaco |
| `CHAR_ZONE_V1` | tavole 1 e 8 | volto lungo, palpebre basse, pupille enormi | pappone e informatore lento |
| `CHAR_SHIN_V1` | tavole 7, 11 e raccordo 13 | giovane cameriere del sushi, gesti minimi | noleggia e riprende la .22 |
| `CHAR_KURT_V1` | tavole 12-13 | giovane brasiliano, presenza asciutta | copre Wage col fucile antisommossa |
| `CHAR_JOEBOYS_V1` | tavole 12-13 | coppia quasi identica, muscoli innestati | scorta di Wage |
| `CHAR_CLERK_V1` | tavole 11 e 13 | adolescente giapponese, libro alla console | lascia entrare Linda con la chiave |
| `CHAR_SHOPKEEPER_V1` | tavola 7 | anziana giapponese, mani macchiate | vende il cobra |
| `CHAR_RECEPTIONIST_V1` | tavola 9 | giovane giapponese, maglia nera | chiama la sicurezza |
| `CHAR_RENTACOP_V1` | fuori campo 9, esito 10/14 | guardia economica con nunchaku | ferito da Molly, non mostrato in dettaglio |
| `CHAR_ZONE_WORKER_V1` | tavola 1 | abbronzatura improbabile, risata tesa | punge Case e si allontana |
| `CHAR_NAVAL_V1` | tavola 1 | alto africano, uniforme, cicatrici rituali | ancora visiva del pubblico del Chat |

### Modelli principali

#### `CHAR_CASE_V1` — Henry Dorsett Case

- 24 anni; alto, molto magro, spalle strette e alte.
- Viso pallido, stretto e angolare; zigomi netti, guance scavate, occhiaie.
- Capelli castano nerissimo, corti, irregolari, spesso bagnati.
- Outfit unico: giacca a vento kaki di nylon macchiata, maglia scura, jeans neri
  scoloriti, scarpe da corsa di nylon.
- Non diventa muscoloso o elegante. Anche quando agisce bene sembra consumato.
- Dopo la caduta: dolore alla caviglia sinistra; carica la gamba destra.
- Mani: in tasca quando nasconde paura; precise soltanto davanti a un problema.

#### `CHAR_MOLLY_V1` — Molly

- Donna adulta, 25-30 anni; snella, atletica, movimenti economici.
- Viso ovale-affilato, zigomi alti, bocca controllata; shag nero corto e ruvido.
- Lenti argento chirurgicamente innestate: crescono dalla pelle, senza stanghette,
  occhi mai visibili.
- Giacca nera voluminosa e opaca, pantaloni aderenti di pelle nera, stivali neri.
- Unghie artificiali borgogna; sotto ciascuna alloggia una lama a doppio filo di
  quattro centimetri.
- Non posa per intimidire: resta immobile, misura lo spazio, poi agisce.
- Nel numero 92 siede contro la parete di fondo con le ginocchia alzate. Non
  cambia posto finché la fletcher non viene riposta.

#### `CHAR_LINDA_V1` — Linda Lee

- 20 anni; minuta, tesa, fragile senza essere infantile.
- Occhi grigi, trucco nero sbavato, pelle pallida sotto gli occhi, nuove linee di
  dolore agli angoli della bocca; un millimetro di bianco sotto le pupille.
- Capelli scuri fermati da una fascia di seta stampata come circuito o mappa.
- Tuta orbitale francese blu scolorita, maniche strappate; scarpe bianche nuove.
- Tremore e bisogno non vanno resi glamour. Quando mente evita per un istante lo
  sguardo di Case, poi lo fissa per costringerlo a crederle.

#### `CHAR_RATZ_V1` — Ratz

- Circa 120 kg; enorme, flaccido, testa rasata e sudata, camicia bianca tesa.
- Denti: rete d'acciaio est-europeo e carie marroni.
- Protesi militare russa a sette funzioni, plastica rosa sporca: braccio destro.
  Il braccio umano serve la birra quando la scena richiede delicatezza.
- È sarcastico ma non crudele con Case. Il bar è il suo territorio morale.

#### `CHAR_WAGE_V1` — Wage

- 35-45 anni; abbronzatura uniforme, volto volutamente dimenticabile.
- Occhi artificiali verde mare, completi trapianti Nikon.
- Completo di seta canna di fucile, camicia scura, un bracciale di platino per
  polso.
- Non alza la voce. Tratta debito e minaccia come la stessa pratica contabile.

#### `CHAR_DEANE_V1` — Julius Deane

- 135 anni; volto rosa, continuo, quasi senza pori; età apparente indefinibile.
- Occhiali d'oro sottili con lenti sfaccettate di quarzo sintetico rosa.
- Completi e cravatte ricostruiti sul primo Novecento; nodo sempre perfetto.
- Siede dietro una scrivania enorme e mantiene una distanza protetta.
- Non è caricaturale: la stranezza nasce dalla pazienza e dall'assenza di usura.

### Modelli secondari

Le voci in corsivo sono scelte di produzione necessarie alla serialità.

- `CHAR_ZONE_V1`: adulto, volto lungo e rilassato, fronte liscia, palpebre
  cadenti, pupille dilatate fino a cancellare quasi iride e bianco. Dipendente dai
  Cloud Dancers. Scelta di produzione: completo morbido grigio-fumo, camicia
  aperta, nessun gioiello.
- `CHAR_SHIN_V1`: giovane adulto giapponese, asciutto, impassibile. Scelta di
  produzione: giacca da banco grigio chiaro, grembiule blu scuro; capelli corti
  pettinati in avanti.
- `CHAR_KURT_V1`: giovane adulto brasiliano, magro e saldo. Scelta di produzione:
  testa rasata ai lati, canottiera scura sotto un grembiule; niente innesti
  evidenti.
- `CHAR_JOEBOYS_V1`: due giovani adulti quasi identici, braccia e spalle gonfiate
  da innesti muscolari. Scelta di produzione: bomber neri gemelli; uno con riga
  nei capelli, l'altro rasato, per poterli tracciare senza rompere l'effetto di
  coppia.
- `CHAR_CLERK_V1`: adolescente giapponese dietro la console a C; corporatura
  piccola, felpa neutra, manuale scolastico diverso tra notte e alba.
- `CHAR_SHOPKEEPER_V1`: anziana giapponese; volto scavato e dita brune macchiate;
  abiti da negozio neutri. La mano che apre il cobra è il suo tratto distintivo.
- `CHAR_RECEPTIONIST_V1`: giovane adulta giapponese, maglia nera senza maniche,
  terminale bianco e manifesto dell'Egeo alle spalle.
- `CHAR_RENTACOP_V1`: adulto; uniforme economica grigia e nunchaku. Nel capitolo
  è soprattutto suono e conseguenza; niente ritratto eroico.
- `CHAR_ZONE_WORKER_V1`: adulta; abbronzatura vistosamente artificiale. Deve
  leggere come lavoratrice del locale, non come decorazione erotica.
- `CHAR_NAVAL_V1`: uomo africano alto, uniforme navale pulita, file precise di
  cicatrici rituali sugli zigomi. Nessuna funzione dialogica.

### Nominati ma non disegnati nel capitolo 1

| Nome | Informazione concessa ora | Regola |
|---|---|---|
| McCoy Pauley | maestro e leggenda dei cowboy | nessun volto prima dell'ingresso in scena |
| Bobby Quine | altro maestro di Case | nessun volto prima dell'ingresso in scena |
| Mona | fonte indiretta dell'avvertimento di Linda | non visualizzare |
| compagno di Mona | uno degli uomini di Wage | non identificarlo con i Joeboy presenti |
| Matsuga | vecchio contatto di affari | non visualizzare |
| Snake Man | compratore di Tokyo, solo voce | silhouette telefonica non identificante |
| compratore di Hong Kong | non risponde alla chiamata | nessun volto o voce |
| ex datori di Case | autori del danno neurologico | mani/sagome anonime nel ricordo |

## Voci e recitazione verbale

Il dialogo non viene tradotto frase per frase. Per ogni battuta si conserva
prima l'intenzione, poi si riscrive come parlerebbe quel personaggio in italiano.

| Voce | Ritmo | Lessico | Cosa evita |
|---|---|---|---|
| Case | corto, difensivo | ironia secca, biz, nomi propri | confessioni, frasi eleganti |
| Molly | preciso, calmo | verbi concreti, domande operative | spiegazioni, minacce teatrali |
| Linda | spezzato ma diretto | parole comuni, ripetizioni minime | poesia involontaria |
| Ratz | ampio, ironico | “artista”, immagini corporee | slang giovanile italiano |
| Wage | contabile | debito, accordo, domanda diretta | monologhi da gangster |
| Deane | cortese, obliquo | “ragazzo mio”, formule educate | volgarità e fretta |
| Zone | lento | risposte minime | dettagli non richiesti |
| Shin | telegrafico | prezzo, tempo, oggetto | giustificazioni |

### Regole di adattamento dei dialoghi

- Ogni balloon esprime una sola intenzione.
- Obiettivo 4-12 parole; massimo 16, salvo una battuta deliberatamente ampia di
  Ratz o Deane.
- Niente calchi come “è così che sono cablata”, “vuole vederti con un buco” o
  “faccio affari quasi onesti” se in italiano suonano tradotti.
- Lo slang del mondo (`biz`, `cowboy`, `dex`, `Joeboy`, `Sprawl`) resta stabile;
  lo slang inglese generico (`man`, `buddy`, `sweetheart`) si traduce per
  relazione, non parola per parola.
- La didascalia aggiunge percezione o causalità; non descrive ciò che il disegno
  mostra già.
- Una domanda introdotta in una tavola riceve risposta o reazione leggibile.

## Registro degli ambienti

### Ambienti mostrati e bloccati

| ID | Tavole | Landmark obbligatori |
|---|---:|---|
| `LOC_PORT_V1` | 1-3 | gru, fari al quarzo, baia nera, cielo TV |
| `LOC_CHAT_V1` | 1-2, 8, 12-13 | bancone lungo, porta plastica, tavoli posteriori |
| `LOC_NINSEI_V1` | 1, 3, 5-8, 11, 13 | asfalto bagnato, insegne verticali, folla gaijin |
| `LOC_JARRE_V1` | 3-5 | specchi rettangolari, neon rosso, laminato bruno |
| `LOC_ARCADE_V1` | 4, 8-10 | sala giochi, scala, corridoio, cubicoli, vicolo |
| `LOC_DEANE_V1` | 6 | magazzino, foyer anacronistico, ufficio protetto |
| `LOC_SHIGA_STALL_V1` | 7, 11, raccordo 13 | banco sushi, retro con barattoli di rafano |
| `LOC_WEAPON_SHOP_V1` | 6-7 | vetrina shuriken, velluto rosso, banco terminale |
| `LOC_SURGICAL_WINDOW_V1` | 7 | vetrina scura, pelle coltivata su finta giada |
| `LOC_CHEAP_EXT_V1` | 11 | mattoni gialli, ascensore trasparente applicato |
| `LOC_CHEAP_ROOF_V1` | 11, 13 | prato plastico, console a C, griglia 6×10 capsule |
| `LOC_COFFIN_92_V2` | 11, 14 | 3 m, sezione ovale, schiuma marrone, terminale |
| `LOC_MEMPHIS_FLASH_V1` | 2 | stanza d'hotel anonima, letto e cinghie, clinica mobile |
| `LOC_PORT_COFFIN_FLASH_V1` | 2, 4 | capsula economica più povera del Cheap Hotel |
| `LOC_HARAJUKU_FLASH_V1` | 4 | pioggia, boutique, mantelle trasparenti, pachinko |

### Geometrie ricorrenti

#### `LOC_CHAT_V1` — Chatsubo

- Sala stretta, soffitto basso; bancone graffiato lungo la parete sinistra
  entrando, porta di plastica traslucida in fondo all'asse.
- Spillatori Kirin e bottiglie dietro Ratz; sgabelli davanti al bancone.
- Tavoli posteriori sulla destra: qui Ratz beve e avviene il confronto con Wage.
- Kurt può vedere porta e tavolo dal bancone; il suo tiro non attraversa Case.

#### `LOC_JARRE_V1` — Jarre de Thé

- Sala stretta; specchi rettangolari su due pareti, ciascuno bordato di neon rosso.
- Tavoli di laminato bruno graffiato; plastiche milanesi pallide e patina opaca.
- Case siede rivolto verso la porta; Linda di fronte. La gabbia di riflessi sulla
  sua uscita deriva dagli stessi pannelli, non da uno spazio nuovo.

#### `LOC_ARCADE_V1` — arcade, uffici e vicolo

- Piano terra rumoroso; scala grezza sul lato destro verso un corridoio rettilineo.
- Reception aperta all'inizio del corridoio; porte blu identiche sui due lati.
- Gli ultimi due cubicoli sono adiacenti. Case sfonda il primo come diversivo,
  entra nel secondo e rompe la finestra sulla parete di fondo.
- Il vicolo corre parallelo al corridoio. Sotto la finestra: cartone fradicio,
  fibre ottiche e chassis di console. Molly guarda dall'alto, Case cade sotto.

#### `LOC_CHEAP_ROOF_V1` — corte e capsule

- Corte rettangolare sul tetto, coperta da stuoia laminata.
- Console a C al centro di prato plastico verde.
- Sessanta capsule bianche in impalcatura: sei livelli per dieci.
- Il numero 92 è sul terzo livello, raggiunto da scala e passerella in griglia.

#### `LOC_COFFIN_92_V2` — capsula 92

La geometria esecutiva è in `assets/environments/capsule-92-layout-v2.svg`.

- Ingombro interno bloccato: lunghezza 3,00 m; larghezza massima 1,00 m; altezza
  massima 1,45 m. Larghezza e altezza sono una scelta di produzione ricavata
  dalle dimensioni del portello indicate nella fonte.
- Portello ovale sulla testata vicina; si solleva verticalmente. Case entra e
  rimane entro i primi 0,75 m.
- Pavimento/letto unico in schiuma temper marrone su tutta la lunghezza.
- Terminale e telefono rosa modellati nella parete sinistra guardando verso il
  fondo, tra 0,60 e 1,25 m dal portello.
- Pannello delle regole sulla parete opposta. Ghiacciaia bianca vicino alla
  testata, sul lato destro, senza bloccare il passaggio.
- Molly è centrata sulla parete di fondo a x=2,65 m, schiena contro la curva,
  ginocchia alzate, talloni nella schiuma; la fletcher poggia sopra i polsi.
- Asse principale: centro del portello → centro della parete di fondo. Non si
  oltrepassa l'asse e non si usa un grandangolo che trasformi la capsula in stanza.
- Tavola 14: posizione di Molly e ingombro della capsula invariati. I campi
  derivano da `capsule-92-scene-master-v2.png`; la chiusura del fermo usa
  `capsule-92-latch-v3.png`, generata sullo stesso asse e con gli stessi
  landmark. Le viste preparatorie della tavola 11 usano
  `capsule-92-case-alone-v3.png` e `capsule-92-phone-v3.png`.

### Luoghi soltanto nominati

Namban, Tokyo, Yokohama, Hong Kong, Amsterdam, Chiba Hilton e le cliniche nere
restano parole o frammenti non identificanti. Non ricevono ancora un design.

## Oggetti e passaggi di mano

| ID | Aspetto | Entrata | Uscita / stato finale |
|---|---|---:|---|
| `PROP_DEX_V1` | ottagono rosa piatto | 3 | seconda dose in 11; non contato oltre |
| `PROP_YEHEYUAN_V1` | pacchetto spiegazzato, filtro | 4 | sigarette a Linda e Case |
| `PROP_SHURIKEN_V1` | stelle cromate su velluto rosso | 6 | simbolo; Case non compra |
| `PROP_COBRA_V1` | tubo opaco, tre molle, punta bronzea | 7 | collassa in 10; gettato in 11 |
| `PROP_PISTOL_V1` | copia PPK .22, guance rosse a drago | 11 | scaricata in 13; restituita a Shin prima di 14 |
| `PROP_HITACHI_V1` | computer tascabile grigio chiaro | 11 | rubato da Linda; assente in 14 |
| `PROP_KEY_V1` | nastro magnetico rigido anonimo | 11 | Linda ne ha una copia o lo usa; Case lo conserva |
| `PROP_COOLER_V1` | ghiacciaia di polistirolo bianca | 11 | resta nella capsula |
| `PROP_FLASK_V1` | fiasca da laboratorio in alluminio | 11 | consegnata a Wage in 13 |
| `PROP_FLETCHER_V1` | pistola nera, bocca a pepperbox | 14 | puntata, poi riposta nella giacca |
| `PROP_BLADES_V1` | dieci lame a doppio filo, 4 cm | 14 | esposte e ritratte nella stessa scena |
| `PROP_RIOTGUN_V1` | S&W enorme, cinque cartucce arancio | 12 | resta con Kurt |
| `PROP_ASHTRAY_V1` | plastica verde Tsingtao | 13 | schiacciato da Ratz |

### Correzione obbligatoria dell'arma di Case

La .22 non è presente nello scontro finale con Molly. Dopo il Chatsubo, Case la
riporta a Shin, recupera il deposito e rivende le cartucce a metà prezzo. La
domanda di Molly serve a verificare questo stato e Case deve rispondere.

## Lettering e aree sicure

- Arte e lettering sono due livelli separati. Ogni vignetta parlata riserva una
  fascia scura sopra l'immagine; il testo non viene mai sovrapposto all'arte.
- Ogni riquadro mostra il nome del parlante e usa un colore stabile per voce.
  Pensieri, narrazione e voce fuori campo hanno etichette proprie.
- Volti, lenti, mani, armi, oggetti scambiati, ferite, portelli e landmark sono
  sempre completamente visibili.
- Se il botta e risposta non entra con un corpo leggibile, si riscrive, si amplia
  la fascia oppure si aggiunge una vignetta.
- Gli effetti sonori sono gli unici elementi ammessi sull'immagine: restano sul
  margine e non possono coprire un punto focale.
- Ordine di lettura occidentale, dall'alto a sinistra verso il basso a destra.

### Tavola 14 — aree protette

| Vignetta | Protetto | Area testo ammessa |
|---|---|---|
| 14.1 | asse completo, portello, terminale, fletcher | fascia nera superiore |
| 14.2 | posizione di Case e mira di Molly | fascia nera superiore |
| 14.3 | lenti, fletcher, distanza tra i due | fascia nera superiore |
| 14.4 | entrambi sullo stesso asse | fascia nera superiore ampliata |
| 14.5 | mano che ripone l'arma, volto di Molly | fascia nera superiore |
| 14.6 | tutte e dieci le lame, lenti, bocca | fascia nera sopra il ritratto |

## Errori vietati

- Capsula 92 larga come una stanza, altezza in piedi o scala variabile.
- Molly che avanza verso Case mentre continua a puntarlo nella tavola 14.
- Molly con occhiali normali, stanghette o occhi visibili.
- Case armato nella tavola 14.
- Ratz con protesi sul braccio sinistro o con due braccia meccaniche.
- Linda glamour, pin-up o con outfit diverso tra Jarre e ricordo immediato.
- Joeboy confusi con Molly nella falsa pista sulla “figura magra in nero”.
- Lettering che copre informazione visiva o dialoghi che lasciano una domanda
  operativa senza risposta.
- Calchi inglesi che un italiano non pronuncerebbe spontaneamente.
- Tecnologia immacolata, neon puliti, strade vuote, pseudo-giapponese leggibile.

## Gate di approvazione

Una tavola passa alla versione finita soltanto se:

1. personaggi, outfit, oggetti e danni coincidono con gli ID;
2. la pianta dell'ambiente e l'asse di ripresa sono dichiarati;
3. ogni battuta è stata verificata per intenzione, voce e naturalezza italiana;
4. ogni fascia di lettering precede la propria immagine e identifica il parlante;
5. una prova in scala pagina rende leggibili testo e azione senza sovrapposizioni;
6. il confronto affiancato con la tavola precedente non mostra salti di scala,
   lato, luce o posizione.
