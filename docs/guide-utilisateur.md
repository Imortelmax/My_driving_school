# Guide utilisateur — My Driving School

Ce guide explique comment utiliser l'intranet au quotidien, rôle par rôle. Il s'adresse aux utilisateurs finaux (élèves, moniteurs, secrétaires, administrateurs) et non aux développeurs — pour l'installation et le déploiement, voir le [README](../README.md).

> **Langue de l'interface** : l'application est en anglais. Les libellés de boutons et de menus sont donc cités en anglais dans ce guide (`Buy Hours`, `New Request`…), pour que vous les retrouviez tels quels à l'écran.

## Sommaire

- [Se connecter](#se-connecter)
- [Guide de l'élève (Student)](#guide-de-lélève-student)
- [Guide du moniteur (Instructor)](#guide-du-moniteur-instructor)
- [Guide de la secrétaire (Secretary)](#guide-de-la-secrétaire-secretary)
- [Guide de l'administrateur (Admin)](#guide-de-ladministrateur-admin)
- [Comprendre le solde d'heures](#comprendre-le-solde-dheures)
- [Problèmes courants](#problèmes-courants)

---

## Se connecter

1. Rendez-vous sur l'adresse de l'application. Vous êtes automatiquement redirigé vers la page de connexion.
2. Saisissez votre **nom d'utilisateur** (`username`) et votre **mot de passe**, puis validez.
3. Vous arrivez directement sur le tableau de bord correspondant à votre rôle.

**Il n'y a pas d'inscription en ligne.** Les comptes sont créés par la secrétaire ou l'administrateur de l'auto-école, qui vous communiquent vos identifiants. Si vous les avez perdus, contactez le secrétariat : il peut redéfinir votre mot de passe (il n'existe pas de procédure « mot de passe oublié » en autonomie).

En cas d'erreur de saisie, le message `Invalid username or password.` s'affiche sous le formulaire.

Pour vous déconnecter, cliquez sur **Logout** en haut à droite, dans la barre de navigation.

> Chaque rôle ne voit que ses propres pages. Si vous tentez d'ouvrir une page réservée à un autre rôle, vous êtes automatiquement renvoyé vers votre propre tableau de bord.

---

## Guide de l'élève (Student)

Menu latéral disponible : **Dashboard**, **My Schedule**.

### Consulter mon tableau de bord

Le **Dashboard** affiche trois indicateurs :

| Carte | Ce qu'elle indique |
| --- | --- |
| **My Hours** | Vos heures restantes sur le total acheté, ainsi que les heures déjà consommées |
| **Lessons Taken** | Le nombre de leçons enregistrées à votre nom |
| **Next Lesson** | La date de votre prochaine leçon à venir, ou `None scheduled` si votre planning est vide |

En dessous, le tableau **My Upcoming Lessons** liste vos leçons avec la date, l'heure, le moniteur et le lieu.

> **À noter** : la carte **Lessons Taken** compte *toutes* vos leçons enregistrées, y compris celles à venir — ce n'est pas un compteur de leçons déjà effectuées.

### Consulter mon planning

Cliquez sur **My Schedule** dans le menu latéral pour afficher la liste complète de vos leçons.

Vous ne pouvez ni créer, ni modifier, ni supprimer une leçon directement : le planning est géré par votre moniteur et par le secrétariat. Pour proposer un créneau, passez par une demande de rendez-vous (voir ci-dessous).

### Acheter des heures de conduite

1. Sur le **Dashboard**, cliquez sur **Buy Hours** dans la carte **My Hours**.
2. Indiquez le **nombre d'heures** souhaité dans le champ `Number of hours`. Le prix unitaire pratiqué par l'auto-école est rappelé à l'écran.
3. Cliquez sur **Pay with Stripe**. Vous êtes redirigé vers la page de paiement sécurisée Stripe.
4. Réglez par carte bancaire. Une fois le paiement validé, vous revenez sur la page **Payment Successful!**.
5. Cliquez sur **Back to Dashboard** : vos nouvelles heures sont créditées sur votre solde.

Vous pouvez interrompre le paiement à tout moment : le bouton **Cancel** (ou un retour depuis Stripe) vous ramène au formulaire sans qu'aucune heure ne soit facturée.

> **Le crédit des heures est confirmé par Stripe, pas par la page de retour.** Dans de rares cas, quelques secondes s'écoulent entre l'affichage de « Payment Successful! » et la mise à jour de votre solde. Rafraîchissez le tableau de bord ; si le solde n'a toujours pas bougé après quelques minutes, contactez le secrétariat avec votre reçu Stripe.

### Demander un rendez-vous à un moniteur

1. Depuis le **Dashboard**, cliquez sur **My Lesson Requests**.
2. Cliquez sur **New Request**.
3. Renseignez :
   - **Instructor** : le moniteur à qui vous adressez la demande ;
   - **Date** : date et heure souhaitées ;
   - **Location** : le lieu de rendez-vous ;
   - **Duration** : la durée en heures.
4. Validez. Votre demande apparaît dans la liste avec le statut `Pending` (en attente).

### Suivre et répondre aux demandes

La page **My Lesson Requests** liste toutes vos demandes avec leur statut :

| Statut affiché | Signification |
| --- | --- |
| `Pending` | En attente de réponse du moniteur |
| `Counter-proposal received` | Le moniteur a proposé un autre créneau — c'est à vous de répondre |
| `Accepted` | La demande est acceptée : la leçon est créée et vos heures ont été décomptées |
| `Refused` | La demande est refusée définitivement |

Quand un moniteur vous fait une contre-proposition, cliquez sur **Respond** en face de la demande. Trois options s'offrent à vous :

- **Accept** — la leçon est créée immédiatement au créneau proposé et les heures correspondantes sont décomptées de votre solde ;
- **Refuse** — la demande est close définitivement ;
- **Counter-Proposal** — vous modifiez la date, le lieu ou la durée et renvoyez la balle au moniteur.

Ce va-et-vient peut se répéter autant de fois que nécessaire : à chaque contre-proposition, c'est à l'autre partie de répondre. La négociation ne s'arrête qu'avec une acceptation ou un refus.

> **Vous ne pouvez pas répondre à votre propre proposition.** Tant que le moniteur n'a pas réagi, le bouton **Respond** n'apparaît pas — c'est normal.

---

## Guide du moniteur (Instructor)

Menu latéral disponible : **Dashboard**, **Schedule**.

### Consulter mon activité

Le **Dashboard** regroupe :

- le nombre de vos élèves,
- vos leçons du jour,
- votre volume horaire total,
- le tableau de vos leçons, avec les actions **Edit** et **Delete** sur chaque ligne.

### Gérer mon planning

**Schedule** affiche l'intégralité de vos leçons. Vous n'y voyez que les vôtres : les leçons des autres moniteurs vous sont invisibles.

**Créer une leçon** — cliquez sur le bouton d'ajout depuis le tableau du **Dashboard**, puis renseignez l'élève, la date et l'heure, le lieu et la durée. Vous n'avez pas à vous désigner comme moniteur : vous êtes automatiquement affecté à la leçon que vous créez.

**Modifier une leçon** — cliquez sur **Edit**. Vous pouvez changer l'élève, la date, le lieu et la durée.

**Supprimer une leçon** — cliquez sur **Delete**, puis confirmez. Les heures correspondantes sont automatiquement **restituées** à l'élève.

> Vous ne pouvez modifier ou supprimer que vos propres leçons.

### Consulter la fiche d'un élève

Depuis le **Dashboard**, ouvrez la fiche d'un élève pour consulter ses forfaits, son historique de leçons et son solde d'heures (total, utilisées, restantes).

> Vous n'avez accès qu'aux fiches des élèves avec lesquels vous avez au moins une leçon programmée. Toute autre fiche vous renvoie à votre tableau de bord.

### Traiter les demandes de rendez-vous

1. Depuis le **Dashboard**, ouvrez la page des demandes (**Lesson Requests**).
2. Pour une demande en attente, cliquez sur **Respond**.
3. Choisissez :
   - **Accept** — la leçon est créée immédiatement et les heures sont décomptées du solde de l'élève ;
   - **Refuse** — la demande est close ;
   - **Counter-Proposal** — vous ajustez la date, le lieu ou la durée, et la demande repart chez l'élève.

> **Si l'élève n'a pas assez d'heures**, l'acceptation échoue et un message d'erreur s'affiche. Vous pouvez alors faire une contre-proposition d'une durée plus courte, ou inviter l'élève à recharger son forfait avant de réessayer.

---

## Guide de la secrétaire (Secretary)

Menu latéral disponible : **Dashboard**, **General Planning**, **People**.

### Tableau de bord

Le **Dashboard** présente le nombre d'élèves, de moniteurs et de leçons, ainsi qu'un compteur d'élèves **sans heures restantes** — utile pour repérer qui relancer. Des raccourcis permettent de créer directement un élève, un moniteur, une leçon ou un forfait.

### Gérer les comptes (People)

La page **People** liste les élèves (avec leurs heures restantes) et les moniteurs.

**Créer un compte** — cliquez sur **Add Student** ou **Add Instructor**, puis renseignez le nom d'utilisateur, le prénom, le nom, l'e-mail et le mot de passe initial. Le rôle est pré-rempli selon le bouton utilisé.

**Modifier un compte** — cliquez sur **Edit**. Pour conserver le mot de passe existant, **laissez le champ mot de passe vide** ; le renseigner le remplace.

**Consulter une fiche élève** — cliquez sur **View** pour voir les forfaits, les leçons et le détail du solde d'heures.

**Supprimer un compte** — cliquez sur **Delete**, puis confirmez.

> ⚠️ **La suppression d'un élève est définitive et supprime en cascade ses forfaits et ses leçons.** Les heures achetées ne sont pas remboursées automatiquement. Vérifiez la fiche de l'élève avant de confirmer.

En tant que secrétaire, vous ne pouvez créer que des comptes **Student** et **Instructor**. La gestion des comptes secrétaires relève de l'administrateur.

### Créditer des heures à un élève

1. Sur **People**, cliquez sur **Add Hours** en face de l'élève concerné.
2. L'élève est déjà pré-sélectionné dans le formulaire. Saisissez le nombre d'heures du forfait.
3. Validez : le forfait est immédiatement disponible.

C'est la marche à suivre pour un règlement effectué au guichet (espèces, chèque, virement). Les paiements par carte effectués en ligne par l'élève créent automatiquement leur forfait, sans intervention de votre part.

Un élève peut cumuler plusieurs forfaits : ils s'additionnent et sont consommés dans leur ordre de création.

### Gérer le planning général

**General Planning** affiche toutes les leçons de l'auto-école, avec deux filtres : par **moniteur** ou par **élève**.

Vous pouvez créer, modifier et supprimer n'importe quelle leçon, pour n'importe quel binôme élève/moniteur. À la création, vous désignez explicitement l'élève **et** le moniteur.

Les règles de gestion des heures s'appliquent automatiquement : décompte à la création, restitution à la suppression, ajustement à la modification, et blocage si le solde est insuffisant.

---

## Guide de l'administrateur (Admin)

Menu latéral disponible : **Dashboard**, **General Planning**, **People**.

L'administrateur dispose de **toutes les capacités de la secrétaire**, décrites ci-dessus : gestion des élèves et moniteurs, forfaits, leçons et planning général.

Deux différences :

1. **Gestion des secrétaires** — le bouton **Add Secretary** est disponible sur les pages **Dashboard** et **People**, et la liste des secrétaires apparaît avec les actions **Edit** et **Delete**. Un administrateur peut donc créer, modifier et supprimer des comptes secrétaires ; une secrétaire ne le peut pas.
2. **Aucune restriction de rôle** — lors de la création ou de la modification d'un compte, le choix du rôle n'est pas limité.

### Modifier le tarif horaire

Le prix de l'heure appliqué lors des achats en ligne se configure dans l'interface d'administration Django (`/admin/`), section **School Settings**. Le tarif par défaut est de 20,00 €.

Cette modification s'applique aux **achats suivants** : elle ne modifie ni les forfaits déjà crédités, ni les paiements déjà effectués.

---

## Comprendre le solde d'heures

C'est le mécanisme central de l'application. En résumé :

| Événement | Effet sur le solde de l'élève |
| --- | --- |
| Achat en ligne (Stripe) | **+** heures payées, créditées automatiquement |
| Forfait ajouté par le secrétariat (**Add Hours**) | **+** heures saisies, immédiatement |
| Création d'une leçon | **−** la durée de la leçon |
| Allongement d'une leçon existante | **−** la différence de durée |
| Raccourcissement d'une leçon | **+** la différence de durée |
| Suppression d'une leçon | **+** la durée de la leçon, restituée intégralement |
| Acceptation d'une demande de RDV | **−** la durée convenue (une leçon est créée) |

**Règle de blocage** : une leçon ne peut pas être créée — ni allongée — si le solde de l'élève est insuffisant. Le message `L'étudiant n'a pas assez d'heures disponibles.` s'affiche et rien n'est enregistré.

**Cumul des forfaits** : les heures de plusieurs forfaits s'additionnent en un solde unique. La consommation se fait forfait par forfait, du plus ancien au plus récent.

---

## Problèmes courants

**Je ne peux pas me connecter.**
Vérifiez le nom d'utilisateur (et non l'e-mail) et le mot de passe. Il n'y a pas de réinitialisation en autonomie : contactez le secrétariat, qui peut définir un nouveau mot de passe depuis la page **People** → **Edit**.

**J'ai payé mais mes heures n'apparaissent pas.**
Le crédit est déclenché par la confirmation de Stripe, qui peut arriver avec quelques secondes de décalage sur l'affichage de la page de succès. Rafraîchissez le tableau de bord. Si le solde n'est toujours pas à jour après quelques minutes, contactez le secrétariat avec votre reçu Stripe : un forfait peut être crédité manuellement.

**Le moniteur ne peut pas accepter ma demande de rendez-vous.**
Votre solde d'heures est probablement insuffisant pour la durée demandée. Achetez des heures via **Buy Hours**, ou convenez d'une leçon plus courte via une contre-proposition.

**Le bouton « Respond » n'apparaît pas sur ma demande.**
C'est que la balle est dans l'autre camp : vous êtes l'auteur de la dernière proposition. Le bouton réapparaîtra si l'autre partie vous fait une contre-proposition. Il disparaît définitivement une fois la demande acceptée ou refusée.

**J'ai supprimé une leçon par erreur.**
Les heures ont été restituées à l'élève : son solde est intact. Recréez simplement la leçon au bon créneau — les heures seront décomptées à nouveau.

**Une page me renvoie systématiquement à mon tableau de bord.**
Elle est réservée à un autre rôle. Chaque rôle n'a accès qu'à ses propres écrans.

**Un élève supprimé par erreur.**
La suppression est définitive : le compte, ses forfaits et ses leçons sont perdus. Il faut recréer le compte et recréditer les heures manuellement via **Add Hours**.
