import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import zipfile
import uservar
import fnmatch
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from urlparse import urljoin
from resources.libs import extract, downloader, notify, wizard as wiz

ADDON_ID         = uservar.ADDON_ID
ADDONTITLE       = uservar.ADDONTITLE
ADDON            = wiz.addonId(ADDON_ID)
VERSION          = wiz.addonInfo(ADDON_ID,'version')
ADDONPATH        = wiz.addonInfo(ADDON_ID,'path')
DIALOG           = xbmcgui.Dialog()
DP               = xbmcgui.DialogProgress()
HOME             = xbmc.translatePath('special://home/')
LOG              = xbmc.translatePath('special://logpath/')
PROFILE          = xbmc.translatePath('special://profile/')
ADDONS           = os.path.join(HOME,      'addons')
USERDATA         = os.path.join(HOME,      'userdata')
PLUGIN           = os.path.join(ADDONS,    ADDON_ID)
PACKAGES         = os.path.join(ADDONS,    'packages')
ADDOND           = os.path.join(USERDATA,  'addon_data')
ADDONDATA        = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED         = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES          = os.path.join(USERDATA,  'sources.xml')
FAVOURITES       = os.path.join(USERDATA,  'favourites.xml')
PROFILES         = os.path.join(USERDATA,  'profiles.xml')
GUISETTINGS      = os.path.join(USERDATA,  'guisettings.xml')
THUMBS           = os.path.join(USERDATA,  'Thumbnails')
DATABASE         = os.path.join(USERDATA,  'Database')
FANART           = os.path.join(ADDONPATH, 'fanart.jpg')
ICON             = os.path.join(ADDONPATH, 'icon.png')
ART              = os.path.join(ADDONPATH, 'resources', 'art')
WIZLOG           = os.path.join(ADDONDATA, 'wizard.log')
SKIN             = xbmc.getSkinDir()
BUILDNAME        = wiz.getS('buildname')
DEFAULTSKIN      = wiz.getS('defaultskin')
DEFAULTNAME      = wiz.getS('defaultskinname')
DEFAULTIGNORE    = wiz.getS('defaultskinignore')
BUILDVERSION     = wiz.getS('buildversion')
BUILDTHEME       = wiz.getS('buildtheme')
BUILDLATEST      = wiz.getS('latestversion')
INSTALLMETHOD    = wiz.getS('installmethod')
SHOW15           = wiz.getS('show15')
SHOW16           = wiz.getS('show16')
SHOW17           = wiz.getS('show17')
SHOW18           = wiz.getS('show18')
SHOWADULT        = wiz.getS('adult')
SHOWMAINT        = wiz.getS('showmaint')
AUTOCLEANUP      = wiz.getS('autoclean')
AUTOCACHE        = wiz.getS('clearcache')
AUTOPACKAGES     = wiz.getS('clearpackages')
AUTOTHUMBS       = wiz.getS('clearthumbs')
AUTOFEQ          = wiz.getS('autocleanfeq')
AUTONEXTRUN      = wiz.getS('nextautocleanup')
INCLUDEVIDEO     = wiz.getS('includevideo')
INCLUDEALL       = wiz.getS('includeall')
INCLUDEBOB       = wiz.getS('includebob')
INCLUDEPHOENIX   = wiz.getS('includephoenix')
INCLUDESPECTO    = wiz.getS('includespecto')
INCLUDEGENESIS   = wiz.getS('includegenesis')
INCLUDEEXODUS    = wiz.getS('includeexodus')
INCLUDEONECHAN   = wiz.getS('includeonechan')
INCLUDESALTS     = wiz.getS('includesalts')
INCLUDESALTSHD   = wiz.getS('includesaltslite')
SEPERATE         = wiz.getS('seperate')
NOTIFY           = wiz.getS('notify')
NOTEID           = wiz.getS('noteid')
NOTEDISMISS      = wiz.getS('notedismiss')
TRAKTSAVE        = wiz.getS('traktlastsave')
REALSAVE         = wiz.getS('debridlastsave')
LOGINSAVE        = wiz.getS('loginlastsave')
KEEPFAVS         = wiz.getS('keepfavourites')
KEEPSOURCES      = wiz.getS('keepsources')
KEEPPROFILES     = wiz.getS('keepprofiles')
KEEPADVANCED     = wiz.getS('keepadvanced')
KEEPREPOS        = wiz.getS('keeprepos')
KEEPSUPER        = wiz.getS('keepsuper')
KEEPWHITELIST    = wiz.getS('keepwhitelist')
KEEPTRAKT        = wiz.getS('keeptrakt')
KEEPREAL         = wiz.getS('keepdebrid')
KEEPLOGIN        = wiz.getS('keeplogin')
LOGINSAVE        = wiz.getS('loginlastsave')
DEVELOPER        = wiz.getS('developer')
THIRDPARTY       = wiz.getS('enable3rd')
THIRD1NAME       = wiz.getS('wizard1name')
THIRD1URL        = wiz.getS('wizard1url')
THIRD2NAME       = wiz.getS('wizard2name')
THIRD2URL        = wiz.getS('wizard2url')
THIRD3NAME       = wiz.getS('wizard3name')
THIRD3URL        = wiz.getS('wizard3url')
BACKUPLOCATION   = ADDON.getSetting('path') if not ADDON.getSetting('path') == '' else 'special://home/'
MYBUILDS         = os.path.join(BACKUPLOCATION, 'My_Builds', '')
AUTOFEQ          = int(float(AUTOFEQ)) if AUTOFEQ.isdigit() else 0
TODAY            = date.today()
TOMORROW         = TODAY + timedelta(days=1)
THREEDAYS        = TODAY + timedelta(days=3)
KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
MCNAME           = wiz.mediaCenter()
EXCLUDES         = uservar.EXCLUDES
BUILDFILE        = uservar.BUILDFILE
APKFILE          = uservar.APKFILE
YOUTUBETITLE     = uservar.YOUTUBETITLE
YOUTUBEFILE      = uservar.YOUTUBEFILE
ADDONFILE        = uservar.ADDONFILE
ADVANCEDFILE     = uservar.ADVANCEDFILE
UPDATECHECK      = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK        = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION     = uservar.NOTIFICATION
ENABLE           = uservar.ENABLE
HEADERMESSAGE    = uservar.HEADERMESSAGE
AUTOUPDATE       = uservar.AUTOUPDATE
WIZARDFILE       = uservar.WIZARDFILE
HIDECONTACT      = uservar.HIDECONTACT
CONTACT          = uservar.CONTACT
CONTACTICON      = uservar.CONTACTICON if not uservar.CONTACTICON == 'http://' else ICON 
CONTACTFANART    = uservar.CONTACTFANART if not uservar.CONTACTFANART == 'http://' else FANART
HIDESPACERS      = uservar.HIDESPACERS
COLOR1           = uservar.COLOR1
COLOR2           = uservar.COLOR2
THEME1           = uservar.THEME1
THEME2           = uservar.THEME2
THEME3           = uservar.THEME3
THEME4           = uservar.THEME4
THEME5           = uservar.THEME5
ICONBUILDS       = uservar.ICONBUILDS if not uservar.ICONBUILDS == 'http://' else ICON
ICONMAINT        = uservar.ICONMAINT if not uservar.ICONMAINT == 'http://' else ICON
ICONSPEED        = uservar.ICONSPEED if not uservar.ICONSPEED == 'http://' else ICON
ICONAPK          = uservar.ICONAPK if not uservar.ICONAPK == 'http://' else ICON
ICONRETRO        = uservar.ICONRETRO if not uservar.ICONRETRO == 'http://' else ICON
ICONADDONS       = uservar.ICONADDONS if not uservar.ICONADDONS == 'http://' else ICON
ICONYOUTUBE      = uservar.ICONYOUTUBE if not uservar.ICONYOUTUBE == 'http://' else ICON
ICONSAVE         = uservar.ICONSAVE if not uservar.ICONSAVE == 'http://' else ICON
ICONTRAKT        = uservar.ICONTRAKT if not uservar.ICONTRAKT == 'http://' else ICON
ICONREAL         = uservar.ICONREAL if not uservar.ICONREAL == 'http://' else ICON
ICONLOGIN        = uservar.ICONLOGIN if not uservar.ICONLOGIN == 'http://' else ICON
ICONCONTACT      = uservar.ICONCONTACT if not uservar.ICONCONTACT == 'http://' else ICON
ICONSETTINGS     = uservar.ICONSETTINGS if not uservar.ICONSETTINGS == 'http://' else ICON
LOGFILES         = wiz.LOGFILES
#TRAKTID          = traktit.TRAKTID
#DEBRIDID         = debridit.DEBRIDID
#LOGINID          = loginit.LOGINID

def index():
	if HIDESPACERS == 'Yes': addFile(wiz.sep(), '', themeit=THEME3)
	
	addDir ('Utilidades'   ,'maint',    icon=ICONMAINT,    themeit=THEME1)
	

	addFile ('[COLOR red][B][I]- El mal uso puede provocar errores en el sistema[/I][/B][/COLOR] ' ,'grupo', icon=ICONSPEED, themeit=THEME3)

#	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	
	addFile ('Test de Velocidad' ,'speed', icon=ICONSPEED, themeit=THEME1)
	
	addFile ('[B][I]- Consulta la velocidad de tu conexion[/I][/B] ' ,'grupo', icon=ICONSPEED, themeit=THEME3)
	
#	if HIDECONTACT == 'No': addFile('Contacto' ,'contact', icon=ICONCONTACT,  themeit=THEME1)

	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addFile('Ajustes'      ,'settings', icon=ICONSETTINGS, themeit=THEME1)
	addFile ('[I]- Establece tus preferencias[/I] ' ,'grupo', icon=ICONSPEED, themeit=THEME3)
	
	if DEVELOPER == 'true': addDir('Developer Menu','developer', icon=ICONSETTINGS, themeit=THEME1)
	setView('files', 'viewType')


			

def maintMenu(view=None):
	on = '[COLOR green]ON[/COLOR]'; off = '[COLOR red]OFF[/COLOR]'
	autoclean   = 'true' if AUTOCLEANUP    == 'true' else 'false'
	cache       = 'true' if AUTOCACHE      == 'true' else 'false'
	packages    = 'true' if AUTOPACKAGES   == 'true' else 'false'
	thumbs      = 'true' if AUTOTHUMBS     == 'true' else 'false'
	maint       = 'true' if SHOWMAINT      == 'true' else 'false'
	includevid  = 'true' if INCLUDEVIDEO   == 'true' else 'false'
	includeall  = 'true' if INCLUDEALL     == 'true' else 'false'
	thirdparty  = 'true' if THIRDPARTY     == 'true' else 'false'
	if wiz.Grab_Log(True) == False: kodilog = 0
	else: kodilog = errorChecking(wiz.Grab_Log(True), True, True)
	if wiz.Grab_Log(True, True) == False: kodioldlog = 0
	else: kodioldlog = errorChecking(wiz.Grab_Log(True,True), True, True)
	errorsinlog = int(kodilog) + int(kodioldlog)
	errorsfound = str(errorsinlog) + ' Error(s) Found' if errorsinlog > 0 else 'None Found'
	wizlogsize = ': [COLOR red]Not Found[/COLOR]' if not os.path.exists(WIZLOG) else ": [COLOR green]%s[/COLOR]" % wiz.convertSize(os.path.getsize(WIZLOG))
#	if includeall == 'true':
#		includebob = 'true'
#		includepho = 'true'
#		includespe = 'true'
#		includegen = 'true'
#		includeexo = 'true'
#		includeone = 'true'
#		includesal = 'true'
#		includeshd = 'true'
#	else:
#		includebob = 'true' if INCLUDEBOB     == 'true' else 'false'
#		includepho = 'true' if INCLUDEPHOENIX == 'true' else 'false'
#		includespe = 'true' if INCLUDESPECTO  == 'true' else 'false'
#		includegen = 'true' if INCLUDEGENESIS == 'true' else 'false'
#		includeexo = 'true' if INCLUDEEXODUS  == 'true' else 'false'
#		includeone = 'true' if INCLUDEONECHAN == 'true' else 'false'
#		includesal = 'true' if INCLUDESALTS   == 'true' else 'false'
#		includeshd = 'true' if INCLUDESALTSHD == 'true' else 'false'
	sizepack   = wiz.getSize(PACKAGES)
	sizethumb  = wiz.getSize(THUMBS)
	sizecache  = wiz.getCacheSize()
	totalsize  = sizepack+sizethumb+sizecache
	feq        = ['Siempre', 'A diario', '3 Dias', 'Semanal']
		

	addDir ('Limpieza Manual'       ,'maint', 'clean',  icon=ICONMAINT, themeit=THEME1)
	if view == "clean" or SHOWMAINT == 'true': 
		addFile('Limpieza Total: [COLOR green][B]%s[/B][/COLOR]' % wiz.convertSize(totalsize)  ,'fullclean',       icon=ICONMAINT, themeit=THEME3)
		addFile('Borra Cache: [COLOR green][B]%s[/B][/COLOR]' % wiz.convertSize(sizecache)     ,'clearcache',      icon=ICONMAINT, themeit=THEME3)
		addFile('Borra Packages: [COLOR green][B]%s[/B][/COLOR]' % wiz.convertSize(sizepack)   ,'clearpackages',   icon=ICONMAINT, themeit=THEME3)
		addFile('Borra Thumbnails: [COLOR green][B]%s[/B][/COLOR]' % wiz.convertSize(sizethumb),'clearthumb',      icon=ICONMAINT, themeit=THEME3)
		addFile('Borra iconos desactualizados', 'oldThumbs',      icon=ICONMAINT, themeit=THEME3)
		addFile('Borra Crash Logs',               'clearcrash',      icon=ICONMAINT, themeit=THEME3)



	addDir ('Limpieza Automatica'     ,'maint', 'Auto Clean',   icon=ICONMAINT, themeit=THEME1)
	if view == "Auto Clean" or SHOWMAINT == 'true':
		#addFile('Auto Clean', '', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
		addFile('Limpieza Automatica al inicio: %s' % autoclean.replace('true',on).replace('false',off) ,'togglesetting', 'autoclean',   icon=ICONMAINT, themeit=THEME3)
	if autoclean == 'true':
		addFile('--- Frecuencia Limpieza Auto: [B][COLOR green]%s[/COLOR][/B]' % feq[AUTOFEQ], 'changefeq', icon=ICONMAINT, themeit=THEME3)
		addFile('--- Borra Cache al inicio: %s' % cache.replace('true',on).replace('false',off), 'togglesetting', 'clearcache', icon=ICONMAINT, themeit=THEME3)
		addFile('--- Borra Packages al inicio: %s' % packages.replace('true',on).replace('false',off), 'togglesetting', 'clearpackages', icon=ICONMAINT, themeit=THEME3)
		addFile('--- Borra Thumbnails al inicio: %s' % thumbs.replace('true',on).replace('false',off), 'togglesetting', 'clearthumbs', icon=ICONMAINT, themeit=THEME3)
	#	addFile('Clear Video Cache', '', fanart=FANART, icon=ICONMAINT, themeit=THEME1)
		addFile('Incluye Cache de Video en Borrado: %s' % includevid.replace('true',on).replace('false',off), 'togglecache', 'includevideo', icon=ICONMAINT, themeit=THEME3)
		if includevid == 'true':
			addFile('--- Incluye Todos los Addons de Video: %s' % includeall.replace('true',on).replace('false',off), 'togglecache', 'includeall', icon=ICONMAINT, themeit=THEME3)


		
	addDir ('Accesorios'     ,'maint', 'misc',   icon=ICONMAINT, themeit=THEME1)
	if view == "misc" or SHOWMAINT == 'true': 
		addFile('Kodi 17 Fix',                    'kodi17fix',       icon=ICONMAINT, themeit=THEME3)
		addFile('Fuerza Addons a Actualizar',            'forceupdate',     icon=ICONMAINT, themeit=THEME3)
		addFile('Fija Addons NO actualizados',        'fixaddonupdate',  icon=ICONMAINT, themeit=THEME3)
		
		addFile('Recarga Skin',                    'forceskin',       icon=ICONMAINT, themeit=THEME3)
		addFile('Recarga Perfil',                 'forceprofile',    icon=ICONMAINT, themeit=THEME3)	
		addFile('Cierra Kodi a la Fuerza',               'forceclose',      icon=ICONMAINT, themeit=THEME3)		
		
		addFile('Ver Errores en el Log: %s' % (errorsfound), 'viewerrorlog',    icon=ICONMAINT, themeit=THEME3)
		addFile('Ver TODO el Archivo Log',                  'viewlog',         icon=ICONMAINT, themeit=THEME3)
		
	addDir ('Utilidades'     ,'maint', 'utils',   icon=ICONMAINT, themeit=THEME1)
	if view == "utils" or SHOWMAINT == 'true': 	
	
	#	addFile(wiz.sep(), '', themeit=THEME3)			
	
		addFile('Quita Nombres de Archivo no ASCII',     'asciicheck',      icon=ICONMAINT, themeit=THEME3)	
		addFile('Convierte Rutas en speciales',       'convertpath',     icon=ICONMAINT, themeit=THEME3)	
		addFile('Escanea Fuentes con links Rotos',  'checksources',    icon=ICONMAINT, themeit=THEME3)
		addFile('Escanea Repositorios Rotos',   'checkrepos',      icon=ICONMAINT, themeit=THEME3)
		
		addFile('--- Activa Todos los Addons de Video', 'togglecache', 'true', icon=ICONMAINT, themeit=THEME3)
		addFile('--- Deshabilita Todos los Addons de Video', 'togglecache', 'false', icon=ICONMAINT, themeit=THEME3)				
		addFile(wiz.sep(), '', themeit=THEME3)
		addFile('[COLOR red][B]* Elimina Database - Destruye tu configuracion[/B][/COLOR]',                'purgedb',         icon=ICONMAINT, themeit=THEME2)
		addFile('[COLOR red][B]* Fresh Start - RESTAURA KODI A CONFIG INICIAL[/B][/COLOR]',                    'freshstart',      icon=ICONMAINT, themeit=THEME2)
		
		
	addDir ('BackUp'     ,'maint', 'backup',   icon=ICONMAINT, themeit=THEME1)
	if view == "backup" or SHOWMAINT == 'true':
		addFile('Borra archivo de BackUp',        'clearbackup',     icon=ICONMAINT,   themeit=THEME3)
		addFile('Carpeta del BackUp: [COLOR %s]%s[/COLOR]' % (COLOR2, MYBUILDS),'settings', 'Maintenance', icon=ICONMAINT, themeit=THEME3)
		addFile('Hacer BackUp',               'backupbuild',     icon=ICONMAINT,   themeit=THEME3)
		addFile('Restaurar Copia de Seguridad',         'restorezip',      icon=ICONMAINT,   themeit=THEME3)
		
	addDir ('Config. AdvancedSettings',       'maint', 'tweaks', icon=ICONMAINT, themeit=THEME1)
	if view == "tweaks" or SHOWMAINT == 'true': 
		if not ADVANCEDFILE == 'http://' and not ADVANCEDFILE == '':
			addDir ('[COLOR lime][B]- Config. Advanced Settings[/B][/COLOR]',            'advancedsetting',  icon=ICONMAINT, themeit=THEME3)
		else: 
			if os.path.exists(ADVANCED):
				addFile('[B]Ver archivo actual AdvancedSettings.xml[/B]',   'currentsettings', icon=ICONMAINT, themeit=THEME3)
				addFile('[COLOR red][B]Borrar el actual AdvancedSettings.xml[/B][/COLOR]', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
			addFile('[B]Configuracion Rapida de AdvancedSettings.xml[/B]',    'autoadvanced',    icon=ICONMAINT, themeit=THEME3)


					
		
	setView('files', 'viewType')

	
	
	
def advancedWindow(url=None):
	if not ADVANCEDFILE == 'http://':
		if url == None:
			ADVANCEDWORKING = wiz.workingURL(ADVANCEDFILE)
			TEMPADVANCEDFILE = uservar.ADVANCEDFILE
		else:
			ADVANCEDWORKING  = wiz.workingURL(url)
			TEMPADVANCEDFILE = url
		addFile('[B]Configuracion Rapida de AdvancedSettings.xml[/B]', 'autoadvanced', icon=ICONMAINT, themeit=THEME3)
		if os.path.exists(ADVANCED): 
			addFile('[B]Ver archivo actual AdvancedSettings.xml[/B]', 'currentsettings', icon=ICONMAINT, themeit=THEME3)
			addFile('[COLOR red][B]Borrar el actual AdvancedSettings.xml[/B][/COLOR]', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
		if ADVANCEDWORKING == True:
			if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONMAINT, themeit=THEME3)
			link = wiz.openURL(TEMPADVANCEDFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				for name, section, url, icon, fanart, description in match:
					if section.lower() == "yes":
						addDir ("[B]%s[/B]" % name, 'advancedsetting', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					else:
						addFile(name, 'writeadvanced', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
			else: wiz.log("[Advanced Settings] ERROR: Invalid Format.")
		else: wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING)
	else: wiz.log("[Advanced Settings] not Enabled")

def writeAdvanced(name, url):
	ADVANCEDWORKING = wiz.workingURL(url)
	if ADVANCEDWORKING == True:
		if os.path.exists(ADVANCED): choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres reemplazar tu actual archivo de AdvancedSettings con [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR green]Reemplazar[/COLOR][/B]", nolabel="[B][COLOR red]Cancelar[/COLOR][/B]")
		else: choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Te gustaria descargar e instalar [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR green]Instalar[/COLOR][/B]", nolabel="[B][COLOR red]Cancelar[/COLOR][/B]")

		if choice == 1:
			file = wiz.openURL(url)
			f = open(ADVANCED, 'w'); 
			f.write(file)
			f.close()
			DIALOG.ok(ADDONTITLE, '[COLOR %s]AdvancedSettings.xml se ha escrito correctamente. Una vez que hagas clic en Aceptar, forzaras el cierre de kodi.[/COLOR]' % COLOR2)
			wiz.killxbmc(True)
		else: wiz.log("[Advanced Settings] instalacion canceleda"); wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), "[COLOR %s]Escritura Cancelada![/COLOR]" % COLOR2); return
	else: wiz.log("[Advanced Settings] URL no funciona: %s" % ADVANCEDWORKING); wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), "[COLOR %s]URL No funciona[/COLOR]" % COLOR2)

def viewAdvanced():
	f = open(ADVANCED)
	a = f.read().replace('\t', '    ')
	wiz.TextBox(ADDONTITLE, a)
	f.close()

def removeAdvanced():
	if os.path.exists(ADVANCED):
		wiz.removeFile(ADVANCED)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]AdvancedSettings.xml not found[/COLOR]")

def showAutoAdvanced():
	notify.autoConfig()




def fixUpdate():
	if KODIV < 17: 
		dbfile = os.path.join(DATABASE, wiz.latestDB('Addons'))
		try:
			os.remove(dbfile)
		except Exception, e:
			wiz.log("Unable to remove %s, Purging DB" % dbfile)
			wiz.purgeDb(dbfile)
	else:
		xbmc.log("Requested Addons.db be removed but doesnt work in Kod17")

def changeFeq():
	feq        = ['Cada inicio', 'Cada dia', 'Cada tres dias', 'Semanalmente']
	change     = DIALOG.select("[COLOR %s]Con que frecuencia quieres que se ejecute?[/COLOR]" % COLOR2, feq)
	if not change == -1: 
		wiz.setS('autocleanfeq', str(change))
		wiz.LogNotify('[COLOR %s]Auto Clean Up[/COLOR]' % COLOR1, '[COLOR %s]Fequency Now %s[/COLOR]' % (COLOR2, feq[change]))





#def testTheme(path):
#	zfile = zipfile.ZipFile(path)
#	for item in zfile.infolist():
#		if '/settings.xml' in item.filename:
#			return True
#	return False

#def testGui(path):
#	zfile = zipfile.ZipFile(path)
#	for item in zfile.infolist():
#		if '/guisettings.xml' in item.filename:
#			return True
#	return False



def toggleCache(state):
	cachelist = ['includevideo', 'includeall', 'includebob', 'includephoenix', 'includespecto', 'includegenesis', 'includeexodus', 'includeonechan', 'includesalts', 'includesaltslite']
	titlelist = ['Include Video Addons', 'Include All Addons', 'Include Bob', 'Include Phoenix', 'Include Specto', 'Include Genesis', 'Include Exodus', 'Include One Channel', 'Include Salts', 'Include Salts Lite HD']
	if state in ['true', 'false']:
		for item in cachelist:
			wiz.setS(item, state)
	else:
		if not state in ['includevideo', 'includeall'] and wiz.getS('includeall') == 'true':
			try:
				item = titlelist[cachelist.index(state)]
				DIALOG.ok(ADDONTITLE, "[COLOR %s]Tendra que deshabilitar [COLOR %s]Incluir TODOS los Addons[/COLOR] a desactivar[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, COLOR1, item))
			except:
				wiz.LogNotify("[COLOR %s]Toggle Cache[/COLOR]" % COLOR1, "[COLOR %s]Invalid id: %s[/COLOR]" % (COLOR2, state))
		else:
			new = 'true' if wiz.getS(state) == 'false' else 'false'
			wiz.setS(state, new)

def playVideo(url):
	if 'watch?v=' in url:
		a, b = url.split('?')
		find = b.split('&')
		for item in find:
			if item.startswith('v='):
				url = item[2:]
				break
			else: continue
	elif 'embed' in url or 'youtu.be' in url:
		a = url.split('/')
		if len(a[-1]) > 5:
			url = a[-1]
		elif len(a[-2]) > 5:
			url = a[-2]
	wiz.log("YouTube URL: %s" % url)
	yt.PlayVideo(url)

def viewLogFile():
	mainlog = wiz.Grab_Log(True)
	oldlog  = wiz.Grab_Log(True, True)
	which = 0; logtype = mainlog
	if not oldlog == False and not mainlog == False:
		which = DIALOG.select(ADDONTITLE, ["Ver %s" % mainlog.replace(LOG, ""), "Ver %s" % oldlog.replace(LOG, "")])
		if which == -1: wiz.LogNotify('[COLOR %s]Ver Log[/COLOR]' % COLOR1, '[COLOR %s]Ver Log Cancelado![/COLOR]' % COLOR2); return
	elif mainlog == False and oldlog == False:
		wiz.LogNotify('[COLOR %s]Ver Log[/COLOR]' % COLOR1, '[COLOR %s]Log File No Encontrado![/COLOR]' % COLOR2)
		return
	elif not mainlog == False: which = 0
	elif not oldlog == False: which = 1
	
	logtype = mainlog if which == 0 else oldlog
	msg     = wiz.Grab_Log(False) if which == 0 else wiz.Grab_Log(False, True)
	
	wiz.TextBox("%s - %s" % (ADDONTITLE, logtype), msg)

def errorChecking(log=None, count=None, all=None):
	if log == None:
		mainlog = wiz.Grab_Log(True)
		oldlog  = wiz.Grab_Log(True, True)
		if not oldlog == False and not mainlog == False:
			which = DIALOG.select(ADDONTITLE, ["Ver %s: %s error(es)" % (mainlog.replace(LOG, ""), errorChecking(mainlog, True, True)), "Ver %s: %s error(es)" % (oldlog.replace(LOG, ""), errorChecking(oldlog, True, True))])
			if which == -1: wiz.LogNotify('[COLOR %s]Ver Log[/COLOR]' % COLOR1, '[COLOR %s]Ver Log Cancelado![/COLOR]' % COLOR2); return
		elif mainlog == False and oldlog == False:
			wiz.LogNotify('[COLOR %s]View Log[/COLOR]' % COLOR1, '[COLOR %s]Log File No Encontrado![/COLOR]' % COLOR2)
			return
		elif not mainlog == False: which = 0
		elif not oldlog == False: which = 1
		log = mainlog if which == 0 else oldlog
	if log == False:
		if count == None:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Log File No Encontrado[/COLOR]" % COLOR2)
			return False
		else: 
			return 0
	else:
		if os.path.exists(log):
			f = open(log,mode='r'); a = f.read().replace('\n', '').replace('\r', ''); f.close()
			match = re.compile("-->Python callback/script devuelve el siguiente error<--(.+?)-->Fin del mensaje de error del script Python<--").findall(a)
			if not count == None:
				if all == None: 
					x = 0
					for item in match:
						if ADDON_ID in item: x += 1
					return x
				else: return len(match)
			if len(match) > 0:
				x = 0; msg = ""
				for item in match:
					if all == None and not ADDON_ID in item: continue
					else: 
						x += 1
						msg += "[COLOR red]Error Number %s[/COLOR]\n(PythonToCppException) : -->Python callback/script returned the following error<--%s-->Fin del mensaje de error del script Python<--\n\n" % (x, item.replace('                                          ', '\n').replace('\\\\','\\').replace(HOME, ''))
				if x > 0:
					wiz.TextBox(ADDONTITLE, msg)
				else: wiz.LogNotify(ADDONTITLE, "Sin errores en Log")
			else: wiz.LogNotify(ADDONTITLE, "Sin errores en Log")
		else: wiz.LogNotify(ADDONTITLE, "Log File no Encontrado")

ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108

def LogViewer(default=None):
	class LogViewer(xbmcgui.WindowXMLDialog):
		def __init__(self,*args,**kwargs):
			self.default = kwargs['default']

		def onInit(self):
			self.title      = 101
			self.msg        = 102
			self.scrollbar  = 103
			self.upload     = 201
			self.kodi       = 202
			self.kodiold    = 203
			self.wizard     = 204 
			self.okbutton   = 205 
			f = open(self.default, 'r')
			self.logmsg = f.read()
			f.close()
			self.titlemsg = "%s: %s" % (ADDONTITLE, self.default.replace(LOG, '').replace(ADDONDATA, ''))
			self.showdialog()

		def showdialog(self):
			self.getControl(self.title).setLabel(self.titlemsg)
			self.getControl(self.msg).setText(wiz.highlightText(self.logmsg))
			self.setFocusId(self.scrollbar)
			
		def onClick(self, controlId):
			if   controlId == self.okbutton: self.close()
			elif controlId == self.upload: self.close(); uploadLog.Main()
			elif controlId == self.kodi:
				newmsg = wiz.Grab_Log(False)
				filename = wiz.Grab_Log(True)
				if newmsg == False:
					self.titlemsg = "%s: Ver Error Log" % ADDONTITLE
					self.getControl(self.msg).setText("Log File No Existe!")
				else:
					self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(LOG, ''))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
			elif controlId == self.kodiold:  
				newmsg = wiz.Grab_Log(False, True)
				filename = wiz.Grab_Log(True, True)
				if newmsg == False:
					self.titlemsg = "%s: Ver Error Log" % ADDONTITLE
					self.getControl(self.msg).setText("Log File No Existe!")
				else:
					self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(LOG, ''))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
			elif controlId == self.wizard:
				newmsg = wiz.Grab_Log(False, False, True)
				filename = wiz.Grab_Log(True, False, True)
				if newmsg == False:
					self.titlemsg = "%s: Ver Error Log" % ADDONTITLE
					self.getControl(self.msg).setText("Log File No Existe!")
				else:
					self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(ADDONDATA, ''))
					self.getControl(self.title).setLabel(self.titlemsg)
					self.getControl(self.msg).setText(wiz.highlightText(newmsg))
					self.setFocusId(self.scrollbar)
		
		def onAction(self, action):
			if   action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()
	if default == None: default = wiz.Grab_Log(True)
	lv = LogViewer( "LogViewer.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', default=default)
	lv.doModal()
	del lv



def removeAddonData(addon, name=None, over=False):
	if addon == 'all':
		if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in you Userdata folder?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR green]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
			wiz.cleanHouse(ADDOND)
		else: wiz.LogNotify('[COLOR %s]Remove Addon Data[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
	elif addon == 'uninstalled':
		if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in you Userdata folder for uninstalled addons?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR green]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
			total = 0
			for folder in glob.glob(os.path.join(ADDOND, '*')):
				foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
				if foldername in EXCLUDES: pass
				elif os.path.exists(os.path.join(ADDONS, foldername)): pass
				else: wiz.cleanHouse(folder); total += 1; wiz.log(folder); shutil.rmtree(folder)
			wiz.LogNotify('[COLOR %s]Clean up Uninstalled[/COLOR]' % COLOR1, '[COLOR %s]%s Folders(s) Removed[/COLOR]' % (COLOR2, total))
		else: wiz.LogNotify('[COLOR %s]Remove Addon Data[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
	elif addon == 'empty':
		if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] empty addon data folders in you Userdata folder?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR green]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
			total = wiz.emptyfolder(ADDOND)
			wiz.LogNotify('[COLOR %s]Remove Empty Folders[/COLOR]' % COLOR1, '[COLOR %s]%s Folders(s) Removed[/COLOR]' % (COLOR2, total))
		else: wiz.LogNotify('[COLOR %s]Remove Empty Folders[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
	else:
		addon_data = os.path.join(USERDATA, 'addon_data', addon)
		if addon in EXCLUDES:
			wiz.LogNotify("[COLOR %s]Protected Plugin[/COLOR]" % COLOR1, "[COLOR %s]Not allowed to remove Addon_Data[/COLOR]" % COLOR2)
		elif os.path.exists(addon_data):  
			if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you also like to remove the addon data for:[/COLOR]' % COLOR2, '[COLOR %s]%s[/COLOR]' % (COLOR1, addon), yeslabel='[B][COLOR green]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
				wiz.cleanHouse(addon_data)
				try:
					shutil.rmtree(addon_data)
				except:
					wiz.log("Error deleting: %s" % addon_data)
			else: 
				wiz.log('Addon data for %s was not removed' % addon)
	wiz.refresh()

def restoreit(type):
	if type == 'build':
		x = freshStart('restore')
		if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Local Restore Cancelado[/COLOR]" % COLOR2); return
	if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
		wiz.skinToDefault()
	wiz.restoreLocal(type)

def restoreextit(type):
	if type == 'build':
		x = freshStart('restore')
		if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]External Restore Cancelled[/COLOR]" % COLOR2); return
	wiz.restoreExternal(type)



def buildVideo(name):
	if wiz.workingURL(BUILDFILE) == True:
		videofile = wiz.checkBuild(name, 'preview')
		if videofile and not videofile == 'http://': playVideo(videofile)
		else: wiz.log("[%s]Unable to find url for video preview" % name)
	else: wiz.log("Build text file not working: %s" % WORKINGURL)

def dependsList(plugin):
	addonxml = os.path.join(ADDONS, plugin, 'addon.xml')
	if os.path.exists(addonxml):
		source = open(addonxml,mode='r'); link = source.read(); source.close(); 
		match  = wiz.parseDOM(link, 'import', ret='addon')
		items  = []
		for depends in match:
			if not 'xbmc.python' in depends:
				items.append(depends)
		return items
	return []

	
	
def manageSaveData(do):
	if do == 'import':
		TEMP = os.path.join(ADDONDATA, 'temp')
		if not os.path.exists(TEMP): os.makedirs(TEMP)
		source = DIALOG.browse(1, '[COLOR %s]Select the location of the SaveData.zip[/COLOR]' % COLOR2, 'files', '.zip', False, False, HOME)
		if not source.endswith('.zip'):
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import Data Error![/COLOR]" % (COLOR2))
			return
		tempfile = os.path.join(MYBUILDS, 'SaveData.zip')
		goto = xbmcvfs.copy(source, tempfile)
		wiz.log("%s" % str(goto))
		extract.all(xbmc.translatePath(tempfile), TEMP)
		trakt  = os.path.join(TEMP, 'trakt')
		login  = os.path.join(TEMP, 'login')
		debrid = os.path.join(TEMP, 'debrid')
		x = 0
		if os.path.exists(trakt):
			x += 1
			files = os.listdir(trakt)
			if not os.path.exists(traktit.TRAKTFOLD): os.makedirs(traktit.TRAKTFOLD)
			for item in files:
				old  = os.path.join(traktit.TRAKTFOLD, item)
				temp = os.path.join(trakt, item)
				if os.path.exists(old):
					if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR green]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
					else: os.remove(old)
				shutil.copy(temp, old)
			traktit.importlist('all')
			traktit.traktIt('restore', 'all')
		if os.path.exists(login):
			x += 1
			files = os.listdir(login)
			if not os.path.exists(loginit.LOGINFOLD): os.makedirs(loginit.LOGINFOLD)
			for item in files:
				old  = os.path.join(loginit.LOGINFOLD, item)
				temp = os.path.join(login, item)
				if os.path.exists(old):
					if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR green]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
					else: os.remove(old)
				shutil.copy(temp, old)
			loginit.importlist('all')
			loginit.loginIt('restore', 'all')
		if os.path.exists(debrid):
			x += 1
			files = os.listdir(debrid)
			if not os.path.exists(debridit.REALFOLD): os.makedirs(debridit.REALFOLD)
			for item in files:
				old  = os.path.join(debridit.REALFOLD, item)
				temp = os.path.join(debrid, item)
				if os.path.exists(old):
					if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR green]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
					else: os.remove(old)
				shutil.copy(temp, old)
			debridit.importlist('all')
			debridit.debridIt('restore', 'all')
		wiz.cleanHouse(TEMP)
		wiz.removeFolder(TEMP)
		os.remove(tempfile)
		if x == 0: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Failed[/COLOR]" % COLOR2)
		else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Complete[/COLOR]" % COLOR2)
	elif do == 'export':
		mybuilds = xbmc.translatePath(MYBUILDS)
		dir = [traktit.TRAKTFOLD, debridit.REALFOLD, loginit.LOGINFOLD]
		traktit.traktIt('update', 'all')
		loginit.loginIt('update', 'all')
		debridit.debridIt('update', 'all')
		source = DIALOG.browse(3, '[COLOR %s]Select where you wish to export the savedata zip?[/COLOR]' % COLOR2, 'files', '', False, True, HOME)
		source = xbmc.translatePath(source)
		tempzip = os.path.join(mybuilds, 'SaveData.zip')
		zipf = zipfile.ZipFile(tempzip, mode='w')
		for fold in dir:
			if os.path.exists(fold):
				files = os.listdir(fold)
				for file in files:
					zipf.write(os.path.join(fold, file), os.path.join(fold, file).replace(ADDONDATA, ''), zipfile.ZIP_DEFLATED)
		zipf.close()
		if source == mybuilds:
			DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))
		else:
			try:
				xbmcvfs.copy(tempzip, os.path.join(source, 'SaveData.zip'))
				DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, os.path.join(source, 'SaveData.zip')))
			except:
				DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, tempzip))


				
def freshStart(install=None, over=False):
#	if KEEPTRAKT == 'true':
#		traktit.autoUpdate('all')
#		wiz.setS('traktlastsave', str(THREEDAYS))
#	if KEEPREAL == 'true':
#		debridit.autoUpdate('all')
#		wiz.setS('debridlastsave', str(THREEDAYS))
	if KEEPLOGIN == 'true':
		loginit.autoUpdate('all')
		wiz.setS('loginlastsave', str(THREEDAYS))
	if over == True: yes_pressed = 1
	elif install == 'restore': yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Restablecer la configuracion de Kodi a valores iniciales" % COLOR2, "", "ANTES de restaurar su copia de seguridad?[/COLOR]", nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]', yeslabel='[B][COLOR green]Continuar[/COLOR][/B]')
	elif install: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Restablecer la configuracion de Kodi" % COLOR2, "a valores iniciales", "Antes de instalar [COLOR %s]%s[/COLOR]?" % (COLOR1, install), nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]', yeslabel='[B][COLOR green]Continuar[/COLOR][/B]')
	else: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Restablecer la configuracion de Kodi" % COLOR2, "a valores iniciales?[/COLOR]", nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]', yeslabel='[B][COLOR green]Continuar[/COLOR][/B]')
	if yes_pressed:
		if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
			skin = 'skin.confluence' if KODIV < 17 else 'skin.estuary'

			skinSwitch.swapSkins(skin)
			x = 0
			xbmc.sleep(1000)
			while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
				x += 1
				xbmc.sleep(200)
				wiz.ebi('SendAction(Select)')
			if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
				wiz.ebi('SendClick(11)')
			else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Skin Swap Timed Out![/COLOR]' % COLOR2); return False
			xbmc.sleep(1000)
		if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Skin Swap Failed![/COLOR]' % COLOR2)
			return
		wiz.addonUpdates('set')
		xbmcPath=os.path.abspath(HOME)
		DP.create(ADDONTITLE,"[COLOR %s]Calculating files and folders" % COLOR2,'', 'Please Wait![/COLOR]')
		total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)]); del_file = 0
		DP.update(0, "[COLOR %s]Gathering Excludes list." % COLOR2)
		EXCLUDES.append('My_Builds')
		EXCLUDES.append('archive_cache')
#		if KEEPREPOS == 'true':
#			repos = glob.glob(os.path.join(ADDONS, 'repo*/'))
#			for item in repos:
#				repofolder = os.path.split(item[:-1])[1]
#				if not repofolder == EXCLUDES:
#					EXCLUDES.append(repofolder)
#		if KEEPSUPER == 'true':
#			EXCLUDES.append('plugin.program.super.favourites')
#		if KEEPWHITELIST == 'true':
#			pvr = ''
#			whitelist = wiz.whiteList('read')
#			if len(whitelist) > 0:
#				for item in whitelist:
#					try: name, id, fold = item
#					except: pass
#					if fold.startswith('pvr'): pvr = id 
#					depends = dependsList(fold)
#					for plug in depends:
#						if not plug in EXCLUDES:
#							EXCLUDES.append(plug)
#						depends2 = dependsList(plug)
#						for plug2 in depends2:
#							if not plug2 in EXCLUDES:
#								EXCLUDES.append(plug2)
#					if not fold in EXCLUDES:
#						EXCLUDES.append(fold)
#				if not pvr == '': wiz.setS('pvrclient', fold)
		if wiz.getS('pvrclient') == '':
			for item in EXCLUDES:
				if item.startswith('pvr'):
					wiz.setS('pvrclient', item)
		DP.update(0, "[COLOR %s]Clearing out files and folders:" % COLOR2)
		latestAddonDB = wiz.latestDB('Addons')
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in files:
				del_file += 1
				fold = root.replace('/','\\').split('\\')
				x = len(fold)-1
				if name == 'sources.xml' and fold[-1] == 'userdata' and KEEPSOURCES == 'true': wiz.log("Guardar Fuentes: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'favourites.xml' and fold[-1] == 'userdata' and KEEPFAVS == 'true': wiz.log("Guardar Favoritos: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'profiles.xml' and fold[-1] == 'userdata' and KEEPPROFILES == 'true': wiz.log("Guardar Perfil: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name == 'advancedsettings.xml' and fold[-1] == 'userdata' and KEEPADVANCED == 'true':  wiz.log("Guardar AdvancedSettings: %s" % os.path.join(root, name), xbmc.LOGNOTICE)
				elif name in LOGFILES: wiz.log("Guardar Log File: %s" % name, xbmc.LOGNOTICE)
				elif name.endswith('.db'):
					try:
						if name == latestAddonDB and KODIV >= 17: wiz.log("Ignorar %s on v%s" % (name, KODIV), xbmc.LOGNOTICE)
						else: os.remove(os.path.join(root,name))
					except Exception, e: 
						if not name.startswith('Textures13'):
							wiz.log('Fallo al Borrar, Purging DB', xbmc.LOGNOTICE)
							wiz.log("-> %s" % (str(e)), xbmc.LOGNOTICE)
							wiz.purgeDb(os.path.join(root,name))
				else:
					DP.update(int(wiz.percentage(del_file, total_files)), '', '[COLOR %s]File: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '')
					try: os.remove(os.path.join(root,name))
					except Exception, e: 
						wiz.log("Error removing %s" % os.path.join(root, name), xbmc.LOGNOTICE)
						wiz.log("-> / %s" % (str(e)), xbmc.LOGNOTICE)
			if DP.iscanceled(): 
				DP.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelado[/COLOR]" % COLOR2)
				return False
		for root, dirs, files in os.walk(xbmcPath,topdown=True):
			dirs[:] = [d for d in dirs if d not in EXCLUDES]
			for name in dirs:
				DP.update(100, '', 'Cleaning Up Empty Folder: [COLOR %s]%s[/COLOR]' % (COLOR1, name), '')
				if name not in ["Database","userdata","temp","addons","addon_data"]:
					shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
			if DP.iscanceled(): 
				DP.close()
				wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelado[/COLOR]" % COLOR2)
				return False
		DP.close()
		wiz.clearS('build')
		if over == True:
			return True
		elif install == 'restore': 
			return True
		elif install: 
			buildWizard(install, 'normal', over=True)
		else:
			if INSTALLMETHOD == 1: todo = 1
			elif INSTALLMETHOD == 2: todo = 0
			else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Quieres [COLOR %s]Forzar salida[/COLOR]de kodi o [COLOR %s]Recargar Pefil[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Recargar Pefil[/COLOR][/B]", nolabel="[B][COLOR green]Forzar salida[/COLOR][/B]")
			if todo == 1: wiz.reloadFix('fresh')
			else: wiz.addonUpdates('reset'); wiz.killxbmc(True)
	else: 
		if not install == 'restore':
			wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Cancelado![/COLOR]' % COLOR2)
			wiz.refresh()

def clearCache():
	if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Deseas Borrar cache?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]No, Cancelar[/COLOR][/B]', yeslabel='[B][COLOR green]Borrar Cache[/COLOR][/B]'):
		wiz.clearCache()
		#clearThumb()

def totalClean():
	if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Deseas borrar cache, packages y thumbnails?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]Cancelar Proceso[/COLOR][/B]',yeslabel='[B][COLOR green]Borrar TODO[/COLOR][/B]'):
		wiz.clearCache()
		wiz.clearPackages('total')
		clearThumb('total')

def clearThumb(type=None):
	latest = wiz.latestDB('Textures')
	if not type == None: choice = 1
	else: choice = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Deseas borrar Thumbnails %s y carpetas de iconos?' % (COLOR2, latest), "Se regeneraran al siguiente inicio[/COLOR]", nolabel='[B][COLOR red]No borrar[/COLOR][/B]', yeslabel='[B][COLOR green]Borrar Thumbs[/COLOR][/B]')
	if choice == 1:
		try: wiz.removeFile(os.join(DATABASE, latest))
		except: wiz.log('Fallo al borrar, Purging DB.'); wiz.purgeDb(latest)
		wiz.removeFolder(THUMBS)
		#if not type == 'total': wiz.killxbmc()
	else: wiz.log('Borrar thumbnames cancelado')
	wiz.redoThumbs()

def purgeDb():
	DB = []; display = []
	for dirpath, dirnames, files in os.walk(HOME):
		for f in fnmatch.filter(files, '*.db'):
			if f != 'Thumbs.db':
				found = os.path.join(dirpath, f)
				DB.append(found)
				dir = found.replace('\\', '/').split('/')
				display.append('(%s) %s' % (dir[len(dir)-2], dir[len(dir)-1]))
	if KODIV >= 16: 
		choice = DIALOG.multiselect("[COLOR %s]Selecciona DB a eliminar[/COLOR]" % COLOR2, display)
		if choice == None: wiz.LogNotify("[COLOR %s]Elimina Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelado[/COLOR]" % COLOR2)
		elif len(choice) == 0: wiz.LogNotify("[COLOR %s]Elimina Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelado[/COLOR]" % COLOR2)
		else: 
			for purge in choice: wiz.purgeDb(DB[purge])
	else:
		choice = DIALOG.select("[COLOR %s]Selecciona DB a eliminar[/COLOR]" % COLOR2, display)
		if choice == -1: wiz.LogNotify("[COLOR %s]Elimina Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelado[/COLOR]" % COLOR2)
		else: wiz.purgeDb(DB[purge])



def addDir(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
	u = sys.argv[0]
	if not mode == None: u += "?mode=%s" % urllib.quote_plus(mode)
	if not name == None: u += "&name="+urllib.quote_plus(name)
	if not url == None: u += "&url="+urllib.quote_plus(url)
	ok=True
	if themeit: display = themeit % display
	liz=xbmcgui.ListItem(display, iconImage="DefaultFolder.png", thumbnailImage=icon)
	liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
	liz.setProperty( "Fanart_Image", fanart )
	if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]

		return param

		

				
def speedMenu():
	xbmc.executebuiltin('Runscript("special://home/addons/plugin.program.ADVSet/speedtest.py")')		
		
		
		
params=get_params()
url=None
name=None
mode=None

try:     mode=urllib.unquote_plus(params["mode"])
except:  pass
try:     name=urllib.unquote_plus(params["name"])
except:  pass
try:     url=urllib.unquote_plus(params["url"])
except:  pass

def setView(content, viewType):
	if wiz.getS('auto-view')=='true':
		views = wiz.getS(viewType)
		if views == '50' and KODIV >= 17 and SKIN == 'skin.estuary': views = '55'
		if views == '500' and KODIV >= 17 and SKIN == 'skin.estuary': views = '50'
		wiz.ebi("Container.SetViewMode(%s)" %  views)

if   mode==None             : index()

#elif mode=='wizardupdate'   : wiz.wizardUpdate()
#elif mode=='builds'         : buildMenu()
#elif mode=='viewbuild'      : viewBuild(name)
#elif mode=='buildinfo'      : buildInfo(name)
#elif mode=='buildpreview'   : buildVideo(name)
#elif mode=='install'        : buildWizard(name, url)
#elif mode=='theme'          : buildWizard(name, mode, url)
#elif mode=='viewthirdparty' : viewThirdList(name)
#elif mode=='installthird'   : thirdPartyInstall(name, url)
#elif mode=='editthird'      : editThirdParty(name); wiz.refresh()


elif mode=='maint'          : maintMenu(name)
elif mode=='kodi17fix'      : wiz.kodi17Fix()
elif mode=='advancedsetting': advancedWindow(name)
elif mode=='autoadvanced'   : showAutoAdvanced(); wiz.refresh()
elif mode=='removeadvanced' : removeAdvanced(); wiz.refresh()
elif mode=='asciicheck'     : wiz.asciiCheck()
elif mode=='backupbuild'    : wiz.backUpOptions('build')
elif mode=='backupgui'      : wiz.backUpOptions('guifix')
elif mode=='backuptheme'    : wiz.backUpOptions('theme')
elif mode=='backupaddon'    : wiz.backUpOptions('addondata')
elif mode=='oldThumbs'      : wiz.oldThumbs()
elif mode=='clearbackup'    : wiz.cleanupBackup()
elif mode=='convertpath'    : wiz.convertSpecial(HOME)
elif mode=='currentsettings': viewAdvanced()
elif mode=='fullclean'      : totalClean(); wiz.refresh()
elif mode=='clearcache'     : clearCache(); wiz.refresh()
elif mode=='clearpackages'  : wiz.clearPackages(); wiz.refresh()
elif mode=='clearcrash'     : wiz.clearCrash(); wiz.refresh()
elif mode=='clearthumb'     : clearThumb(); wiz.refresh()
elif mode=='checksources'   : wiz.checkSources(); wiz.refresh()
elif mode=='checkrepos'     : wiz.checkRepos(); wiz.refresh()
elif mode=='freshstart'     : freshStart()
elif mode=='forceupdate'    : wiz.forceUpdate()
elif mode=='forceprofile'   : wiz.reloadProfile(wiz.getInfo('System.ProfileName'))
elif mode=='forceclose'     : wiz.killxbmc()
elif mode=='forceskin'      : wiz.ebi("ReloadSkin()"); wiz.refresh()
elif mode=='hidepassword'   : wiz.hidePassword()
elif mode=='unhidepassword' : wiz.unhidePassword()
elif mode=='enableaddons'   : enableAddons()
elif mode=='toggleaddon'    : wiz.toggleAddon(name, url); wiz.refresh()
elif mode=='togglecache'    : toggleCache(name); wiz.refresh()
elif mode=='toggleadult'    : wiz.toggleAdult(); wiz.refresh()
elif mode=='changefeq'      : changeFeq(); wiz.refresh()
elif mode=='uploadlog'      : uploadLog.Main()
elif mode=='viewlog'        : LogViewer()
elif mode=='viewwizlog'     : LogViewer(WIZLOG)
elif mode=='viewerrorlog'   : errorChecking(all=True)
elif mode=='clearwizlog'    : f = open(WIZLOG, 'w'); f.close(); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Wizard Log Cleared![/COLOR]" % COLOR2)
elif mode=='purgedb'        : purgeDb()
elif mode=='fixaddonupdate' : fixUpdate()
elif mode=='removeaddons'   : removeAddonMenu()
elif mode=='removeaddon'    : removeAddon(name)
elif mode=='removeaddondata': removeAddonDataMenu()
elif mode=='removedata'     : removeAddonData(name)
elif mode=='resetaddon'     : total = wiz.cleanHouse(ADDONDATA, ignore=True); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Addon_Data reset[/COLOR]" % COLOR2)
elif mode=='systeminfo'     : systemInfo()
elif mode=='restorezip'     : restoreit('build')
elif mode=='restoregui'     : restoreit('gui')
elif mode=='restoreaddon'   : restoreit('addondata')
elif mode=='restoreextzip'  : restoreextit('build')
elif mode=='restoreextgui'  : restoreextit('gui')
elif mode=='restoreextaddon': restoreextit('addondata')
elif mode=='writeadvanced'  : writeAdvanced(name, url)


elif mode=='addons'         : addonMenu(name)
elif mode=='addoninstall'   : addonInstaller(name, url)

elif mode=='savedata'       : saveMenu()
elif mode=='togglesetting'  : wiz.setS(name, 'false' if wiz.getS(name) == 'true' else 'true'); wiz.refresh()
elif mode=='managedata'     : manageSaveData(name)
elif mode=='whitelist'      : wiz.whiteList(name)



elif mode=='login'          : loginMenu()
elif mode=='savelogin'      : loginit.loginIt('update',      name)
elif mode=='restorelogin'   : loginit.loginIt('restore',     name)
elif mode=='addonlogin'     : loginit.loginIt('clearaddon',  name)
elif mode=='clearlogin'     : loginit.clearSaved(name)
elif mode=='authlogin'      : loginit.activateLogin(name); wiz.refresh()
elif mode=='updatelogin'    : loginit.autoUpdate('all')
elif mode=='importlogin'    : loginit.importlist(name); wiz.refresh()

elif mode=='contact'        : notify.contact(CONTACT)
elif mode=='settings'       : wiz.openS(name); wiz.refresh()
elif mode=='opensettings'   : id = eval(url.upper()+'ID')[name]['plugin']; addonid = wiz.addonId(id); addonid.openSettings(); wiz.refresh()



elif mode=='UNZIPROM'       : UNZIPROM()
elif mode=='viewIP'         : viewIP()
elif mode=='net'            : net_tools()
elif mode=='speed'          : speedMenu()

xbmcplugin.endOfDirectory(int(sys.argv[1]))#')