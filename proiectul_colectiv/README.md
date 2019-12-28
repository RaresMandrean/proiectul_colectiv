###Tutorial pentru setup local

# 1. Clonare repo

Clonezi de pe BitBucket proiectul 

# 2. Instalare pachete

Deschizi proiectul in Pycharm (de preferat). Dupa aceea, intri in terminalul de PyCharm. Se presupune ca nu schimbi 
calea standard cu care se deschide proiectul din terminal (asigura-te ca esti la radacina). Rulezi urmatoarea comanada
in terminal:
```pip install -r requirements.txt```

# 3. Incarcare migrari

In terminal in calea unde este manage.py rulezi comanda:
```python manage.py migrate```

# 4. Incarcare fixturi

Din aceeasi cale, din terminal rulezi urmatoarea comanda:
```python manage.py loaddata proiectul_colectiv/fixtures/groups.json```

# 5. Ultimul pas din tutorial

Continui de aici exact cum este precizat in tutorialul din documentatie, de ex. creezi un superuser, rulezi server-ul, 
si asa mai departe.