from selenium import webdriver
from random import randrange
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time, re

class WhatsappBot:
    def __init__(self):
        options =  webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', chrome_options=options)
        self.driver.get('https://web.whatsapp.com')
        time.sleep(15)

    def pesquisarNome(self, nome):
        novaConversa = self.driver.find_elements_by_xpath('//div[@class="rAUz7"]')
        novaConversa[1].click()
        participante = self.driver.find_element_by_class_name('_2S1VP')
        participante.send_keys(nome)
        time.sleep(2)
        user = self.driver.find_element_by_xpath('//span[@title="{}"]'.format(nome))
        user.click()
    
    def enviarMensagem(self, mensagem):  
        mensage_caixa = self.driver.find_element_by_xpath('//div[@class="_1Plpp"]')
        mensage_caixa.send_keys(mensagem)

        time.sleep(4)
        try:
            enviar = self.driver.find_element_by_xpath('//button[@class="_35EW6"]')
            enviar.click()
        except NoSuchElementException:
            pass
            

    def enviarGif(self, nomeGif) :
        abaconteudos = self.driver.find_elements_by_xpath('//div[@class="weEq5"]')
        abaconteudos[0].click()
        time.sleep(1)

        abaGif = self.driver.find_element_by_class_name('_1oRJg')
        abaGif.click()
        time.sleep(2)

        campo_pesquisa = self.driver.find_element_by_class_name('_2U5s1')
        campo_pesquisa.send_keys(nomeGif)
        time.sleep(2)
        
        abaGif = self.driver.find_elements_by_xpath('//div[@class="zl5TR"]')
        abaGif[randrange(1, 4)].click()
        time.sleep(8)

        enviar = self.driver.find_element_by_xpath('//div[@class="_3nfoJ"]')
        enviar.click()
        
    
    def obterUltimaMensagem(self):
        # Conteudo mensagem
        #message-in
        mensagens = self.driver.find_elements_by_class_name("_3_7SH")
        ultimaMensagem = len(mensagens) - 1

        try:
            mensagem = mensagens[ultimaMensagem].find_element_by_css_selector('span.selectable-text').text

            # Rementente
            Rementente_mensagem = self.driver.find_elements_by_xpath('//div[@class="copyable-text"]')
            ultimoRemetente = len(Rementente_mensagem) -1 
            
            rementente = Rementente_mensagem[ultimoRemetente].get_attribute('data-pre-plain-text')
            nome = re.findall(r"[a-zA-Z]", rementente)

            return ['success', nome, mensagem] 
        except NoSuchElementException:
            return ['alert', '', 'Infelizmente, não consigo identificar o tipo de mensagem que você me enviou.']

    def abrirAba(self):
        self.driver.execute_script("window.open('https://accounts.google.com/signin/oauth/oauthchooseaccount?state=%7B%22csrf_token%22%3A%20%22628b041b6c99b29d0846867ba5626ce3863a25ae29c72b1c7a3c5a38ac478506%22%2C%20%22return_url%22%3A%20%22https%3A%2F%2Fdialogflow.com%2F%22%7D&redirect_uri=https%3A%2F%2Fdialogflow.com%2Foauth2callback&prompt=select_account&response_type=code&client_id=157101835696-ooapojlodmuabs2do2vuhhnf90bccmoi.apps.googleusercontent.com&scope=openid%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgoogledevelopers%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&access_type=online&o2v=2&as=GtbyJPnOlpf5qDIzhPFf8Q&flowName=GeneralOAuthFlow', '_blank')")
        self.driver.switch_to_window(self.driver.window_handles[1])

    def loginDialogFlow(self):
        email = self.driver.find_element_by_id("identifierId")
        email.send_keys("chatbotdebora@gmail.com")
        botaoLogin = self.driver.find_element_by_id("identifierNext")
        botaoLogin.click()

        time.sleep(10)

        senha = self.driver.find_element_by_name("password")
        senha.send_keys("caneta!1")        
        botaoSenha = self.driver.find_element_by_id("passwordNext")
        botaoSenha.click()

        time.sleep(10)
        self.driver.get("https://dialogflow.cloud.google.com/")
    
    def digitarMensagemDialogFlow(self, mensagem):
        campoMensagem = self.driver.find_element_by_id("test-client-query-input")
        campoMensagem.send_keys(mensagem)
        campoMensagem.send_keys(Keys.ENTER)
    
    def obterRespostaDialogFlow(self):
        respostas = self.driver.find_elements_by_xpath('//span[@class="ng-binding"]')
        respostaDialogFlow = []
        contador = 0

        for resposta in respostas:
            if resposta.text == "input.welcome":
                break
            if resposta.text == "Intents":
                break
            if resposta.text == "input.unknown":
                break
            if contador > 1 :
                respostaDialogFlow.append(resposta.text)
            
            contador = contador + 1

        return respostaDialogFlow

    def mudarAbaWhatssap(self):
         self.driver.switch_to_window(self.driver.window_handles[0])
    
    def mudarAbaDialogFlow(self):
         self.driver.switch_to_window(self.driver.window_handles[1])



if __name__ == "__main__":
    # ABRIR WhatsApp 
    WhatsappBot = WhatsappBot()
    time.sleep(10)
    alunos = ["Felipe Vilella"]
     
    #Abrir dialogFlow
    WhatsappBot.abrirAba()
    WhatsappBot.loginDialogFlow()
    time.sleep(10)

    WhatsappBot.mudarAbaWhatssap()
    time.sleep(3)
    
    while True:

        for aluno in alunos:
            WhatsappBot.pesquisarNome(aluno)
            time.sleep(3)

            mensagem = WhatsappBot.obterUltimaMensagem()

            # Formatar nome aluno em array
            nomeAluno = re.findall(r"[a-zA-Z]", aluno)
            destinatario = True

            mensagem = WhatsappBot.obterUltimaMensagem()

            for letra in nomeAluno :
                if(letra not in mensagem[1]) :
                    destinatario = False

            if(destinatario):

                if mensagem[0] == 'success':
                    mensagem[2] = mensagem[2].lower()
                    # Verificar Quiz
                    quiz = re.findall('#quiz', mensagem[2])
                    # Gerar Relatorio
                    relatorio = re.findall('#gerarRelatorio', mensagem[2])
                    
                    if quiz:
                        mensage[2] = re.split(r'#quiz', mensagem[2])

                    if relatorio:
                        print('aaaa')
                    
                    WhatsappBot.mudarAbaDialogFlow()
                    time.sleep(2)
                    
                    WhatsappBot.digitarMensagemDialogFlow(mensagem[2])
                    time.sleep(2)
                    
                    mensagensRobo = WhatsappBot.obterRespostaDialogFlow()
                    WhatsappBot.mudarAbaWhatssap()
                    time.sleep(2)
 
                    for mensagemRobo in mensagensRobo :  
                        if re.findall('enviar-gif-ok', mensagem[2]):
                            WhatsappBot.enviarGif(mensagemRobo)
                        else:
                            WhatsappBot.enviarMensagem(mensagemRobo)
                        time.sleep(1)
                    
                else:
                    WhatsappBot.enviarMensagem(mensagem[2])

                time.sleep(4)