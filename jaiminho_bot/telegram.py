import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app as app
)

import requests
from requests import Session

bp = Blueprint('telegram', __name__, url_prefix='/telegram')

@bp.route('/enel', methods=['GET'])
def enel_invoice():
    # invoices = get_invoices(cpf=app.config['CPF'], instalacao=app.config['INSTALACAO'])
    invoices = get_invoices(cpf=request.args.get('cpf'), instalacao=request.args.get('instalacao'))
    return json.dumps(list(invoices))

# TODO improve pretty print
def get_invoices_pretty_print(**user_credentials):
    invoices = get_invoices(**user_credentials)
    template = render_template('telegram/invoice_enel.txt', **user_credentials)
    return list(map(template.render, invoices))

def get_invoices(**user_credentials):
    """`user_credentials` is a dict containing `cpf` and `instalacao` keys""" 
    url = 'https://portalhome.eneldistribuicaosp.com.br'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    login_payload = render_template('telegram/payload_enel.json', **user_credentials)

    session = Session()
    session.headers.update({'user-agent': user_agent})
    login = session.post(url + '/api/sap/getloginv2', json=json.loads(login_payload))
    session.headers.update({'Authorization': login.headers['Authorization']})

    portalinfo_payload = json.loads('{"I_CANAL":"ZINT","I_COD_SERV":"TC","I_SSO_GUID":""}')
    portalinfo = session.post(url + '/api/sap/portalinfo', json=portalinfo_payload)
    invoices = json.loads(portalinfo.text).get('ET_CONTAS')
    open_invoices = filter(lambda invoice: 'Pendente' in invoice['SITUACAO'], invoices)

    return map(format_invoice, open_invoices)

def format_invoice(invoice):
    due_date = datetime.strptime(invoice['VENCIMENTO'], '%Y%m%d').strftime('%d/%m/%Y')
    invoice_value = str(invoice['MONTANTE']).replace('.',',')
    currency_value = "R$ {}".format(invoice_value)
    return {
        'due_date': due_date,
        'value': currency_value,
        'barcode': invoice['O_COD_BARRAS']
    }

