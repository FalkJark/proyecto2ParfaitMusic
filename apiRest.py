#import framework
from flask import Flask,jsonify,request
from flask_cors import CORS,cross_origin

#import classes
from cUser import User
from cTest import colors
from cTest import prueba
from cSong import Song
from cComents import Coment
from cPlaylist import Playlist
from cRequest import Request

#Global variables
IdForRequest = 3
IdForPlaylist = 2
IdForComents = 2
IdForSongs = 5

# create API
app = Flask(__name__)
CORS(app)

# ----------------------------------------------- Test Connection ---------------------------------------------
@app.route('/ping')
def test():
    return jsonify('Pong')

#Test Colors
@app.route('/colores')
def getPaint():
    #return jsonify(prueba)
    return jsonify(colors)

# ------------------------------------------------- REQUEST -----------------------------------------------------
@app.route('/request')
def getRequest():
    #return jsonify(prueba)
    return jsonify(Request)

@app.route('/request/add', methods=["POST"])
def addOneRequest():
    global IdForRequest
    newId = IdForRequest
    IdForRequest = IdForRequest + 1
    
    req = request.get_json()
    newElePlay = {
        'id_request': newId,
        'user' : req['user'],
        'name' : req['name'],
        'image': req['image'],
        'artist': req['artist'],
        'album':req['album'],
        'year':req['year'],
        'spotify':req['spotify'],
        'youtube':req['youtube']
    }
    jsonify(newElePlay)
    Request.append(newElePlay)
    ans = 'todo bien'
    return jsonify({'answer':ans})

@app.route('/request/delete',methods=['DELETE'])
def deleteRequest():
    req = request.get_json()
    idReq = req['id']
    stock = [i for i in Request if str(i['id_request']) == idReq]
    if (len(stock) > 0):
        Request.remove(stock[0])
        ans = 'ok'
        desk = 'Song deleted'
    else:
        ans = 'null'
        desk = 'no existe la solicitud'
    return jsonify({'ans':ans,'desk':desk})

@app.route('/request/accept',methods=['POST'])
def acceptRequest():
    global IdForSongs
    newId= IdForSongs
    IdForSongs = IdForSongs + 1
    req = request.get_json()
    idReq = req['id']
    stock = [i for i in Request if str(i['id_request']) == idReq]
    if (len(stock) > 0):
        newSong = {
            'id': newId,
            'name':stock[0]['name'],
            'artist' : stock[0]['artist'],
            'album' : stock[0]['album'],
            'year' : stock[0]['year'],
            'image' : stock[0]['image'],
            'spotify' : stock[0]['spotify'],
            'youtube' : stock[0]['youtube']
        }
        #print(stock[0]['name'])
        print("new Id: ",newId)
        jsonify(newSong)
        Song.append(newSong)
        ans = 'ok'
        desk = 'Song added'
    else:
        ans = 'null'
        desk = 'no existe la solicitud'
    return jsonify({'ans':ans,'desk':desk})
# ------------------------------------------------- PLAYLIST -----------------------------------------------------

@app.route('/playlist')
def getAllPlaylist():
    #return jsonify(prueba)
    return jsonify(Playlist)

@app.route('/playlist', methods=['POST'])
def getPlaylist():
    req = request.get_json()
    nickName = req['user']
    stock = [i for i in Playlist if str(i['user']) == nickName]
    if (len(stock) > 0):
        ans = stock
        desk = 'Return all coments with compatibility id'
    else:
        ans = 'null'
        desk = 'No aun no tienes ninguna cancion guardada'
    return jsonify({'answer':ans,'desc':desk})


@app.route('/playlist/add', methods=["POST"])
def addOneElementPlaylist():
    req = request.get_json()
    global IdForPlaylist
    newId = IdForPlaylist
    IdForPlaylist = IdForPlaylist + 1
    IdS = req['id']
    userPlay = req['user']
    songToWork = [i for i in Song if str(i['id']) == IdS]
    if (len(songToWork) > 0):
        for j in Playlist:
            if j['idSong'] == int(IdS) and j['user'] == userPlay:
                ans = 'null'
                desc = 'La canción ya está en Playlist'
                print('pasa por el if')
                break
        else:
            newElePlay = {
                'id': newId,
                'idSong':int(songToWork[0]['id']),
                'user' : userPlay,
                'name' : songToWork[0]['name'],
                'artist': songToWork[0]['artist'],
                'album':songToWork[0]['album'],
                'year':songToWork[0]['year'],
                'spotify':songToWork[0]['spotify'],
                'youtube':songToWork[0]['youtube']
            }
            jsonify(newElePlay)
            Playlist.append(newElePlay)
            ans = 'ok'
            desc = 'Canción agregarda a tu lista'
    else: 
        ans = 'null'
        desc = 'Song not found'

    return jsonify({'answer':ans,'desc':desc})

#---------------------------------------------------- COMENTS ---------------------------------------------------

@app.route('/coments/particular', methods=['POST'])
def getSomeComents():
    req = request.get_json()
    idSong = req['id']
    stock = [i for i in Coment if str(i['idSong']) == idSong]
    if (len(stock) > 0):
        ans = stock
        desk = 'Return all coments with compatibility id'
    else:
        ans = 'null'
        desk = 'something go wrong'
    return jsonify({'answer':ans,'desc':desk})


@app.route('/coments/add', methods=["POST"])
def addOneComent():
    req = request.get_json()
    global IdForComents
    newId = IdForComents
    IdForComents = IdForComents + 1 
    newComent = {
        'id': newId,
        'idSong':int(req['idSong']),
        'user' : req['user'],
        'text' : req['text'],
    }
    jsonify(newComent)
    Coment.append(newComent)
    ans = 'todo bien'
    return jsonify({'answer':ans})

@app.route('/coments')
def getAllComents():
    return jsonify(Coment)

#---------------------------------------------------- SONGS ---------------------------------------------------

@app.route('/songs')
def getAllSongs():
    return jsonify(Song)


@app.route('/songs/register', methods=["POST"])
def addOneSong():
    global IdForSongs
    newId= IdForSongs
    IdForSongs = IdForSongs + 1
    
    req = request.get_json()
    newSong = {
        'id': newId,
        'name':req['name'],
        'artist' : req['artist'],
        'album' : req['album'],
        'year' : req['year'],
        'image' : req['image'],
        'spotify' : req['spotify'],
        'youtube' : req['youtube']
    }
    jsonify(newSong)
    Song.append(newSong)
    ans = 'todo bien'
    return jsonify({'answer':ans})

@app.route('/songs/delete',methods=['DELETE'])
def deleteSong():
    req = request.get_json()
    idSong = req['id']
    stock = [i for i in Song if str(i['id']) == idSong]
    if (len(stock) > 0):
        for j in Playlist:
            if j['idSong'] == int(idSong):
                Playlist.remove(j)

        Song.remove(stock[0])
        ans = 'ok'
        desk = 'Song deleted'
    else:
        ans = 'null'
        desk = 'no existe la cancion'
    return jsonify({'ans':ans,'desk':desk})

@app.route('/songs/getOne',methods=['POST'])
def getOneSong():
    req = request.get_json()
    idSong = req['id']
    stock = [i for i in Song if str(i['id']) == idSong]
    if (len(stock) > 0):
        print(stock)
        ans = stock[0]
        desk = 'Information'
    else:
        ans = 'null'
        desk = 'no existe la cancion'
    return jsonify({'answer':ans,'desk':desk})

@app.route('/songs/modify', methods=["PUT"])
def modifySong():
    req = request.get_json()
    oldId = req['id']
    print(oldId)
    stock = [i for i in Song if str(i['id']) == oldId]
    print('esto es stock',stock)
    if (len(stock) > 0):
        
        stock[0]['name'] = req['name']
        stock[0]['artist'] = req['artist']
        stock[0]['album'] = req['album']
        stock[0]['image'] = req['image']
        stock[0]['year'] = req['year']
        stock[0]['spotify'] = req['spotify']
        stock[0]['youtube'] = req['youtube']
        ans = 'ok'
        desk = 'todo bien'    
    else:
        print('pasa por el else')
        ans = 'null'
        desk = 'La cancion no existe'
    return jsonify({'answer':ans,'desc':desk})
        

#---------------------------------------------------- USERS ---------------------------------------------------

@app.route('/users')
def getAllUsers():
    return jsonify(User)

@app.route('/users/delete',methods=['DELETE'])
def deleteUser():
    req = request.get_json()
    nick = req['nickName']
    stock = [i for i in User if i['nickName'] == nick]
    if (len(stock) > 0):
        User.remove(stock[0])
        ans = 'ok'
        desk = 'User deleted'
    else:
        ans = 'null'
        desk = 'no existe el producto'
    return jsonify({'ans':ans,'desk':desk})


@app.route('/users/modify', methods=["PUT"])
def modifyUser():
    req = request.get_json()
    oldN = req['oldNick']
    newN = req['nickName']
    if oldN != newN:
        stock = [i for i in User if i['nickName'] == newN]
        if (len(stock) > 0):
            ans = 'null'
            desk = 'el nombre de usuario ya existe'
        else:
            stock2 = [j for j in User if j['nickName'] == oldN]
            stock2[0]['name'] = req['name']
            stock2[0]['lastName'] = req['lastName']
            stock2[0]['nickName'] = req['nickName']
            stock2[0]['password'] = req['password']
            stock2[0]['type'] = req['type']
            ans = stock2[0]
            desk = 'todo bien'
    else:
        stock3 = [k for k in User if k['nickName'] == oldN]
        stock3[0]['name'] = req['name']
        stock3[0]['lastName'] = req['lastName']
        #stock3[0]['nickName'] = req['nickName']
        stock3[0]['password'] = req['password']
        stock3[0]['type'] = req['type']
        ans = stock3[0]
        desk = 'todo bien, eran iguales'
    return jsonify({'answer':ans,'desc':desk})


@app.route('/users/register', methods=["POST"])
def addOneUser():
    req = request.get_json()
    nick = req['nickName'] 
    for i in User:
        if i['nickName'] == nick:
            ans =  'El usuario ya esta registrado'
            break
        else:
            ans = 'ok'
    if ans == 'ok':
        User.append(req)
    return jsonify({'answer':ans})


@app.route('/users/recoverPass', methods=["POST"])
def recoverPass():
    req = request.get_json()
    value = req['nickName']
    for i in User:
        if i['nickName'] == value:
            ans = i['password']
            break
        else:
            ans = 'null' 
    return jsonify({"answer":ans})


@app.route('/users/login', methods=["POST"])
def login():
    req = request.get_json()
    nick = req['nickName']
    pass1 = req['password']
    for i in User:
        if i['nickName'] == nick and i['password'] == pass1:
            #ans = i['nickName']
            ans = i
            break
        else:
            ans = 'null'
    return jsonify({'answer': ans})


#---------------------------------------------------- WITGETS ---------------------------------------------------

# run app, define port and activate debug mode
if __name__ == "__main__":
    app.run(threaded=True,host="0.0.0.0",port=5000,debug=True)
