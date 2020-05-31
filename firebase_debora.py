import requests
from firebase import firebase

class firebase_debora:
    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://debora-fnjowg.firebaseio.com/', None)
    
    def obterRespostas(self, tabela):
        resultado = self.firebase.get('/debora-fnjowg/'+tabela, '')
        return resultado
    
    def atualizarRespostas(self, key, campo, valor):
        self.firebase.put('/debora-fnjowg/respostas/'+key, campo, valor)
        return 'resposta atualizado com sucesso' 