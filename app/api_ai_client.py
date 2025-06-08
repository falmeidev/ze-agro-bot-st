# import the libraries
import streamlit as st
import openai
#from app.config import Config
import re
#from assistant.config import Config
import time

# getting the assistant secret key
ASSISTANT_ID = st.secrets["open_ai_credentials"]["openai_assistant_id"]

# getting the secret key
API_KEY = st.secrets["open_ai_credentials"]["openai_api_key"]

# creating the key
openai.api_key = API_KEY

# create the class
class ChatGptApiClient:

    @staticmethod 
    def zeagro_answer(message_from_user):
        # create the thread
        thread = openai.beta.threads.create()

        # send the message from the user
        message = openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message_from_user
        )

        # initialize the response processing
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # wait the answer (unitil the response generation is finished)
        while True:
            # get the run status
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            # if the run status is "completed", stop the waiting
            if run_status.status == "completed":
                break
            time.sleep(1)

        # get the answer
        messages = openai.beta.threads.messages.list(thread_id=thread.id)

        for msg in reversed(messages.data):
            print(msg)
            print(msg.role + ": " + msg.content[0].text.value)
            # get only the answer from assitant
            if msg.role == "assistant":
                answer = msg.content[0].text.value

            # Verifica se há citações
            annotations = msg.content[0].text.annotations if hasattr(msg.content[0].text, 'annotations') else []
            references = []
            ref_links = {'file-F1MUHkbVo5uAcJtAubzhCy': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1124393/citros-o-produtor-pergunta-a-embrapa-responde (Citrus)', #citrus
                         'file-P2euDZHG7RR3cVFfDEWXjJ': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1118408/soja-o-produtor-pergunta-a-embrapa-responde (Soja)', #soja
                         'file-HiTeaLvJNaQwvR7xt7SCkh': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1015482/sorgo-o-produtor-pergunta-a-embrapa-responde (Sorgo)', #sorgo
                         'file-Y2tzFLU1c2ivvkGCKNS8hM': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1124520/producao-organica-de-hortalicas-o-produtor-pergunta-a-embrapa-responde (Produção Orgânica de Hortaliças)', #prod_org_hort 
                         'file-75yWbAMum1JKxGht12GmZR': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1124380/banana-o-produtor-pergunta-a-embrapa-responde (Banana)', #banana
                         'file-MYaPEFDTu8jvXvqYoc46XC': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1124374/abacaxi-o-produtor-pergunta-a-embrapa-responde (Abacaxi)', #abacaxi
                         'file-NKs2fKL253rWbHFuJKAHqc': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1108718/coco-o-produtor-pergunta-a-embrapa-responde (Coco)', #coco
                         'file-6YZtECjt7BhqERmvVQmZ3a': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1124404/feijao-o-produtor-pergunta-a-embrapa-responde (Feijão)', #feijao
                         'file-KAweYLj7hkgAZys2MJbDhv': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/1124497/manga-o-produtor-pergunta-a-embrapa-responde (Manga)', #manga
                         'file-Ps7rQpeUaCXTG6G5uoEQtd': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/921546/pos-colheita-de-hortalicas-o-produtor-pergunta-a-embrapa-responde (Pós Colheita de Hortaliças)', #pos_colheira_hort
                         'file-LyHdhrQRxE9aTi2yRiorAj': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000038 (Feijão Caupi)', #feijao_caupi
                         'file-Pm9Xqwet2X51BZeCEgWGXo': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000003 (Uva)', #uva
                         'file-8ZzMgVgPge8eMw7ySvByCN': 'https://mais500p500r.sct.embrapa.br/view/publicacao.php?publicacaoid=90000029 (Suínos)', #suinos
                         'file-LgCG5wEkaffcvPnPzNyqqQ': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000027 (Plantio Direto)', #plantio_direto
                         'file-K2ByMXpmawR3HeyYysGDSm': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000007 (Pesca e Piscicultura)', #pesca_e_piscicultura
                         'file-RTCn6AEAj6g9SeeuYw7qfM': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000011 (Pequenas Frutas)', #pequenas_frutas
                         'file-HtLSy6q2CwrRHLJvBk4agt': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000013 (Ovinos)', #ovinos
                         'file-RStjKz5A88Dfsj73ZCUVwr': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000036 (Maracujá)', #maracuja
                         'file-KSWt9bvmggnYZNjKsQRJPA': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000012 (Mandioca)', #mandioca
                         'file-Gxd71ou67NhdBNkg7dZeiR': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000014 (Mamona)', #mamona
                         'file-5k94HBH6YimNR3x5RPoZiU': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000024 (Mamão)', #mamao
                         'file-FhdL6spGg9NhCEGEaQHAGv': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000006 (Hortas)', #hortas
                         'file-EgqsR4eo3op9AKhZbkwj43': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000028 (Geotecnologias e Geoinformação)', #geotecnologias_geoinformação
                         'file-FZ7kwqHRpSNLCigmaPzxvj': 'https://www.embrapa.br/busca-de-publicacoes/-/publicacao/920741/gado-de-corte-o-produtor-pergunta-a-embrapa-responde (Gado de Corte)', #gado_corte
                         'file-LvA6MLDLM4AADet9hWE8bc': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000026 (Bufalos)', #bufalos
                         'file-TjJwHUBkzQwPVfEwrTbLSN': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000008 (Fruticultura Irrigada)', #fruticultura_irrigada
                         'file-AQejvUVbjkaNgivhNkGp2B': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000037 (Caprinos e Ovinos de Corte)', #caprinos_ovinos_corte
                         'file-K2JV2iytJ9hwDTKU3ay7Hs': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000031 (Caju)', #caju
                         'file-81zcr7TYD7DWLJmahqwzdt': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000010 (Gado de Leite)', #gado_leite
                         'file-JmxEjax8nTyvfsvvpUnvNR': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000023 (Arroz)', #arroz
                         'file-G5ZFeVfZ4KhQyq92uctoAc': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000005 (Gergelim)', #gergelim
                         'file-TwsWjDWcFGj6Dbh8TaGuY6': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000018 (Gado de Corte no Pantanal)', #gado_corte_pantanal
                         'file-AmG9Fy1qi5apqnaT27NHRW': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000020 (Maçã)', #maca
                         'file-9QxYEjt8jMewksJ5xT1N2f': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000033 (Integração Lavoura, Pecuária e Floresta)', #integracao_lavoura_pecuaria_floresta
                         'file-TdvfibWKb1eBnZdrsXXTdC': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000004 (Amendoim)', #amendoim
                         'file-HKwcaia2gtsn7JveUWp1Xp': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000001 (Algodão)', #algodao
                         'file-XYTEbLMLZKCnTN28poGu7r': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000034 (Trigo)', #trigo
                         'file-XwQZhdseb3oRTPBPDfm4qz': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000040 (Pêssego, Nectarina e Ameixa)', #pessego_nectarina_ameixa
                         'file-AtRP1upBPonCT8awYWumsg': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000035 (Pera)', #pera
                         'file-EnFcRX7TvyEJZMcW2Kz4rM': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000042 (Recursos Genéticos)', #genetica
                         'file-A4jJivyDUcpJ2DLcG4qyzu': 'https://mais500p500r.sct.embrapa.br/view/arquivoPDF.php?publicacaoid=90000022 (Milho)'  #milho
                         }
            answer_links = []

            for annotation in annotations:
                if annotation.type == 'file_citation':
                    file_id = annotation.file_citation.file_id
                    #quote = annotation.file_citation.quote
                    if file_id not in references:
                        references.append(file_id)
            print(references)
        for i in references:
            print(f"valor de i = {i}")
            print(ref_links[i])
            try:
                answer_links.append(ref_links[i])
            except:
                None
        print(answer_links)
        if len(answer_links) == 1:
            text_ref = "Referência:"
        else:
            text_ref = "Referências:"
        answer = answer + f"\n\n{text_ref} \n\n" + " \n\n ".join(answer_links)

        cleaned_answer = re.sub(r'【\d+:\d+†source】', '', answer)
   
        return cleaned_answer

        