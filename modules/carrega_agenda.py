import datetime
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PLANILHA_AGENDA = BASE_DIR / 'agenda.xlsx'


def normalizar_data(valor):
    texto = str(valor).strip()
    if not texto or texto.lower() in ('nan', 'none'):
        return datetime.date.today()

    try:
        return pd.to_datetime(texto, errors='coerce').date()
    except Exception:
        pass

    try:
        return datetime.datetime.strptime(texto.split(' ')[0], '%Y-%m-%d').date()
    except Exception:
        pass

    try:
        return datetime.datetime.strptime(texto, '%d/%m/%Y').date()
    except Exception:
        return datetime.date.today()


def normalizar_hora(valor):
    texto = str(valor).strip().lower()
    if not texto or texto in ('nan', 'none'):
        return '09:00:00'

    numeros = {
        'zero': 0, 'um': 1, 'uma': 1, 'dois': 2, 'duas': 2, 'três': 3, 'tres': 3,
        'quatro': 4, 'cinco': 5, 'seis': 6, 'sete': 7, 'oito': 8, 'nove': 9,
        'dez': 10, 'onze': 11, 'doze': 12, 'treze': 13, 'quatorze': 14,
        'quinze': 15, 'dezesseis': 16, 'dezessete': 17, 'dezoito': 18, 'dezenove': 19,
        'vinte': 20, 'trinta': 30, 'quarenta': 40, 'cinquenta': 50,
    }

    texto = texto.replace('hora', '').replace('horas', '').replace('h', ':').replace('da tarde', '').replace('da manhã', '').replace('da noite', '')
    texto = texto.replace(' e ', ' ').strip()

    if ' ' in texto and all(p in numeros for p in texto.split() if p not in ('e', '')):
        partes = texto.split()
        if len(partes) == 2 and partes[0] in numeros and partes[1] in numeros:
            horas = numeros[partes[0]]
            minutos = numeros[partes[1]]
            return f'{horas:02d}:{minutos:02d}:00'

    try:
        hora_obj = datetime.datetime.strptime(texto, '%H:%M:%S').time()
        return hora_obj.strftime('%H:%M:%S')
    except ValueError:
        pass

    try:
        hora_obj = datetime.datetime.strptime(texto, '%H:%M').time()
        return hora_obj.strftime('%H:%M:%S')
    except ValueError:
        return '09:00:00'


def garantir_arquivo_agenda():
    if not PLANILHA_AGENDA.exists():
        pd.DataFrame(columns=['data', 'hora', 'descricao', 'responsavel']).to_excel(
            PLANILHA_AGENDA,
            index=False,
        )
    return PLANILHA_AGENDA


def adicionar_compromisso(descricao, responsavel, data, hora):
    try:
        garantir_arquivo_agenda()
        agenda = pd.read_excel(PLANILHA_AGENDA, dtype={'data': 'string', 'hora': 'string', 'descricao': 'string', 'responsavel': 'string'})

        descricao = (descricao or 'Compromisso').strip() or 'Compromisso'
        responsavel = (responsavel or 'Você').strip() or 'Você'
        data_normalizada = normalizar_data(data).isoformat()
        hora_normalizada = normalizar_hora(hora)

        nova_linha = pd.DataFrame([
            {
                'data': data_normalizada,
                'hora': hora_normalizada,
                'descricao': descricao,
                'responsavel': responsavel,
            }
        ])
        agenda = pd.concat([agenda, nova_linha], ignore_index=True)
        agenda.to_excel(PLANILHA_AGENDA, index=False)
        return True
    except Exception as exc:
        print(f'[INFO] Não foi possível salvar o compromisso: {exc}')
        return False


def carrega_agenda():
    if not PLANILHA_AGENDA.exists():
        print(f'[INFO] Arquivo de agenda não encontrado: {PLANILHA_AGENDA}. Criando um novo arquivo...')
        try:
            garantir_arquivo_agenda()
            print(f'[INFO] Arquivo criado com sucesso em: {PLANILHA_AGENDA}')
        except Exception as exc:
            print(f'[INFO] Não foi possível criar a agenda: {exc}')
            return False

    try:
        agenda = pd.read_excel(PLANILHA_AGENDA, dtype={'data': 'string', 'hora': 'string', 'descricao': 'string', 'responsavel': 'string'})
    except Exception as exc:
        print(f'[INFO] Não foi possível ler a agenda: {exc}')
        return False

    hora_atual = datetime.datetime.now().hour
    data_atual = datetime.date.today()
    descricao, responsavel, hora_agenda = [], [], []

    for _, row in agenda.iterrows():
        data = normalizar_data(row['data'])
        hora_texto = normalizar_hora(row['hora'])
        try:
            hora = datetime.datetime.strptime(hora_texto, '%H:%M:%S').time().hour
        except Exception:
            continue

        if data_atual == data and hora >= hora_atual:
            descricao.append(str(row['descricao']))
            responsavel.append(str(row['responsavel']))
            hora_agenda.append(str(row['hora']))

    if descricao:
        return descricao, responsavel, hora_agenda
    return False




















