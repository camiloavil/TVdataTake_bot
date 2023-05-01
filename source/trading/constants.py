from datetime import timedelta
from enum import Enum

class temp(Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H2 = "2h"
    H4 = "4h"
    D1 = "1d"

class alarm_type(Enum):
    def __str__(self):
        return str(self.value)
    A_VOLUME    = "Volumen mayor a SMA"
    A_BB_H      = "Curce B Bollinger Superior"    #Banda de bollinger arriba
    A_BB_L      = "Cruce B Bollinger Inferior"    #Banda de bollinger abajo
    A_RSI7_H    = "RSI7 arriba del limite Superior"  #RSI_7 arriba del limite
    A_RSI7_L    = "RSI7 abajo del limite Inferior"  #RSI_7 abajo del limite
    A_INC_BBUp  = "Inclinacion pronunciada BB Superior"
    A_INC_BBDo  = "Inclinacion pronunciada BB Inferior"

class action_todo(Enum):
    def __str__(self):
        return str(self.value)
    NOTING           = "No se hace nada" 
    WAIT_BUY         = "Esperando gatillo para compra"
    WAIT_SELL        = "Esperando gatillo para venta"
    MAKE_BUY         = "BUY Market/Limit"
    MAKE_SELL        = "SELL Market/Limit"
    VALIDATE     = "Validar compra realizada"

class cons_strategy(Enum):
    RSI7_LOW        = 25 #Limite del RSI_7 abajo 27 puede ser temp alcista
    RSI7_LIMIT_BUY  = 35 #Limite del RSI_7 abajo 27 puede ser temp alcista
    RSI_7_HIGH      = 75 #Limite del RSI_7 Sobre Compra
    #INC_UP_BB  = 50 #Limite de pendiente de BB de subida
    #INC_DO_BB  =-50 #Limite de pendiente de BB de bajada

class strategy_type(Enum):
    def __str__(self):
        return str(self.value)
    ZERO            = "Ninguna"    #Ninguna Estrategia se descarta la Vela↗️ ↘️
    BB_BUY          = "Compra: por cruce de B Bollinger inferior"
    BB_RE_BUY       = "Re Compra: por cruce de B Bollinger inferior"
    BB_SELL         = "Venta: por cruce de B Bollinger superior"
    BB_RE_SELL      = "Re Venta: por cruce de B Bollinger superior"
    SURFBB_BUY      = "Long: por surf de B Bollinger superior"
    SURFBB_SELL     = "Short: por surf de B Bollinger inferior"

class deltaPrice(Enum):
    def __str__(self):
        return str(self.value)
    NUP  = "Tendencia Alza"
    NDO  = "Tendencia Baja"
    UP   = "Alto"   
    UPUP = "Alto mas alto"
    UPDO = "Alto mas bajo"
    DO   = "Bajo"
    DODO = "Bajo mas bajo"
    DOUP = "Bajo mas alto"

class candle_color(Enum):
    def __str__(self):
        return str(self.value)
    AZUL = "Azul"   
    ROJA = "Roja"

class candle_flow(Enum):
    def __str__(self):
        return str(self.value)
    BULLISH = "Alcista"
    DOUBT   = "Duda"
    BEARISH = "Bajista"
    NN      = "No definido"

class candle_type(Enum):
    def __str__(self):
        return str(self.value)
    NONO         = "no definida aun"
    HAMMER       = "Hammer"    #Vela martillo
    DOJI         = "Doji"
    HAMMER_INV   = "Martillo Invertido"    #Vela martillo
    BODY         = "con Cuerpo"
    NOBODY       = "sin Cuerpo" #puede ser doji
    DEAD         = "Muerta"
    T_HAMMER     = "Martillo con cola"
    T_HAMMER_INV = "Martillo Invertido con cola"
    DOUBT_B      = "Indecision con cuerpo"    #Vela indecision con cuerpo
    DOUBT_L      = "Indecision sin cuerpo"    #Vela indecision sin cuerpo
    NB_TAIL_UP   = "Cola arriba"    #liquidez o dejar cola
    NB_TAIL_DO   = "Cola abajo"    #liquidez o dejar cola

class TelegramTab(Enum):
    def __str__(self):
        return str(self.value)
    T1 = "  " 
    T2 = "    " 
    T3 = "      "  

def getDeltaTime(temp):
    if(temp=="1m"):
        return timedelta(minutes=1)
    elif(temp=="5m"):
        return timedelta(minutes=5)
    elif(temp=="15m"):
        return timedelta(minutes=15)
    elif(temp=="30m"):
        return timedelta(minutes=30)
    elif(temp=="1h"):
        return timedelta(hours=1)
    elif(temp=="2h"):
        return timedelta(hours=2)
    elif(temp=="4h"):
        return timedelta(hours=4)
    else:
        return timedelta(days=4)

def get_percentage(p_init,p_end):
    return (100*((float(p_end)-float(p_init))/float(p_init)))

def get_price_percen(percentage,p_init):
    return ((p_init*percentage/100)+p_init)

def get_range(range,p_start,p_end):
    return p_start+(range*(p_end-p_start))