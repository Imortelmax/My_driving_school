# My Driving School

Intranet de gestion d'auto-école développé avec Django. Permet de gérer les élèves, les instructeurs, les plannings et les forfaits d'heures de conduite.

## Fonctionnalités

### 4 rôles utilisateurs

| Rôle | Capacités |
| --- | --- |
| **Student** | Consulter son planning, suivre l'avancement de ses forfaits, envoyer des demandes de RDV |
| **Instructor** | Gérer son planning, consulter les fiches de ses élèves, répondre aux demandes de RDV |
| **Secretary** | Créer/modifier/supprimer des comptes student & instructor, gérer les forfaits et leçons, consulter le planning général |
| **Admin** | Tous les droits Secretary + gestion des comptes Secretary |

### Fonctionnalités principales

- Authentification par rôle avec redirection automatique
- Gestion des leçons avec vérification des heures disponibles (blocage si forfait épuisé)
- Suivi des forfaits d'heures : déduction automatique à la création, restitution à la suppression
- Planning filtrable par instructeur ou élève (Secretary & Admin)
- Fiches élèves détaillées (heures totales / utilisées / restantes)

### Bonus implémentés

- **Demandes de RDV** : un étudiant peut envoyer une demande à un instructeur. Chaque partie peut accepter, refuser ou faire une contre-proposition, jusqu'à un accord ou un refus définitif.
- **Achat d'heures en ligne** via Stripe Checkout (paiement par carte).

## Stack technique

- **Backend** : Django 4.2, Python 3
- **Base de données** : SQLite
- **Frontend** : Bootstrap 5, Bootstrap Icons
- **Paiement** : Stripe
- **Déploiement** : Docker, Gunicorn, Nginx

## Installation locale

### Prérequis

- Python 3.10+

### Mise en place

```bash
# Cloner le projet
git clone <url-du-repo>
cd my_driving_school

# Créer et activer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt

# Copier et remplir les variables d'environnement
cp .env.example .env

# Appliquer les migrations
python manage.py migrate

# Charger les données initiales
python manage.py loaddata school/fixtures/initial_data.json

# Lancer le serveur
python manage.py runserver
```

L'application est accessible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Déploiement VPS avec Docker

### Prérequis sur le VPS

- Docker
- Docker Compose

### Étapes

```bash
# 1. Cloner le projet sur le VPS
git clone <url-du-repo>
cd my_driving_school

# 2. Créer le fichier .env à partir de l'exemple
cp .env.example .env
# Éditer .env avec vos vraies valeurs
nano .env

# 3. Construire et lancer les conteneurs
docker compose up -d --build

# 4. Vérifier que tout tourne
docker compose logs -f
```

L'application est accessible sur le port 80 de votre VPS.

### Webhook Stripe en production

Configurer le webhook Stripe sur `https://votre-domaine.com/payment/webhook/` depuis le dashboard Stripe, puis mettre à jour `STRIPE_WEBHOOK_SECRET` dans `.env`.

### Commandes utiles

```bash
# Voir les logs
docker compose logs -f web

# Redémarrer après un changement de code
docker compose up -d --build

# Accéder au shell Django
docker compose exec web python manage.py shell

# Sauvegarder la base de données
docker compose exec web cp /app/data/db.sqlite3 /app/data/db.backup.sqlite3
```

## Comptes de test

Les fixtures fournissent 4 comptes préconfigurés (mot de passe : `epitech`).

| Username | Rôle |
| --- | --- |
| `student1` | Student |
| `instructor1` | Instructor |
| `secretary1` | Secretary |
| `admin1` | Admin |

## Structure du projet

```text
my_driving_school/
├── driving_school/         # Configuration Django
│   ├── settings.py
│   └── urls.py
├── school/                 # Application principale
│   ├── models.py           # User, Package, Lesson, LessonRequest, SchoolSettings
│   ├── views.py            # Vues fonctionnelles et génériques
│   ├── forms.py            # Formulaires
│   ├── urls.py             # Routes
│   ├── decorators.py       # Décorateur role_required
│   ├── admin.py            # Interface d'administration Django
│   ├── fixtures/
│   │   └── initial_data.json
│   └── templates/
│       ├── registration/
│       │   └── login.html
│       └── school/         # Templates par rôle
├── nginx/
│   └── nginx.conf
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── .env.example
└── manage.py
```

## Variables d'environnement

| Variable | Description |
| --- | --- |
| `SECRET_KEY` | Clé secrète Django (obligatoire en prod) |
| `DEBUG` | `True` en dev, `False` en prod |
| `ALLOWED_HOSTS` | Domaines autorisés, séparés par des virgules |
| `DB_PATH` | Chemin vers le fichier SQLite (défaut : `db.sqlite3`) |
| `STRIPE_PUBLIC_KEY` | Clé publique Stripe |
| `STRIPE_SECRET_KEY` | Clé secrète Stripe |
| `STRIPE_WEBHOOK_SECRET` | Secret du webhook Stripe |
