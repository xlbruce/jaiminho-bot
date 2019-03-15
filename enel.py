import json
import locale

from datetime import datetime
from requests import Session
from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja = Environment(
    loader=FileSystemLoader('templates'),
)

def format_invoice(invoice):
    due_date = datetime.strptime(invoice['VENCIMENTO'], '%Y%m%d').strftime('%d/%m/%Y')
    value_str = str(invoice['MONTANTE']).replace('.',',')
    value = "R$ {}".format(value_str)
    return {
        'due_date': due_date,
        'value': value,
        'barcode': invoice['O_COD_BARRAS']
    }

def get_invoices_pretty_print(user_credentials):
    invoices = get_invoices(user_credentials)
    template = jinja.get_template('invoice.txt')
    return map(template.render, invoices)

def get_invoices(user_credentials):
    """`user_credentials` is a dict containing `cpf` and `instalacao` keys""" 
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
    login_payload = jinja.get_template('payload.json').render(user_credentials)

    session = Session()
    session.headers.update({'user-agent': user_agent})
    login = session.post('https://portalhome.eneldistribuicaosp.com.br/api/sap/getloginv2', json=json.loads(login_payload))
    session.headers.update({'Authorization': login.headers['Authorization']})

    portalinfo_payload = json.loads('{"I_CANAL":"ZINT","I_COD_SERV":"TC","I_SSO_GUID":""}')
    portalinfo = session.post('https://portalhome.eneldistribuicaosp.com.br/api/sap/portalinfo', json=portalinfo_payload)
    invoices = json.loads(portalinfo.text).get('ET_CONTAS')
    open_invoices = filter(lambda invoice: 'Pendente' in invoice['SITUACAO'], invoices)

    return map(format_invoice, open_invoices)
