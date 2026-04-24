------------------------------------------------------------------------------------------------------
ATELIER API-DRIVEN INFRASTRUCTURE
------------------------------------------------------------------------------------------------------
L’idée en 30 secondes : **Orchestration de services AWS via API Gateway et Lambda dans un environnement émulé**.  
Cet atelier propose de concevoir une architecture **API-driven** dans laquelle une requête HTTP déclenche, via **API Gateway** et une **fonction Lambda**, des actions d’infrastructure sur des **instances EC2**, le tout dans un **environnement AWS simulé avec LocalStack** et exécuté dans **GitHub Codespaces**. L’objectif est de comprendre comment des services cloud serverless peuvent piloter dynamiquement des ressources d’infrastructure, indépendamment de toute console graphique.Cet atelier propose de concevoir une architecture API-driven dans laquelle une requête HTTP déclenche, via API Gateway et une fonction Lambda, des actions d’infrastructure sur des instances EC2, le tout dans un environnement AWS simulé avec LocalStack et exécuté dans GitHub Codespaces. L’objectif est de comprendre comment des services cloud serverless peuvent piloter dynamiquement des ressources d’infrastructure, indépendamment de toute console graphique.
  
-------------------------------------------------------------------------------------------------------
Séquence 1 : Codespace de Github
-------------------------------------------------------------------------------------------------------
Objectif : Création d'un Codespace Github  
Difficulté : Très facile (~5 minutes)
-------------------------------------------------------------------------------------------------------
RDV sur Codespace de Github : <a href="https://github.com/features/codespaces" target="_blank">Codespace</a> **(click droit ouvrir dans un nouvel onglet)** puis créer un nouveau Codespace qui sera connecté à votre Repository API-Driven.
  
---------------------------------------------------
Séquence 2 : Création de l'environnement AWS (LocalStack)
---------------------------------------------------
Objectif : Créer l'environnement AWS simulé avec LocalStack  
Difficulté : Simple (~5 minutes)
---------------------------------------------------

Dans le terminal du Codespace copier/coller les codes ci-dessous etape par étape :  

**Installation de l'émulateur LocalStack**  
```
sudo -i mkdir rep_localstack
```
```
sudo -i python3 -m venv ./rep_localstack
```
```
sudo -i pip install --upgrade pip && python3 -m pip install localstack && export S3_SKIP_SIGNATURE_VALIDATION=0
```
```
localstack start -d
```
**vérification des services disponibles**  
```
localstack status services
```
**Réccupération de l'API AWS Localstack** 
Votre environnement AWS (LocalStack) est prêt. Pour obtenir votre AWS_ENDPOINT cliquez sur l'onglet **[PORTS]** dans votre Codespace et rendez public votre port **4566** (Visibilité du port).
Réccupérer l'URL de ce port dans votre navigateur qui sera votre ENDPOINT AWS (c'est à dire votre environnement AWS).
Conservez bien cette URL car vous en aurez besoin par la suite.  

Pour information : IL n'y a rien dans votre navigateur et c'est normal car il s'agit d'une API AWS (Pas un développement Web type UX).

---------------------------------------------------
Séquence 3 : Exercice
---------------------------------------------------
Objectif : Piloter une instance EC2 via API Gateway
Difficulté : Moyen/Difficile (~2h)
---------------------------------------------------  
Votre mission (si vous l'acceptez) : Concevoir une architecture **API-driven** dans laquelle une requête HTTP déclenche, via **API Gateway** et une **fonction Lambda**, lancera ou stopera une **instance EC2** déposée dans **environnement AWS simulé avec LocalStack** et qui sera exécuté dans **GitHub Codespaces**. [Option] Remplacez l'instance EC2 par l'arrêt ou le lancement d'un Docker.  

**Architecture cible :** Ci-dessous, l'architecture cible souhaitée.   
  
![Screenshot Actions](API_Driven.png)   
  
---------------------------------------------------  
## Processus de travail (résumé)

1. Installation de l'environnement Localstack (Séquence 2)
2. Création de l'instance EC2
3. Création des API (+ fonction Lambda)
4. Ouverture des ports et vérification du fonctionnement
-----------------------------------------------------
🚀 Orchestration EC2 via API Gateway & Lambda (LocalStack)
Ce projet démontre la mise en place d'une architecture Serverless sur AWS (émulé par LocalStack) permettant de piloter une infrastructure cloud (démarrage/arrêt d'une instance EC2) via des requêtes HTTP.

🏗️ Architecture du projet
L'architecture repose sur trois composants clés :

Amazon EC2 : L'instance cible que nous souhaitons piloter.

AWS Lambda : Le "cerveau" contenant la logique Python (via boto3) pour agir sur EC2.

API Gateway / Function URL : Le point d'entrée HTTP public qui permet d'invoquer la Lambda depuis un navigateur ou un terminal.

🛠️ Guide d'utilisation
1. Pré-requis
Un environnement GitHub Codespaces.

LocalStack installé et démarré avec un AUTH_TOKEN valide.

L'outil awslocal installé (pip install awscli-local).

2. Initialisation de l'infrastructure
Tout d'abord, nous créons l'instance EC2 qui sera contrôlée :

Bash
awslocal ec2 run-instances --image-id ami-0907535bcb3aed0b6 --count 1 --instance-type t2.micro
Note : Notez l'ID de l'instance généré (ex: i-99451ae8ec9ccba8a).

3. Déploiement de la logique (Lambda)
Le code se trouve dans lambda_function.py. Pour le déployer :

Bash
# Compression du code
zip function.zip lambda_function.py

# Création de la fonction
awslocal lambda create-function \
    --function-name MonPiloteEC2 \
    --runtime python3.9 \
    --zip-file fileb://function.zip \
    --handler lambda_function.lambda_handler \
    --role arn:aws:iam::000000000000:role/lambda-role
4. Exposition de l'API
Pour rendre la fonction accessible via Internet, nous activons une Function URL et ouvrons les ports :

Générer l'URL : awslocal lambda create-function-url-config --function-name MonPiloteEC2 --auth-type NONE

Dans l'onglet PORTS de VS Code, passer le port 4566 en Public.

🚦 Tests et Vérification
Démarrer l'instance
Utilisez la commande curl suivante (en adaptant l'URL de votre Codespace) :

Bash
curl -X POST "https://jubilant-space-garbanzo-5wg5rpvxg972v7x6-4566.app.github.dev/2021-11-07/functions/MonPiloteEC2/invocations?action=status" \
     -d '{"queryStringParameters": {"action": "start"}}'
Vérifier l'état
Pour confirmer que l'ordre a été exécuté, vérifiez le statut réel de l'instance :

Bash
awslocal ec2 describe-instances --instance-ids i-99451ae8ec9ccba8a --query 'Reservations[0].Instances[0].State.Name'
Résultat attendu : "running"

📝 Processus de travail
Pendant ce TP, j'ai dû résoudre des problématiques de routage réseau liées au tunnel sécurisé de GitHub Codespaces. L'utilisation des en-têtes (Headers) et des ports publics a été essentielle pour permettre la communication entre mon navigateur et l'émulateur LocalStack Pro.
---------------------------------------------------
Séquence 4 : Documentation  
Difficulté : Facile (~30 minutes)
---------------------------------------------------
**Complétez et documentez ce fichier README.md** pour nous expliquer comment utiliser votre solution.  
Faites preuve de pédagogie et soyez clair dans vos expliquations et processus de travail.  
   
---------------------------------------------------
Evaluation
---------------------------------------------------
Cet atelier, **noté sur 20 points**, est évalué sur la base du barème suivant :  
- Repository exécutable sans erreur majeure (4 points)
- Fonctionnement conforme au scénario annoncé (4 points)
- Degré d'automatisation du projet (utilisation de Makefile ? script ? ...) (4 points)
- Qualité du Readme (lisibilité, erreur, ...) (4 points)
- Processus travail (quantité de commits, cohérence globale, interventions externes, ...) (4 points) 
