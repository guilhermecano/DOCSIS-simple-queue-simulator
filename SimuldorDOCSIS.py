import random
import pylab as pl

class Pacote:
    def __init__(self, tArrival, tServiceStart, tService):
        self.tArrival = tArrival
        self.tServiceStart = tServiceStart
        self.tService = tService
        self.tEndOfService = tServiceStart + tService
        self.tDelay = tServiceStart - tArrival

class Queue:
    def __init__(self, maxSize):
        self.items = []
        self.discarted = []
        self.log = []
        self._maxSize = maxSize
        
    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        if self.size() < self._maxSize:
            self.items.insert(0,item)
        else:
            self.discard(item)
        
    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    def discard(self, item):
        self.discarted.append(item)
        
    def discSize(self):
        return len(self.discarted)
    
    def register(self, item):
        self.log.append(item)
    
    def logSize(self):
        return len(self.log)
        
class LeakyBucket(object):
 
    def __init__(self, tokens, fill_rate, time):
        self.capacity = float(tokens)
        self._tokens = float(tokens)
        self.fill_rate = float(fill_rate)
        self.timestamp = time

    def consume(self, tokens, time):
        self.timestamp = time
        if tokens <= self._tokens:
            self._tokens -= tokens
        else:
            return False
        return True

    def get_tokens(self, time):
        now = time
        if self._tokens < self.capacity:
            delta = self.fill_rate * (now - self.timestamp)
            self._tokens = min(self.capacity, self._tokens + delta)
        self.timestamp = now
        return self._tokens

#Funcao  para gerar os intervalos de chegada e tempo de serviço (relacionado com o tamanho do pacote)
def rGen(lmb):
    return random.expovariate(lmb)

def simQueue(n, tSimulacao = False, txDadosLeaky = False,mu = False, k = False, B=False, txNodeMax = False, pkgSize = False):
    if not tSimulacao:
        tSimulacao = 1
    if not txDadosLeaky:
        txDadosLeaky = float(input("Digite a taxa de dados do assinante (Mbps):\n"))
    if not B:
        B = 5 #Quantidade de tokens/limite de buffering
    if not mu:
        mu = float(input("Digite a taxa de serviço da fila (Mbps):\n"))
    if not txNodeMax:
        txNodeMax = 800/n
    if not pkgSize:
        pkgSize = 188
    if not k:
        k = 60 #Valor arbitrario para o tamanho da fila
        
    #Conversão para bits
    txDadosLeaky = txDadosLeaky*1024*1024
    txNodeMax = txNodeMax*1024*1024 #Taxa máxima de transmissão downstream de um nó:
    pkgSize = pkgSize*8
    lmbdLeaky = txDadosLeaky/pkgSize
    mu = (mu*1024*1024)/pkgSize
    #Limite de transferência downstream de um nó.
    lmbdNode = txNodeMax/pkgSize #Taxa de chegada máxima do nó.
    downloaded = []    
    tLog = []
    qsLog = []
    qdLog = []
    qlLog = []
    
    t = 0
    queue = Queue(k)
    leaky = LeakyBucket(B, lmbdLeaky, t)
    
    while t<tSimulacao:
        tLog.append(t)
        qsLog.append(queue.size())
        qdLog.append(queue.discSize())
        qlLog.append(queue.logSize())
        
        if queue.logSize() == 0:
            tArrival = rGen(lmbdNode)
        else:
            tArrival = tArrival + rGen(lmbdNode)
            if queue.size() >0 and tArrival > queue.items[0].tEndOfService:
                downloaded.append(queue.dequeue())
                
        if leaky.consume(1,t):
            if queue.size() == 0:
                tServiceStart = tArrival
            else:
                tServiceStart = max(tArrival, queue.items[0].tEndOfService)
            tService = rGen(mu) 
            queue.enqueue(Pacote(tArrival, tServiceStart, tService))
            queue.register(Pacote(tArrival, tServiceStart, tService))
        else:
            queue.discard(Pacote(tArrival, 0, 0))
        t = tArrival
        leaky.get_tokens(t)
    
    atrasoVec = [i.tDelay for i in queue.log]
    mediaAtraso = sum(atrasoVec)/len(atrasoVec)
    utilizacao = lmbdLeaky/mu
    
    print("\nResultados:")
    print("Taxa de transmissão downstream para um nó do CMTS (bps): %.2f"%(txNodeMax))
    print("Taxa de transmissão downstream para um nó do CMTS (Pacotes/s): %.2f"%(txNodeMax/pkgSize))
    print("\nTaxa de chegada de pacotes após traffic shaping (bps): %.2f"%(txDadosLeaky))
    print("Taxa de chegada de pacotes após traffic shaping (Pacotes/s): %.2f"%(lmbdLeaky))
    print("\nTaxa de serviço do CM (bits/segundo): %.2f"%(mu*1504))
    print("Taxa de serviço do CM (pacotes/segundo): %.2f"%(mu))
    print("\nNumero de pacotes após traffic shapping: %d"%(queue.logSize()))
    print("Volume de dados após traffic shapping: %.2f"%(queue.logSize()*pkgSize))
    print("\nNumero de pacotes baixados: %d"%(len(downloaded)))
    print("Volume de dados baixados(bits): %.2f"%((len(downloaded)*pkgSize)))
    print("\nNumero de pacotes descartados: %d"%(queue.discSize()))
    print("Volume de dados descartados: %.2f"%(queue.discSize()*pkgSize))
    print("\nUtilização da fila (lmbdLeaky/mu): %f"%(utilizacao))
    print("\nAtraso médio na fila: %.5f s"%(mediaAtraso))
    
    ppt = pl.axes()
    ppt.plot(tLog, qsLog)
    ppt.set_title('Número de pacotes na fila x tempo')
    ppt.set_xlabel('t (s)')
    ppt.set_ylabel('Número de pacotes')
    

