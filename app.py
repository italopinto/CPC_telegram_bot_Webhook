import logging
import sys
import time
import os
import random
import hashlib
from flask import Flask, request

import telebot
from telebot import types

__author__ = "Ítalo Pinto"

# Making an instance for the flask server within the code
server = Flask(__name__)

# The telegram token of the bot
API_TOKEN = '<TOKEN>'

# Calling the class telebot with the log
bot = telebot.TeleBot(API_TOKEN)
telebot.logger.setLevel(logging.DEBUG)

# Metadata of the documents
mime = 'application/pdf'
title = 'CPC '

# List of all documents, name, url and their description
url_doc = [('00', 'http://www.cpc.org.br/Arquivos/Documentos/573_CPC00(R2).pdf', 'Estrutura Conceitual para Relatório Financeiro'), ('01', 'http://www.cpc.org.br/Arquivos/Documentos/27_CPC_01_R1_rev%2012.pdf', 'Redução ao Valor Recuperável de Ativos'), ('02', 'http://www.cpc.org.br/Arquivos/Documentos/62_CPC_02_R2_rev%2013.pdf', 'Efeitos das mudanças nas taxas de câmbio e conversão de demonstrações contábeis'), ('03', 'http://www.cpc.org.br/Arquivos/Documentos/183_CPC_03_R2_rev%2014.pdf', 'Demonstração dos Fluxos de Caixa'), ('04', 'http://www.cpc.org.br/Arquivos/Documentos/187_CPC_04_R1_rev%2014.pdf', 'Ativo Intangível'), ('05', 'http://www.cpc.org.br/Arquivos/Documentos/159_CPC_05_R1_rev%2006.pdf', 'Divulgação sobre Partes Relacionadas'), ('06', 'http://www.cpc.org.br/Arquivos/Documentos/533_CPC_06_R2_rev%2016.pdf', 'Arrendamentos'), ('07', 'http://www.cpc.org.br/Arquivos/Documentos/167_CPC_07_R1_rev%2012.pdf', 'Subvenção e Assistência Governamentais'), ('08', 'http://www.cpc.org.br/Arquivos/Documentos/171_CPC08_R1.pdf', 'Custos de Transação e Prêmios na Emissão de Títulos e Valores Mobiliários'), ('09', 'http://www.cpc.org.br/Arquivos/Documentos/175_CPC_09_rev%2014.pdf', 'Demonstração do Valor Adicionado (DVA)'), ('10', 'http://www.cpc.org.br/Arquivos/Documentos/211_CPC_10_R1_rev%2014.pdf', 'Pagamento Baseado em Ações'), ('11', 'http://www.cpc.org.br/Arquivos/Documentos/215_CPC_11_rev%2014.pdf', 'Contratos de Seguro'), ('12', 'http://www.cpc.org.br/Arquivos/Documentos/219_CPC_12.pdf', 'Ajuste a Valor Presente'), ('13', 'http://www.cpc.org.br/Arquivos/Documentos/223_CPC_13.pdf', 'Adoção Inicial da Lei nº. 11.638/07 e da Medida Provisória nº. 449/08'), ('14', 'http://www.cpc.org.br/Arquivos/Documentos/227_CPC_14.pdf', 'Instrumentos Financeiros: Reconhecimento, Mensuração e Evidenciação (Fase I) - Transformado em OCPC 03'), ('15', 'http://www.cpc.org.br/Arquivos/Documentos/235_CPC_15_R1_rev%2014.pdf', 'Combinação de Negócios'), ('16', 'http://www.cpc.org.br/Arquivos/Documentos/243_CPC_16_R1_rev%2013.pdf', 'Estoques'), ('18', 'http://www.cpc.org.br/Arquivos/Documentos/263_CPC_18_(R2)_rev%2013.pdf', 'Investimento em Coligada, em Controlada e em Empreendimento Controlado em Conjunto'), ('19', 'http://www.cpc.org.br/Arquivos/Documentos/274_CPC_19_%20R2_rev%2013.pdf', 'Negócios em Conjunto'), ('20', 'http://www.cpc.org.br/Arquivos/Documentos/281_CPC_20_R1_rev%2014.pdf', 'Custos de Empréstimos'), ('21', 'http://www.cpc.org.br/Arquivos/Documentos/288_CPC_21_R1_rev%2014.pdf', 'Demonstração Intermediária'), ('22', 'http://www.cpc.org.br/Arquivos/Documentos/292_CPC_22_rev%2008.pdf', 'Informações por Segmento'), ('23', 'http://www.cpc.org.br/Arquivos/Documentos/296_CPC_23_rev%2014.pdf', 'Políticas Contábeis, Mudança de Estimativa e Retificação de Erro'), ('24', 'http://www.cpc.org.br/Arquivos/Documentos/300_CPC_24%20_rev%2012.pdf', 'Evento Subsequente'), ('25', 'http://www.cpc.org.br/Arquivos/Documentos/304_CPC_25_rev%2014.pdf', 'Provisões, Passivos Contingentes e Ativos Contingentes'), ('26', 'http://www.cpc.org.br/Arquivos/Documentos/312_CPC_26_R1_rev%2014.pdf', 'Apresentação das Demonstrações Contábeis'), ('27', 'http://www.cpc.org.br/Arquivos/Documentos/316_CPC_27_rev%2014.pdf', 'Ativo Imobilizado'), ('28', 'http://www.cpc.org.br/Arquivos/Documentos/320_CPC_28_rev%2014.pdf', 'Propriedade para Investimento'), ('29', 'http://www.cpc.org.br/Arquivos/Documentos/324_CPC_29_rev%2014.pdf', 'Ativo Biológico e Produto Agrícola'), ('31', 'http://www.cpc.org.br/Arquivos/Documentos/336_CPC_31_rev%2012.pdf', 'Ativo Não Circulante Mantido para Venda e Operação Descontinuada'), ('32', 'http://www.cpc.org.br/Arquivos/Documentos/340_CPC_32_rev%2014.pdf', 'Tributos sobre o Lucro'), ('33', 'http://www.cpc.org.br/Arquivos/Documentos/350_CPC_33_R1_rev%2013.pdf', 'Benefícios a Empregados'), ('35', 'http://www.cpc.org.br/Arquivos/Documentos/363_CPC_35_R2_rev%2007.pdf', 'Demonstrações Separadas'), ('36', 'http://www.cpc.org.br/Arquivos/Documentos/448_CPC_36_R3_rev%2008.pdf', 'Demonstrações Consolidadas'), ('37', 'http://www.cpc.org.br/Arquivos/Documentos/402_CPC_37_R1_rev%2014.pdf', 'Adoção Inicial das Normas Internacionais de Contabilidade'), ('39', 'http://www.cpc.org.br/Arquivos/Documentos/410_CPC_39_rev%2013.pdf', 'Instrumentos Financeiros: Apresentação'), ('40', 'http://www.cpc.org.br/Arquivos/Documentos/567_CPC_40_R1_rev%2015.pdf', 'Instrumentos Financeiros: Evidenciação'), ('41', 'http://www.cpc.org.br/Arquivos/Documentos/430_CPC_41_rev%2012.pdf', 'Resultado por Ação'), ('42', 'http://www.cpc.org.br/Arquivos/Documentos/558_CPC_42.pdf', 'Contabilidade em Economia Hiperinflacionária'), ('43', 'http://www.cpc.org.br/Arquivos/Documentos/426_CPC43_R1.pdf', 'Adoção Inicial dos Pronunciamentos Técnicos CPCs 15 a 41'), ('44', 'http://www.cpc.org.br/Arquivos/Documentos/437_CPC_44_final_06052013.pdf', 'Demonstrações Combinadas'), ('45', 'http://www.cpc.org.br/Arquivos/Documentos/434_CPC_45_rev%2012.pdf', 'Divulgação de Participações em outras Entidades'), ('46', 'http://www.cpc.org.br/Arquivos/Documentos/395_CPC_46_rev%2014.pdf', 'Mensuração do Valor Justo'), ('47', 'http://www.cpc.org.br/Arquivos/Documentos/527_CPC_47_Rev%2014.pdf', 'Receita de Contrato com Cliente'), ('48', 'http://www.cpc.org.br/Arquivos/Documentos/530_CPC_48_Rev%2015.pdf', 'Instrumentos Financeiros'), ('49', 'http://www.cpc.org.br/Arquivos/Documentos/551_CPC_49_final.pdf', 'Contabilização e Relatório Contábil de Planos de Benefícios de Aposentadoria'), ('PME', 'http://www.cpc.org.br/Arquivos/Documentos/392_CPC_PMEeGlossario_R1_rev%2014.pdf', 'Contabilidade para Pequenas e Médias Empresas com Glossário de Termos')]


# Function to return an unique ID for the default query answer 
def id_shuffle(docid, number=None) -> str:
            if number == None:
                qid: str = hashlib.md5(docid.encode()).hexdigest()
                return qid
            else:
                qid: str = hashlib.md5(docid.encode()).hexdigest() + number
                return qid

# The inline handlers to the users queries
@bot.inline_handler(lambda query: query.query != "")
def query_document(inline_query):
    try:
        for cpc in url_doc:
            if inline_query.query == cpc[0]:
                item = types.InlineQueryResultDocument(id=inline_query.id, title=title + cpc[0], document_url=cpc[1], mime_type=mime, description=cpc[2])
                bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    try:
        doc1 = random.choice(url_doc)
        doc2 = random.choice(url_doc)
        doc3 = random.choice(url_doc)
        doc4 = random.choice(url_doc)
        doc5 = random.choice(url_doc)
        doc6 = random.choice(url_doc)
        doc7 = random.choice(url_doc)
        doc8 = random.choice(url_doc)
        doc9 = random.choice(url_doc)
        doc10 = random.choice(url_doc)
        item1 = types.InlineQueryResultDocument(id=id_shuffle(doc1[0], '1'), title=title + doc1[0], document_url=doc1[1], mime_type=mime, description=doc1[2])
        item2 = types.InlineQueryResultDocument(id=id_shuffle(doc2[0], '2'), title=title + doc2[0], document_url=doc2[1], mime_type=mime, description=doc2[2])
        item3 = types.InlineQueryResultDocument(id=id_shuffle(doc3[0], '3'), title=title + doc3[0], document_url=doc3[1], mime_type=mime, description=doc3[2])
        item4 = types.InlineQueryResultDocument(id=id_shuffle(doc4[0], '4'), title=title + doc4[0], document_url=doc4[1], mime_type=mime, description=doc4[2])
        item5 = types.InlineQueryResultDocument(id=id_shuffle(doc5[0], '5'), title=title + doc5[0], document_url=doc5[1], mime_type=mime, description=doc5[2])
        item6 = types.InlineQueryResultDocument(id=id_shuffle(doc6[0], '6'), title=title + doc6[0], document_url=doc6[1], mime_type=mime, description=doc6[2])
        item7 = types.InlineQueryResultDocument(id=id_shuffle(doc7[0], '7'), title=title + doc7[0], document_url=doc7[1], mime_type=mime, description=doc7[2])
        item8 = types.InlineQueryResultDocument(id=id_shuffle(doc8[0], '8'), title=title + doc8[0], document_url=doc8[1], mime_type=mime, description=doc8[2])
        item9 = types.InlineQueryResultDocument(id=id_shuffle(doc9[0], '9'), title=title + doc9[0], document_url=doc9[1], mime_type=mime, description=doc9[2])
        item10 = types.InlineQueryResultDocument(id=id_shuffle(doc10[0], '10'), title=title + doc10[0], document_url=doc10[1], mime_type=mime, description=doc10[2])
        bot.answer_inline_query(inline_query.id, results=[item1, item2, item3, item4, item5, item6, item7, item8, item9, item10], cache_time=1)
    except Exception as e:
        print(e)


# The flask server decorators
@server.route("/" + API_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-heroku-app.herokuapp.com/' + API_TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
