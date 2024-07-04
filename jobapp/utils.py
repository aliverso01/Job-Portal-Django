import requests

def get_efipay_token():
    # Implementar a lógica para obter o token de autenticação do EFIPay
    pass

def create_split_payment(amount, recipient_list):
    token = get_efipay_token()
    url = 'https://api.efipay.com.br/v1/payments/split'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    payload = {
        'amount': amount,
        'recipients': recipient_list,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
