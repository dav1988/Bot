#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Codi bàsic de bot que realitza enquestes per gestionar el personal que atent als pacients que han caigut.
 
import logging
import time
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from fitxer import id_users, personal

llista=[]
nollista=[]
count=0
personal=personal()
idiaio=random.randrange(10)
query_text="Ha caigut el l'avi " + str(idiaio) + " al 'lloc caiguda', necessita l'assistencia de 2 infermers/es"
 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


 
def start(bot, update):
    global query_text
    #identificador avi
    #localització caiguda
    keyboard = [[InlineKeyboardButton("✅ Vaig a assistir-lo", callback_data='1'), InlineKeyboardButton("❌ No puc atendre'l", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(query_text, reply_markup=reply_markup)
    starting_point=time.time()


    
 
def button(bot, update):
    global llista
    global nollista
    global count
    query = update.callback_query 
    ### Obtenció ID user ###
    nom=str(query)
    nom = nom.split(",")
    if str(nom[2])== " 'is_bot': False":
        iduser=nom[3]
    else:
        iduser=nom[4]
    iduser=iduser.split(" ")
    iduser=iduser[2]
    ########################
    if str(query.data)=="1" and str(iduser) not in llista:        
        llista.append(str(iduser))
        keyboard = [[InlineKeyboardButton("✅ Vaig a assistir-lo", callback_data='1'), InlineKeyboardButton("❌ No puc atendre'l", callback_data='2')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.editMessageText(text=query_text+ '\n ✅' + iduser , chat_id=query.message.chat_id, message_id=query.message.message_id,reply_markup=reply_markup)
        print "l'infermer/a "+ iduser +" va a socorrer a l'avi, fa falta un/a segon/a infermer/a"
        if len(llista)==2:
            bot.editMessageText(text="Els/Les infermers/es " + llista[0] + " i " + llista[1] + " van a socorrer l'avi "+str(idiaio)+" que ha caigut" , chat_id=query.message.chat_id, message_id=query.message.message_id)
            llista=[]
            nollista=[]
        elif str(iduser) in nollista:
            nollista.remove(str(iduser))
        
    elif str(query.data)=="2":
        if str(iduser) not in nollista:
            nollista.append(iduser)
            keyboard = [[InlineKeyboardButton("✅ Vaig a assistir-lo", callback_data='1'), InlineKeyboardButton("❌ No puc atendre'l", callback_data='2')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.editMessageText(text=query_text +'\n ❌' + iduser, chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup)
            if str(iduser) in llista:
                llista.remove(str(iduser))
                count=count-1
                print "l'infermer/a "+ iduser +" ja NO va a socorrer a l'avi, fan falta dos infermers/es"
        else:
            print iduser + " ja sabem que no hi vas"


    else:
        print "usuari "+ iduser +" ja sabem que vas a socorre l'avi"


        
def stop(bot, update):
    #error AttributeError: 'NoneType' object has no attribute 'message'
    query = update.callback_query
    bot.editMessageText(text="Enquesta cancelada" , chat_id=query.message.chat_id, message_id=query.message.message_id)


    
def help(bot, update):
    update.message.reply_text("Contacta amb el servei tècnic")

    
 
def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))
 





# Crea el Updater i pas del nostre token del bot.
updater = Updater("697741163:AAEIsJnN3fQehIhrXI_TjgzgwM0jMJlD7FE")
 
updater.dispatcher.add_handler(CommandHandler('query', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
#updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_error_handler(error)

try:
	# Inicia el bot
	print "inicialitzant bot [...]"	
	updater.start_polling()
	print "bot actiu"

	# Parar el bot 
	updater.idle()
except Exception as error:
	print ("Connectant amb el Bot de Telegram -> ERROR")
	print (error) # <- Error de connexió
	sys.exit(1)	
	
		
########################################################
################### Tasques pendents ###################
########################################################
# Relació de id's i noms de treballadors. ->BD
# Agafar directament els noms pot donar problemes de coincidencies. Millors utilitzar els id's i establir un nom per a cada treballador.-> BD
# Definir funció que mitjançant una senyal pel port serie realitzi l'enquesta
# ID caiguda, localització, Id avi
# Editar missatge ajuda. Afegir estat dels pacients.
# Opció stop per parar l'enquesta
# Temporitzador 5 min?
# Repassar ID. Amb el Josep no m'agafa la seva id, em retorna false.
# Falla funció identificació. Cosa rara amb el iduser.
# Retornar ID Caiguda i ID cuidadors al servidor.
#Altres proves
