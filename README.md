# Vježbe iz kolegija Baze podataka 2

**Nositelj kolegija:** [Daniel Vasić](https://github.com/danielvasic)

**Demo programske podrške:** [Ovdje](http://129.152.0.114:5000/) možete pronaći pokrenut primjerak programa.

Dobro došli u repozitorij vježbi za kolegij **Baze podataka 2**. Ovaj kolegij se izvodi na Fakultetu prirodoslovno-matematičkih i odgojnih znanosti Sveučilišta u Mostaru. Studijski program očekuje od studenata da se upuste u učenje i istraživanje naprednih koncepta razvoja web aplikacija, koristeći niz modernih tehnologija, uključujući:

- Razvoj sustava baziranih na web tehnologijama za upravljanje podacima u bazi podataka,
- Korištenje Docker tehnologije,
- Razvoj aplikacija korištenjem Docker platforme,
- Korištenje JQuery i Flask tehnologija za rad s podacima u stvarnom vremenu,
- Korištenje Kafka i Redis za uspješnu komunikaciju i smanjenje opterećenja na sustav.

Za pokretanje aplikacije lokalno sve što je potrebno je pokrenuti sljedeću naredbu:

```
docker compose up --build
```
Napomena: Pripaziti prilikom pokretanja na atribut `platform: linux/x86_64` u `docker-compose.yaml` datoteci ukoliko pokrećete na **Windows** operacijskom sustvu ukloniti ovaj atribut iz YAML datoteke.


Relacijski model baze podataka implementiran u SQLAlchemy programskom okruženju:

![ERD](petsmodel.png)

Aplikacija kroz MySQL bazu podataka osigurava trajnost podataka, a kroz Redis sustav osigurava cache-ing za brzo dohvaćanje podataka. Za komunikaciju u stvarnom vremenu korištena je Kafka.
