# Revisione di continuità e lettering — Capitolo 1, v2.0

## Obiettivo

Correggere due classi di errore della prima edizione completa:

1. testo sovrapposto a volti, mani, armi o azioni;
2. variazioni di scala, posizione e geometria nella capsula 92.

## Metodo di lettering

`scripts/build_ch01_revision.py` ricompone ogni vignetta come una coppia
verticale: fascia editoriale sopra, illustrazione sotto. Ogni riquadro porta il
nome del parlante e un colore stabile. Non vengono disegnate code e nessun testo
entra nell'arte; restano ammessi soltanto effetti sonori marginali.

## Derivati bloccati della capsula 92

Tutti i prompt hanno imposto lo stesso set: vano ovale lungo tre metri, schiuma
marrone continua, portello vicino, terminale e telefono rosa sulla parete
sinistra, pannello delle regole sulla destra, fluorescente centrale, asse
portello-testata e palette bianco sporco/nero/marrone.

### `capsule-92-case-alone-v3.png`

Scena precedente all'arrivo di Molly. Case resta vicino al portello e dispone
la .22, nove cartucce, Hitachi, fiasca e ghiacciaia. Nessun'altra persona e
nessuna seconda arma.

### `capsule-92-phone-v3.png`

Stesso vano, stessi landmark e stesso inventario. Case telefona con il ricevitore
rosa senza cambiare lato o ingrandire l'ambiente.

### `capsule-92-latch-v3.png`

Stesso vano durante l'incontro finale. Case è accovacciato sul lato del portello
e aziona il fermo; Molly resta seduta contro la testata di fondo, alla stessa
distanza del master, e impugna una sola fletcher.

## Vincoli negativi comuni

- niente testo, balloon, segnaletica leggibile o watermark;
- niente stanza rettangolare, soffitto alto o spazio per stare in piedi;
- nessun cambio di parete per terminale, telefono, pannello o portello;
- nessun personaggio duplicato e nessuna arma aggiuntiva;
- Molly non avanza verso Case durante la mira;
- Case è disarmato nella tavola 14.
