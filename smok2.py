from notify_run import Notify
from time import time
from datetime import date, time, datetime, timedelta
#-------------------------------CONST------------------------------------
H_MATIN = time(6, 0, 0)
H_MIDI = time(11, 0, 0)
H_SOIR = time(16, 20, 0)
H_FDJ = time(21, 0, 0)

MATIN_MAX = 4
MIDI_MAX = 3
SOIR_MAX = 4

TIME_INTERVAL_1 = timedelta(hours = 1)
TIME_INTERVAL_2 = timedelta(hours = 1, minutes = 30)
TIME_INTERVAL_3_H_delta = timedelta(hours = 2)
TIME_INTERVAL_3_min_delta = timedelta(minutes= 30)
TIME_INTERVAL_3_H = 2    #int
TIME_INTERVAL_3_min = 30 #int

def rst(theTime, theDate):
    with open("recording.txt", "w+") as f:
        f.writelines(['0', '\n', str(theTime), '\n', str(theDate)])   
        f.close() 

def recEntry(bowlFaits, nextOk, derniereDate):
    with open("recording.txt", "w+") as f:
        f.writelines([str(bowlFaits), '\n', str(nextOk), '\n', str(derniereDate)])   
        f.close()
def readFile():
    f = open("recording.txt", "r")
    rawLines = f.readlines()
    f.close()

    lines = [' '] * 3
    for i in range(len(rawLines)):
        lines[i] = rawLines[i].replace('\n', '')
    return lines

#-----------------------------INIT NOTIFY RUN-------------------------------
notify = Notify(endpoint="https://notify.run/8s3R8EcV6SgLMbYvfKSl")
#--------------------------INIT DATETIME VARS-------------------------------
currentTime = datetime.now()
rawTheTime = currentTime.time()
theTime = time(int(rawTheTime.strftime("%H")), int(rawTheTime.strftime("%M")), int(rawTheTime.strftime("%S")))
rawTheDate = currentTime.date()
theDate = date(int(rawTheDate.strftime("%Y")), int(rawTheDate.strftime("%m")), int(rawTheDate.strftime("%d")))
#---------------------------INIT FILE--------------------------------------
print(H_MATIN,H_MIDI, H_SOIR, H_FDJ)
print("Smoke v.2")
print("")
lines = readFile() #lecture fichier
#derniereDate traitement
#print('Processing date...')
derniereDate = datetime.strptime(lines[2], "%Y-%m-%d").date()

if (derniereDate < theDate) and (H_MATIN <= theTime < H_MIDI):#si ancien jour dans recording.txt le matin
    print('Bon matin!')
    derniereDate = theDate
    rst('', derniereDate)
    
print('Temps: ', derniereDate, ' à ', theTime) 

#print(lines)

#bowlFaits traitement
bowlFaits = int(lines[0])

if H_MATIN <= theTime < H_MIDI:
    tempsJour = 'matin'
    bowlRestant = MATIN_MAX - bowlFaits
elif H_MIDI <= theTime < H_SOIR:
    tempsJour = 'midi'
    bowlRestant =  MIDI_MAX - bowlFaits
elif H_SOIR <= theTime < H_FDJ:
    tempsJour= 'soir'
    bowlRestant =  SOIR_MAX - bowlFaits
elif (H_FDJ <= theTime) or (theTime < H_MATIN):
    tempsJour = 'nuit'
    bowlRestant = 0
else:
    print('erreur theTime')
print("C'est le ", tempsJour, ', ', theTime)
print("Bowl(s) restant(s): ", bowlRestant)

if bowlFaits > 0:
    prochainBowlH = datetime.strptime(lines[1], "%H:%M:%S").time()
    print ('Prochain bowl à : ', prochainBowlH)
#-----------------------------INPUT-----------------------------------------
if ((tempsJour == 'matin') or (tempsJour == 'midi') or (tempsJour == 'soir')) and (bowlFaits == 0):
    print ('1 bowl disponible mtn')
    choix = input('Debut periode maintenant? (yes/no)>')
elif (theTime >= prochainBowlH) and (bowlFaits < MATIN_MAX) and (tempsJour == 'matin'):#bowl cap nb par periode
    print ('1 bowl disponible mtn')
    choix = input('Bowl matin maintenant? (yes/no)>')
elif (theTime >= prochainBowlH) and (bowlFaits < MIDI_MAX) and (tempsJour == 'midi'):#bowl cap nb par periode
    print ('1 bowl disponible mtn')
    choix = input('Bowl midi maintenant? (yes/no)>')
elif (theTime >= prochainBowlH) and (bowlFaits < SOIR_MAX) and (tempsJour == 'soir'):#bowl cap nb par periode
    print ('1 bowl disponible mtn')
    choix = input('Bowl soir maintenant? (yes/no)>')
elif (tempsJour == 'soir') and (bowlFaits == SOIR_MAX):
    print ('1 bowl disponible mtn')
    choix = input('Dernier bowl du soir maintenant? (yes/no)>')
elif tempsJour == 'nuit':
    print("C'est la nuit :)")
    choix = 'no'
elif theTime < prochainBowlH:
    print ('Prochain bowl à : ', prochainBowlH)
    choix = 'no'
else:
    print('Erreur choix')
#--------------------------TRAITEMENT POST INPUT-----------------------------
if choix == 'no':
    print('Pas maintenant')
    exit()
if choix == 'yes':
    bowlFaits += 1
    bowlRestant -= 1
    print('+1 bowl (0,33g)')
    prochainBowlH = time() #changement de valeur de lheure du prochain bowl
    if (bowlFaits - 1) == 0:#-1 pour iter avant, interval 1
        prochainBowlHraw = (currentTime + TIME_INTERVAL_1).time()
        prochainBowlH = time(int(prochainBowlHraw.strftime("%H")), int(prochainBowlHraw.strftime("%M")), int(prochainBowlHraw.strftime("%S"))) # enleve deci
        
        print ('prochain bowl (interval 1h) :', prochainBowlH)
    elif (tempsJour == 'soir') and (bowlFaits == SOIR_MAX):
        prochainBowlH = ''
        print ('Dernier. Bonne nuit')
    elif (bowlFaits - 1) > 0:#interval 2
        prochainBowlHraw = (currentTime + TIME_INTERVAL_2).time()
        prochainBowlH = time(int(prochainBowlHraw.strftime("%H")), int(prochainBowlHraw.strftime("%M")), int(prochainBowlHraw.strftime("%S"))) # enleve deci
        
        if (tempsJour == 'matin') and (prochainBowlH > H_MIDI):
            bowlFaits = 0
            prochainBowlH = H_MIDI
        elif (tempsJour == 'midi') and (prochainBowlH > H_SOIR):
            bowlFaits = 0
            prochainBowlH = H_SOIR
        elif (tempsJour == 'soir') and (prochainBowlH > H_FDJ):
            bowlFaits = 0
            prochainBowlH = H_FDJ
        
        print ('prochain bowl (interval 1h30):', prochainBowlH)
    recEntry(bowlFaits, prochainBowlH, derniereDate)
    exit()
