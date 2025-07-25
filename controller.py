import view as v,time as t,sys

class Controller:
    def __init__(self, model):
        self.model = model
        self.produtos = self.model.listarProdutos()
        self.inicio = None
        self.rodando = False
        self.misto_comidos = 0
        self.mainVeiw = None  

        self.tela1 = None
        self.tela2 = None
        self.tela3 = None
        self.telaJogo = None
        self.telaJogoExtendida = None
        self.tela4 = None
        self.telaADM = None


    def set_main_view(self, main_view):
        self.mainVeiw = main_view

    def set_telas(self, **telas):
        self.tela1 = telas.get('tela1')
        self.tela2 = telas.get('tela2')
        self.tela3 = telas.get('tela3')
        self.telaJogo = telas.get('telaJogo')
        self.telaJogoExtendida = telas.get('telaJogoExtendida')
        self.tela4 = telas.get('tela4')
        self.telaADM = telas.get('telaADM')

        self.gerenciador_telas(2)
        
    def gerenciador_telas(self, id):
        if id == 1:
            self.mostrar_tela(self.tela1)
        elif id == 2:
            self.tela2.setProdutos()
            self.tela2.limparFiltro()
            self.mostrar_tela(self.tela2)
        elif id == 3:
            self.tela3.criarContainerCupons()
            self.mostrar_tela(self.tela3)
        elif id==4:
            self.model.set0_Cliques()
            self.telaJogo.atualizar_imagem()
            self.resetar_cronometro()
            self.mostrar_tela(self.telaJogo)
            self.iniciar_cronometro()
        elif id ==5:
            self.parar_cronometro()
            self.mostrar_tela(self.telaJogoExtendida)
            self.telaJogoExtendida.get_score()
            self.telaJogoExtendida.get_imagemFinal()
            self.telaJogoExtendida.get_fimJogo()
        elif id==6:
            self.tela4.criarContainerCupons()
            self.mostrar_tela(self.tela4)
        elif id==7:
            self.mostrar_tela(self.telaADM)

    def get_Produto(self):
        self.produtos = self.model.listarProdutos()
        return self.produtos

    def filtrarProdutos(self,termoBusca):
        retorno = self.model.filtrarProdutos(termoBusca)
        if retorno:
            self.tela2.exibir_produtos(retorno)
        else:   
            self.tela2.exibir_produtos(self.produtos)

    def mostrar_detalhes(self,produto):
        self.tela2extendida = v.Tela2extendidaView(self.mainVeiw.root, self, produto)
        self.mostrar_tela(self.tela2extendida)

    def mostrar_tela(self, tela):
        self.mainVeiw.mostrarTela(tela)

    def iniciar_cronometro(self):
        if not self.rodando:
            if self.inicio is None:
                self.inicio = t.time()
            self.rodando = True
            self.atualizar_cronometro()

    def atualizar_cronometro(self):

        if self.rodando:
            tempo = t.time() - self.inicio
            if tempo >= 10.0:
                self.gerenciador_telas(5)
                return
            self.telaJogo.atualizar_tempo(tempo)
            self.mainVeiw.root.after(100, self.atualizar_cronometro)

    def parar_cronometro(self):
        if self.rodando:
            self.tempo_final = t.time() - self.inicio
            self.rodando = False

    def get_tempo_final(self):
        tp = self.tempo_final
        return tp

    def resetar_cronometro(self):
        self.rodando = False
        self.inicio = None
        self.telaJogo.atualizar_tempo(0)

    def get_imagem(self):
        imagem,self.misto_comidos =self.model.getImagemJogo()
        self.telaJogo.atualizar_mistoQuentes(self.misto_comidos)
        return imagem

    def get_CaminhoJogo(self):
        caminho = self.get_imagem()
        return caminho
    
    def get_mistoComidos(self):
        misto_comidos = self.misto_comidos
        return misto_comidos

    def atualizar_contador_view(self):
        self.telaJogo.atualizar_contador()

    def incrementar_cliques(self):
        self.model.registrar_clique()
        self.atualizar_contador_view()
    
    def get_resultado(self):
        return self.model.get_resultado()

    def set_criarConta(self,Conta):
        Erro = self.validarEntrada(Conta)
        if Erro:
            return Erro
        return None
    
    def validarEntrada(self,Conta):
        return self.model.validarDados(Conta)
    
    def get_conta(self):
        return self.model.get_Conta()

    def get_cupons(self):
        return self.model.get_userCupons()
    
    def verifConta(self,nome,senha):
        retorno = self.model.verifConta(nome,senha)
        if retorno[0]==0:
            return retorno[1]
        
        elif retorno[0]==1:
            self.logarADM()
            return 1
        else:
            self.logarUser()
            return None
    
    def usarCupom(self,email,cupom):
        retorno = self.model.usarCupom(email,cupom)
        return retorno
    
    def logarUser(self):
        self.gerenciador_telas(2)
    
    def logarADM(self):
        self.gerenciador_telas(7)

    def deletarProduto(self,Produto):
        retorno = self.model.deletarProduto(Produto)
        return retorno
    
    def atualizarProduto(self,Produto):
        retorno = self.model.atualizarProduto(Produto)
        return retorno
    
    def cadastrarProduto(self,Produto):
        retorno = self.model.cadastrarProduto(Produto)
        return retorno
    
    def getImageName(self,caminho):
        imageName = self.model.getImageName(caminho)
        return imageName
    
    def exit(self, evento=None):
        sys.exit()
    


        