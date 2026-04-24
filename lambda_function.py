import boto3
import json

def lambda_handler(event, context):
    # Ton instance spécifique
    INSTANCE_ID = "i-99451ae8ec9ccba8a"
    
    # On récupère l'action dans l'URL (ex: ?action=start)
    query_params = event.get('queryStringParameters') or {}
    action = query_params.get('action')

    # Connexion au service EC2
    ec2 = boto3.client('ec2', region_name='us-east-1')

    try:
        if action == 'start':
            ec2.start_instances(InstanceIds=[INSTANCE_ID])
            msg = f"Succès : L'instance {INSTANCE_ID} démarre."
        elif action == 'stop':
            ec2.stop_instances(InstanceIds=[INSTANCE_ID])
            msg = f"Succès : L'instance {INSTANCE_ID} s'arrête."
        else:
            msg = "Erreur : Paramètre 'action' manquant ou invalide (utilisez start ou stop)."
            return {"statusCode": 400, "body": json.dumps(msg)}

        return {"statusCode": 200, "body": json.dumps(msg)}
    
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}