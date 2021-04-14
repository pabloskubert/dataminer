#!/usr/bin/env python
from pathlib import Path
import sys
import csv
import requests


def main():
    if len(sys.argv) < 3:
        print("Uso: %s [ARQ_CSV] [SALVAR_NOME] [PAROU EM]" % (sys.argv[0]))
        sys.exit(0)

    SALVAR_EM = Path.joinpath(Path.home(), 'RICH_CSV', sys.argv[2]+'.csv')
    INICIAR_EM = int(sys.argv[3])
    if INICIAR_EM != 0:
        INICIAR_EM += 1
    
    TOKEN_ACESSO = pegarToken()
    print("\n\t\t Token pego: %s \n\t\t Iniciar em: %d \n" % (TOKEN_ACESSO, INICIAR_EM))
    def naoEncontrado(s): return s if s != 'None' and s != '' else 'Não encontrado.'  # noqa E731
    with open(sys.argv[1], mode='r') as arquivoCsv:

        linhas = csv.DictReader(arquivoCsv)
        consul_cont = 1
        for linha in linhas:
            INICIAR_EM -= 1
            if INICIAR_EM >= 1:
                continue

            # Coloca na ordem correta
            if "/" in linha['cpf']:
                cp = linha['nasc']
                linha['nasc'] = linha['cpf']
                linha['cpf'] = cp
    
            consultaJson = consultarCPF(linha['cpf'], TOKEN_ACESSO)

            if "result" not in consultaJson or len(consultaJson['result']) < 1:
                print("\n\tSem registro para o cpf %s" % (linha['cpf']))
                continue

            consulPessoa = consultaJson['result'][0]['pessoa']
            cad = consulPessoa['cadastral']
            nome = "%s %s %s" % (
                cad['nomePrimeiro'],
                cad['nomeMeio'],
                cad['nomeUltimo']
            )
            nasc = cad['dataNascimento']
            prof = naoEncontrado(consulPessoa['socioDemografico']['profissao'])
            renda = naoEncontrado(
                consulPessoa['socioDemografico']['rendaPresumida'])
            escol = naoEncontrado(consulPessoa['cadastral']['escolaridade'])
            emails = consulPessoa['contato']['email']
            email = "Não encontrado." if len(emails) == 0 else emails[0]['email']  # noqa

            empregos = consulPessoa['vinculo']['empregador']
            dataAdmissao = 0
            empregoAtual = {'razSocial': '', 'dtAdm': ''}

            # Pega o emprego mais recente
            for emprego in empregos:
                admData = str(emprego['dataAdmissao'])
                dtAdmStr = admData.replace('-', '')
                dtAdmStr = '0' if admData == 'None' else dtAdmStr
                dtAdm = int(dtAdmStr)

                if (dtAdm > dataAdmissao):
                    dataAdmissao = dtAdm
                    empregoAtual['razSocial'] = emprego['razaoSocial']
                    empregoAtual['dtAdm'] = '' if dtAdm == 0 else admData

            # Pega os telefones da lista CSV
            tels = []
            for i in range(1, 4):
                telc = linha['tel'+str(i)]
                if telc:
                    tels.append(telc)

            # Completa a lista com telefones da consulta
            faltam = (9-len(tels))
            telefones = consulPessoa['contato']['telefone']
            telCont = 0
            for tel in telefones:
                if telCont == faltam:
                    break
                tels.append("(%s)%s" % (tel['ddd'], tel['numero']))
                telCont += 1

            # Completa com "Vazio" o resto da celulas de telefone
            restante = (9-len(tels))
            for y in range(0, restante):
                tels.append("Vazio")

            CSV = "\"%s\",\"%s\",\"%s\",%s,%s,\"%s\",%s,%s,\"%s\",\"%s\"" % (
                nome,
                prof,
                empregoAtual['dtAdm'],
                ','.join(tels),
                nasc,
                renda,
                linha['cpf'],
                email,
                empregoAtual['razSocial'],
                escol
            )

            print("\n\t Consulta nº %d: \"%s\",\"%s\",\"%s\"" %
                  (consul_cont, nome, prof, escol))
            consul_cont += 1
            with open(SALVAR_EM, mode='a') as salvarCSV:
                salvarCSV.write(CSV)
                salvarCSV.write('\n')
        
        print("\n\t\t\t Fim. \n")


def pegarToken():
    autenticarD = {
        'grant_type': 'password',
        'client_id': '2',
        'client_secret': '<CHAVE_SECRETA>',
        'username': '<USUÁRIO>',
        'password': '<SENHA>',
        'empresa': '<ID DA EMPRESA>'
    }

    ret_code = 0
    tents = 0
    while ret_code != 200:
        if tents == 4:
            print("\n\t\t Many http code: %s" % (ret_code))
            sys.exit(1)

        tokenRet = requests.post("https://targetdatasmart.com/api/token", json=autenticarD)
        ret_code = tokenRet.status_code
        tents += 1

    tokenObtido = tokenRet.json()
    return tokenObtido['access_token']


def consultarCPF(cpfAlvo, token):
    cabecalho = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token
    }

    HTTP_OK = 200
    CODIGO_RET = 0
    tentivas = 0
    consultarCPF = [cpfAlvo]
    while CODIGO_RET != HTTP_OK:
        if tentivas == 4:
            print("\n\n\t\t Várias tentativas falhas de consultar, código http retornado: %s" % (
                CODIGO_RET))
            sys.exit(1)

        try:
            consulRet = requests.post("https://targetdatasmart.com/api/PF/CPF", headers=cabecalho, json=consultarCPF)
            CODIGO_RET = consulRet.status_code
        except Exception:
            pass

        tentivas += 1

    return consulRet.json()


if __name__ == '__main__':
    main()
