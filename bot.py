import telebot
import os
from datetime import datetime

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

CONOCIMIENTO = {
    "resistencia": "Limita corriente. Se mide con multímetro en Ω. Fallas: valor alterado o quemada.",
    "capacitor": "Almacena carga. Tipos: electrolítico y cerámico. Fallas: inflado, ESR alto.",
    "mosfet": "Transistor de potencia. 3 pines: Gate, Drain, Source. Falla común: corto D-S.",
    "vrm": "Regulador de voltaje. Convierte 12V en voltajes precisos. Fallas: MOSFETs muertos.",
    "inductor": "Bobina que almacena energía magnética. Fallas: saturación, circuito abierto.",
    "diodo": "Permite flujo de corriente en una dirección. Fallas: corto o abierto.",
    "ic": "Circuito integrado. Chip que contiene múltiples componentes. Fallas: quemado, pines en corto."
}

DIAGNOSTICOS = {
    "no_enciende": """🔴 **DIAGNÓSTICO: PLACA NO ENCIENDE**

**Pasos:**
1. Verificar fuente da 12V/5V/3.3V con multímetro
2. Medir 5VSB (standby) en placa madre
3. Verificar botón de encendido funciona
4. Revisar señal POWER_GOOD
5. Medir VRMs sin carga
6. Buscar cortos a tierra en rieles principales

**Herramientas:** Multímetro, fuente ATX conocida
**Voltajes clave:** 5VSB, 12V, 5V, 3.3V, VCORE""",
    
    "no_video": """🔴 **DIAGNÓSTICO: NO DA VIDEO**

**Pasos:**
1. Verificar que placa enciende (fans, LEDs)
2. Testear con otra GPU o video integrado
3. Revisar slot PCIe (pines doblados/sucios)
4. Medir voltajes de VRM de GPU
5. Verificar RAM (probar en otro slot)
6. Revisar chip de video con pistola calor (avanzado)

**Causas comunes:** GPU muerta, slot dañado, BIOS corrupta, RAM mala"""
}

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"""
🔧 **HARDWAREPROF-AI ACTIVADO** 🔧

¡Hola {m.from_user.first_name}!

Soy tu mentor personal para reparación de tarjetas madre y GPUs.

**📚 COMANDOS:**
/componentes - Aprende sobre resistencias, MOSFETs, etc.
/diagnostico - Guías paso a paso
/herramientas - Qué comprar en Venezuela
/no_enciende - Diagnóstico placa no enciende
/no_video - Diagnóstico sin video

**🎯 PREGUNTAME DIRECTAMENTE:**
"¿Cómo mido un MOSFET?"
"¿Qué es un VRM?"
"Diferencia entre capacitor electrolítico y cerámico"

¡Empecemos! 💪
    """, parse_mode='Markdown')

@bot.message_handler(commands=['componentes'])
def componentes(m):
    texto = "🔌 **COMPONENTES PRINCIPALES:**\n\n"
    for comp, desc in CONOCIMIENTO.items():
        texto += f"**{comp.upper()}:**\n{desc}\n\n"
    texto += "💡 Escribí el nombre de un componente para más info"
    bot.reply_to(m, texto, parse_mode='Markdown')

@bot.message_handler(commands=['diagnostico'])
def diagnostico(m):
    bot.reply_to(m, """
🔍 **DIAGNÓSTICOS DISPONIBLES:**

/no_enciende - Placa no enciende
/no_video - No da video
/reinicia - Enciende y apaga
/artefactos - GPU con artefactos (próximamente)

O describime tu problema y te guío paso a paso.
    """, parse_mode='Markdown')

@bot.message_handler(commands=['no_enciende'])
def no_enciende(m):
    bot.reply_to(m, DIAGNOSTICOS['no_enciende'], parse_mode='Markdown')

@bot.message_handler(commands=['no_video'])
def no_video(m):
    bot.reply_to(m, DIAGNOSTICOS['no_video'], parse_mode='Markdown')

@bot.message_handler(commands=['herramientas'])
def herramientas(m):
    bot.reply_to(m, """
🛠️ **HERRAMIENTAS VENEZUELA 2026:**

**📦 KIT BÁSICO ($50-$80):**
• Multímetro Prasek PR-85: $25-$40
• Soldador 30W: $8-$15
• Flux pasta sin clean: $3-$8
• Pinzas antiestáticas: $5-$10
• Alcohol isopropílico 99%: $5-$10

**🔥 KIT INTERMEDIO ($200-$350):**
• Estación Yihua 853D: $80-$120
• Fuente voltaje variable 30V: $40-$80
• Pistola de calor: $30-$60
• Microscopio USB: $25-$50

**📍 DÓNDE COMPRAR:**
• MercadoLibre Venezuela
• Mundo Electrónico (Caracas)
• Grupos Telegram "Electrónica VE"
• AliExpress (20-40 días envío)

💡 **Tip:** Empezá con básico y andá upgradando
    """, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def responder(m):
    pregunta = m.text.lower()
    respuesta = None
    
    # Búsqueda en componentes
    for comp, desc in CONOCIMIENTO.items():
        if comp in pregunta:
            respuesta = f"🔌 **{comp.upper()}**\n\n{desc}\n\n💡 ¿Querés saber cómo medirlo? Preguntame: '¿Cómo mido {comp}?'"
            break
    
    # Respuestas sobre medición
    if "medir" in pregunta or "medicion" in pregunta:
        if "mosfet" in pregunta:
            respuesta = """📏 **CÓMO MEDIR UN MOSFET:**

**Con multímetro en modo DIODO:**

1. Identificá los pines: G (Gate), D (Drain), S (Source)
2. Desconectá el MOSFET del circuito (al menos 1 pata)
3. Medí D→S: debe leer infinito o muy alto
4. Medí S→D: debe leer infinito o muy alto
5. Medí G→S: debe leer infinito
6. Medí G→D: debe leer infinito

**Si alguna lectura da corto (0.000) = MOSFET MALO**

⚠️ Consultá el datasheet para valores exactos"""
        
        elif "capacitor" in pregunta:
            respuesta = """📏 **CÓMO MEDIR UN CAPACITOR:**

**Con multímetro en modo CAPACITANCIA:**

1. **DESCARGÁ EL CAPACITOR** (corto entre patas con destornillador aislado)
2. Desoldar al menos 1 pata del circuito
3. Configurá multímetro en modo F (Faradios)
4. Medí entre las 2 patas
5. Compará con valor marcado (ej: 1000µF)

**Tolerancia normal: ±20%**
**Si lee 50% menos = CAPACITOR MALO**

💡 Si está inflado/abombado = malo directo (ni lo midas)"""
    
    if not respuesta:
        respuesta = """🤔 Interesante pregunta.

📚 **Probá estos comandos:**
/componentes - Info detallada
/diagnostico - Guías de reparación
/herramientas - Qué necesitás

O reformulá tu pregunta:
Ejemplos: "¿Cómo mido un MOSFET?" / "¿Qué es un VRM?" """
    
    bot.reply_to(m, respuesta, parse_mode='Markdown')

if __name__ == '__main__':
    print("🤖 HardwareProf-AI iniciado")
    print("⚡ Bot activo 24/7")
    bot.infinity_polling()
