# ADR 001 · Dove pubblicare mini-ask

- **Stato:** accettata
- **Data:** 23/11/2026

## Contesto
mini-ask è una piccola API FastAPI di esempio, già pronta in un container Docker. Voglio metterla online per imparare tutto il percorso fino alla produzione: CI, deploy, segreti, monitoraggio.
Vincoli:
- costo zero;
- usare il Dockerfile che ho già;
- niente server da gestire a mano;
- la chiave API deve stare in un segreto, non nel codice.

## Opzioni considerate
1. **Render, piano Free.** Gratis per sempre e legge il Dockerfile. Segreti nelle variabili d'ambiente, health check, deploy automatico da GitHub che può aspettare la CI verde. Contro: si addormenta dopo 15 minuti senza richieste, quindi la prima risposta è lenta (cold start), e ha poca CPU.
2. **Railway.** Comodo e con Docker. Però il piano gratuito ha solo 1 $ di consumo al mese, dopo i 30 giorni di prova con 5 $, e i servizi si addormentano dopo 5-10 minuti. Per averlo sempre acceso serve Hobby, a 5 $ al mese.
3. **AWS (App Runner, ECS o EC2).** È lo standard nelle aziende. Per un primo deploy però devo configurare a mano account, IAM, registro delle immagini e rete, e il rischio di costi non previsti è più alto. Ho iniziato a studiarlo per la certificazione Cloud Practitioner e voglio usarlo nel prossimo progetto.

## Decisione
Scelgo **Render Free**. È a costo zero, usa il mio Dockerfile senza modifiche e mi fa vedere tutti i concetti che voglio imparare: variabili d'ambiente e segreti, health check, deploy automatico solo dopo la CI verde.

## Conseguenze
- **Positive:** il servizio è online su https://mini-ask.onrender.com. Il deploy parte solo con la CI verde ("After CI Checks Pass"). Un workflow GitHub controlla `/healthz` ogni giorno.
- **Negative:** dopo 15 minuti di inattività la prima richiesta può impiegare decine di secondi. La CPU è poca, va bene per una demo ma non per un servizio vero.
- **Cosa resta valido se cambio piattaforma:** Docker, i segreti come variabili d'ambiente e la CI restano uguali. Su AWS cambiano solo dove gira il container e come si danno i permessi (IAM).
- **Quando rivedere questa scelta:** quando servirà un database che resta (il disco del container si cancella a ogni deploy) o un servizio sempre acceso. A quel punto valuto AWS.
