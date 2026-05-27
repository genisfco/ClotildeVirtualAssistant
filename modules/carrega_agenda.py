import datetime
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
PLANILHA_AGENDA = BASE_DIR / 'agenda.xlsx'


def carrega_agenda():
    if not PLANILHA_AGENDA.exists():
        print(f'[INFO] Arquivo de agenda não encontrado: {PLANILHA_AGENDA}')
        return False

    try:
        agenda = pd.read_excel(PLANILHA_AGENDA)
    except Exception as exc:
        print(f'[INFO] Não foi possível ler a agenda: {exc}')
        return False

    hora_atual = datetime.datetime.now().hour
    data_atual = datetime.date.today()
    descricao, responsavel, hora_agenda = [], [], []

    for _, row in agenda.iterrows():
        data = datetime.datetime.date(row['data'])
        hora_completa = datetime.datetime.strptime(str(row['hora']), '%H:%M:%S')
        hora = datetime.datetime.time(hora_completa).hour

        if data_atual == data and hora >= hora_atual:
            descricao.append(row['descricao'])
            responsavel.append(row['responsavel'])
            hora_agenda.append(row['hora'])

    if descricao:
        return descricao, responsavel, hora_agenda
    return False




















