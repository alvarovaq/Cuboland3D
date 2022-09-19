import ctypes, math, copy, sys, os, time, random, threading, socket, pickle
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

def TamPantalla () :

	user32 = ctypes.windll.user32
	user32.SetProcessDPIAware()
	ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
	return ancho, alto

class Model :

	def __init__ (self,file=None) :

		self.batch = pyglet.graphics.Batch()
		self.cubes = CubeHandler(self.batch)

		if not file : self.make_model()
		else : self.read_model(file)

	def make_model (self) :

		for x in range(20) :
			for z in range(20) :
				self.cubes.add((x,0,-z),(200,200,200),255)

		self.update_cubes()

	def save_model (self,file) :

		cubes = []
		for cube in self.cubes.cubes.values() :
			cubes.append((cube.p,cube.c,cube.o))
		arch = open(file, "wb")
		pickle.dump(cubes, arch)
		arch.close()

	def read_model (self,file) :

		arch = open(file, "ab+")
		arch.seek(0)
		try :
			cubes = pickle.load(arch)
			for cube in cubes :
				self.cubes.add(cube[0],cube[1],cube[2])
			self.update_cubes()
		except :
			print("[ERROR] El proyecto no funciona o no se ha encontrado.")
			print("Creando un nuevo proyecto...")
			self.make_model()
		finally :
			arch.close()

	def update_cubes (self) :

		for cube in self.cubes.cubes.values() : self.cubes.update_cube(cube)

	def update (self,dt) :

		pass

	def draw (self) :

		self.batch.draw()

class Cube :

	def __init__ (self,p,c,o) :

		self.p,self.c,self.o = p,c,o
		self.shown = {'left':False,'right':False,'bottom':False,'top':False,'back':False,'front':False}
		self.faces = {'left':None,'right':None,'bottom':None,'top':None,'back':None,'front':None}

class CubeHandler :

	def __init__ (self,batch) :

		self.batch = batch
		self.cubes = {}

	def hit_test (self,p,vec,dist=256) :

		m = 8; x,y,z = p; dx,dy,dz = vec
		dx/=m; dy/=m; dz/=m; prev=None

		for i in range(dist*m) :
			key = normalize((x,y,z))
			if key in self.cubes: return key,prev
			prev = key
			x,y,z = x+dx,y+dy,z+dz
		return None, None

	def show (self,v,c) : 

		return (self.batch.add(2,GL_LINES,None,('v3f',(v[0],v[1],v[2], v[3],v[4],v[5])),('c3B',(0,0,0, 0,0,0))),
			self.batch.add(2,GL_LINES,None,('v3f',(v[3],v[4],v[5], v[6],v[7],v[8])),('c3B',(0,0,0, 0,0,0))),
			self.batch.add(2,GL_LINES,None,('v3f',(v[6],v[7],v[8], v[9],v[10],v[11])),('c3B',(0,0,0, 0,0,0))),
			self.batch.add(2,GL_LINES,None,('v3f',(v[9],v[10],v[11], v[0],v[1],v[2])),('c3B',(0,0,0, 0,0,0))),
			self.batch.add(4,GL_QUADS,None,('v3f/dynamic',v),('c4B',c)),)

	def update_cube (self,cube) :

		if not any(cube.shown.values()) : return
		v = cube_vertices(cube.p)
		c = cube_color(cube.c,cube.o)
		f = 'left','right','bottom','top','back','front'
		for i in (0,1,2,3,4,5) :
			if cube.shown[f[i]] :
				if not cube.faces[f[i]] : cube.faces[f[i]] = self.show(v[i],c)
			elif cube.faces[f[i]] : self.delete_face(cube.faces[f[i]]); cube.faces[f[i]] = None

	def delete_face (self,face) :

		for f in face :
			f.delete()

	def set_adj (self,cube,adj,state) :

		x,y,z = cube.p; X,Y,Z = adj; d = X-x,Y-y,Z-z; f = 'left','right','bottom','top','back','front'
		for i in (0,1,2) :
			if d[i] :
				j = i+i; a,b = [f[j+1],f[j]][::d[i]]; cube.shown[a] = state
				if not state and cube.faces[a] : self.delete_face(cube.faces[a]); cube.faces[a] = None

	def add (self,p,c,o,now=False) :

		if p in self.cubes : return
		cube = self.cubes[p] = Cube(p,c,o)

		for adj in adjacent(*cube.p) :
			if adj in self.cubes :
				self.set_adj(self.cubes[adj],cube.p,False)
			else : self.set_adj(cube,adj,True)

		if now : self.update_cube(cube)

	def remove (self,p) :

		if p not in self.cubes : return
		cube = self.cubes.pop(p)

		for side,face in cube.faces.items() :
			if face : self.delete_face(face)

		for adj in adjacent(*cube.p) :
			if adj in self.cubes :
				self.set_adj(self.cubes[adj],cube.p,True)
				self.update_cube(self.cubes[adj])

def cube_vertices (pos,n=0.5) :

	x,y,z = pos; v = tuple((x+X,y+Y,z+Z) for X in (-n,n) for Y in (-n,n) for Z in (-n,n))
	return tuple(tuple(k for j in i for k in v[j]) for i in ((0,1,3,2),(5,4,6,7),(0,4,5,1),(3,7,6,2),(4,0,2,6),(1,5,7,3)))

def cube_color (c,o) :

	return (*c,o, *c,o, *c,o, *c,o)

def flatten (lst) : return sum(map(list,lst),[])
def normalize (pos) : x,y,z = pos; return round(x),round(y),round(z)
def adjacent (x,y,z) : 
	for p in ((x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)) : yield p

class Block :

	def __init__ (self,c,o) :
		self.c,self.o = c,o

class Player :

	WALKING_SPEED = 5
	FLYING_SPEED = 15

	GRAVITY = 20
	JUMP_SPEED = (2*GRAVITY)**.5
	TERMINAL_VELOCITY = 50

	CREATIVE = True

	def push (self) : glPushMatrix(); glRotatef(-self.rot[0],1,0,0); glRotatef(self.rot[1],0,1,0); glTranslatef(-self.pos[0],-self.pos[1],-self.pos[2])

	def __init__ (self,cubes,pos=(0,0,0),rot=(0,0),draw_player=True) :

		self.batch = pyglet.graphics.Batch()
		self.init_batch()

		self.cubes = cubes
		self.pos,self.rot = list(pos),list(rot)
		self.flying = True
		self.noclip = True
		self.dy = 0

		self.death = False
		self.point_revive = copy.copy(pos)
		self.touch_color = []
		self.inventory = False
		self.pause = False
		self.Name = ''
		self.draw_player = draw_player

		self.blocks = {}
		self.blocks[1] = Block((200,200,200),255)
		self.blocks[2] = Block((200,100,100),255)
		self.blocks[3] = Block((100,200,100),255)
		self.blocks[4] = Block((100,100,200),255)
		self.blocks[5] = Block((200,100,200),255)
		self.blocks[6] = Block((200,200,100),255)
		self.blocks[7] = Block((100,200,200),255)
		self.blocks[8] = Block((100,100,100),255)
		self.block_selected = 1

	def load (self) :

		rotY = self.rot[1]*math.pi/180
		r = (0.5**2+0.5**2)**.5
		v1 = (self.pos[0]+r*math.cos(rotY+math.pi/4),self.pos[1]+1,self.pos[2]-r*math.sin(rotY+math.pi/4))
		v2 = (self.pos[0]+r*math.cos(rotY+3*math.pi/4),self.pos[1]+1,self.pos[2]-r*math.sin(rotY+3*math.pi/4))
		v3 = (self.pos[0]+r*math.cos(rotY-3*math.pi/4),self.pos[1]+1,self.pos[2]-r*math.sin(rotY-3*math.pi/4))
		v4 = (self.pos[0]+r*math.cos(rotY-math.pi/4),self.pos[1]+1,self.pos[2]-r*math.sin(rotY-math.pi/4))
		v5 = (self.pos[0]+r*math.cos(rotY+math.pi/4),self.pos[1]-1,self.pos[2]-r*math.sin(rotY+math.pi/4))
		v6 = (self.pos[0]+r*math.cos(rotY+3*math.pi/4),self.pos[1]-1,self.pos[2]-r*math.sin(rotY+3*math.pi/4))
		v7 = (self.pos[0]+r*math.cos(rotY-3*math.pi/4),self.pos[1]-1,self.pos[2]-r*math.sin(rotY-3*math.pi/4))
		v8 = (self.pos[0]+r*math.cos(rotY-math.pi/4),self.pos[1]-1,self.pos[2]-r*math.sin(rotY-math.pi/4))

		self.top.vertices = (*v1,*v2,*v3,*v4)
		self.side1.vertices = (*v1,*v2,*v6,*v5)
		self.side2.vertices = (*v2,*v3,*v7,*v6)
		self.side3.vertices = (*v3,*v4,*v8,*v7)
		self.side4.vertices = (*v4,*v1,*v5,*v8)
		self.bottom.vertices = (*v5,*v6,*v7,*v8)
		self.line1.vertices = (*v1,*v2)
		self.line2.vertices = (*v2,*v3)
		self.line3.vertices = (*v3,*v4)
		self.line4.vertices = (*v4,*v1)
		self.line5.vertices = (*v5,*v6)
		self.line6.vertices = (*v6,*v7)
		self.line7.vertices = (*v7,*v8)
		self.line8.vertices = (*v8,*v5)
		self.line9.vertices = (*v1,*v5)
		self.line10.vertices = (*v2,*v6)
		self.line11.vertices = (*v3,*v7)
		self.line12.vertices = (*v4,*v8)

	def init_batch (self) :

		c = (150,255,150)
		self.top = self.batch.add(4,GL_QUADS,None,('v3f/dynamic',(0,0,0, 0,0,0, 0,0,0, 0,0,0)),('c3B',(*c,*c,*c,*c)))
		self.side1 = self.batch.add(4,GL_QUADS,None,('v3f/dynamic',(0,0,0, 0,0,0, 0,0,0, 0,0,0)),('c3B',(*c,*c,*c,*c)))
		self.side2 = self.batch.add(4,GL_QUADS,None,('v3f/dynamic',(0,0,0, 0,0,0, 0,0,0, 0,0,0)),('c3B',(*c,*c,*c,*c)))
		self.side3 = self.batch.add(4,GL_QUADS,None,('v3f/dynamic',(0,0,0, 0,0,0, 0,0,0, 0,0,0)),('c3B',(*c,*c,*c,*c)))
		self.side4 = self.batch.add(4,GL_QUADS,None,('v3f/dynamic',(0,0,0, 0,0,0, 0,0,0, 0,0,0)),('c3B',(*c,*c,*c,*c)))
		self.bottom = self.batch.add(4,GL_QUADS,None,('v3f/dynamic',(0,0,0, 0,0,0, 0,0,0, 0,0,0)),('c3B',(*c,*c,*c,*c)))
		self.line1 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line2 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line3 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line4 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line5 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line6 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line7 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line8 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line9 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line10 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line11 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))
		self.line12 = self.batch.add(2,GL_LINES,None,('v3f/dynamic',(0,0,0, 0,0,0)),('c3B',(0,0,0, 0,0,0)))


	def draw (self) :

		if self.draw_player :self.batch.draw()

	def mouse_motion (self,dx,dy) :

		if self.pause : return

		dx/=8; dy/=8; self.rot[0]+=dy; self.rot[1]+=dx
		if self.rot[0]>90: self.rot[0] = 90
		elif self.rot[0]<-90: self.rot[0] = -90

	def jump (self,jump_speed) :
		if not self.dy : self.dy = jump_speed

	def get_sight_vector (self) :

		rotX,rotY = self.rot[0]*math.pi/180,self.rot[1]*math.pi/180
		dx,dz = math.sin(rotY),-math.cos(rotY)
		dy,m = math.sin(rotX),math.cos(rotX)
		return dx*m,dy,dz*m

	def update (self,dt,keys) :

		if self.inventory : self.pause = True
		else: self.pause = False

		if self.pause : return

		self.touch_color.clear()

		DX,DY,DZ = 0,0,0; s = dt*self.FLYING_SPEED if self.flying else dt*self.WALKING_SPEED
		rotY = self.rot[1]*math.pi/180
		dx,dz = s*math.sin(rotY),s*math.cos(rotY)
		if self.flying :
			if keys[key.LSHIFT] : DY-=s
			if keys[key.SPACE] : DY+=s
		elif keys[key.SPACE] : self.jump(self.JUMP_SPEED)
		if keys[key.W] : DX+=dx; DZ-=dz
		if keys[key.S] : DX-=dx; DZ+=dz
		if keys[key.A] : DX-=dz; DZ-=dx
		if keys[key.D] : DX+=dz; DZ+=dx

		if dt<0.2 :
			dt/=10; DX/=10; DY/=10; DZ/=10
			for i in range(10) : self.move(dt,DX,DY,DZ)

		if self.death :
			self.die()

	def on_text (self,text) :

		try :
			n = int(text)
			if n in self.blocks :
				self.block_selected = n
		except:
			return

	def move (self,dt,dx,dy,dz) :

		if not self.flying :
			self.dy -= dt*self.GRAVITY
			self.dy = max(self.dy,-self.TERMINAL_VELOCITY)
			dy += self.dy*dt

		x,y,z = self.pos
		self.pos = self.collide((x+dx,y+dy,z+dz))

	def collide (self,pos) :

		if self.noclip and self.flying : return pos
		pad = 0.25; p = list(pos); np = normalize(pos)
		for face in ((-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)) :
			for i in (0,1,2) :
				if not face[i] : continue
				d = (p[i]-np[i])*face[i]
				if d<pad : continue
				for dy in (0,1) :
					op = list(np); op[1]-=dy; op[i]+=face[i]
					if tuple(op) in self.cubes :
						self.touch_color.append(self.cubes[tuple(op)].c)
						p[i] -= (d-pad)*face[i]
						if face[1] : self.dy = 0
						break
		return tuple(p)

	def die (self) :

		self.pos = copy.copy(self.point_revive)
		self.death = False

	def collision_color (self,c) :

		return c in self.touch_color

	def color_block_selec (self) :

		return cube_color(self.blocks[self.block_selected].c,self.blocks[self.block_selected].o)

class Script_Player (Player) :

	def __init__ (self,*args,**kwargs) :

		super().__init__(*args,**kwargs)

	def script_update (self) :

		if not self.flying :
			if self.collision_color((100,200,100)) :
				self.jump(2*self.JUMP_SPEED)
			if self.collision_color((200,100,100)) :
				self.death = True

class network :

	HEADER = 248
	PORT = 7998
	SERVER = socket.gethostbyname(socket.gethostname())
	ADDR = (SERVER, PORT)
	FORMAT = 'utf-8'
	DISCONNECT_MESSAGE = "!DISCONNECT"

	def __init__ (self,model,player,players) :

		self.model = model
		self.player = player
		self.players = players

	def send (self,conn,msg) :
		message = msg.encode(self.FORMAT)
		conn.send(message)

	def read (self,conn,header=None) :
		if not header : header = self.HEADER
		while True :
			msg = conn.recv(header).decode(self.FORMAT)
			if msg : return msg

	def set_data (self,ply) : return ply.Name + "/" + str(ply.pos[0]) + ":" + str(ply.pos[1]) + ":" + str(ply.pos[2]) + "/" + str(-ply.rot[1])
	def get_data (self,ply,msg) : data=msg.split("/");p_=data[1].split(":");ply.Name=data[0];ply.pos=[float(p_[0]),float(p_[1]),float(p_[2])];ply.rot[1]=data[2]
	def get_name_data (self,msg) : data=msg.split("/"); return data[0]
	def set_data_players (self) :
		msg = ''
		for ply in self.players : msg += self.set_data(ply) + "&"
		return msg[:-1]
	def get_data_players (self,msg) :
		data=msg.split("&")
		for dt in data :
			name = self.get_name_data(dt)
			if not name in self.players : self.add_player(name)
			if name != self.player.Name : self.get_data(self.players[name],dt)

	def add_player (self,Name) : print(Name); self.players[Name] = Player(self.model.cubes.cubes); self.players[Name].Name = Name
	def delete_player (self,Name) : del self.players[Name]

class server (network) :

	def __init__ (self,*args,**kwargs) :

		super().__init__(*args,**kwargs)

	def connection (self) :

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.bind(self.ADDR)

	def init_connection (self,conn) :

		name = self.read(conn)
		self.add_player(name)

	def handle_client (self,conn,addr) :

		self.init_connection(conn)

		while True :

			data = self.read(conn); name = self.get_name_data(data); self.get_data(self.players[name],data)
			self.send(conn,self.set_data_players())

	def start (self) :

		self.connection()

		th = threading.Thread(target=self.connection_client)
		th.start()

	def connection_client (self) :

		self.server.listen()
		print(f"[LISTENING] Server is listening on {self.SERVER}")
		while True :
			conn, addr = self.server.accept()
			thread = threading.Thread(target=self.handle_client, args=(conn,addr))
			thread.start()
			print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

class client (network) :

	def __init__ (self,*args,**kwargs) :

		super().__init__(*args,**kwargs)

		self.client = None

	def init_client(self) : 
		if not self.client : self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def connection (self) : self.init_client(); self.client.connect(self.ADDR)
	def disconnect (self) : self.client.close(); self.client = None

	def init_connection (self) :

		self.connection()
		self.send(self.client,self.player.Name)

	def start (self) :

		th = threading.Thread(target=self.run)
		th.start()

	def run (self) :

		self.init_connection()

		while True :

			self.send(self.client,self.set_data(self.player))
			data = self.read(self.client); self.get_data_players(data)

def cube2d (batch,x,y,c,m) :

		v1 = (x,y+m); v2 = (x+m,y+m); v3 = (x+m,y); v4 = (x,y)
		v5 = (x+m/2,y+m+3*m/8); v6 = (x+m+m/2,y+m+3*m/8); v7 = (x+m+m/2,y+3*m/8)

		cube = [	
					batch.add(4,GL_QUADS,None,('v2f',(*v1, *v2, *v3, *v4)),('c4B/dynamic',c)),
					batch.add(4,GL_QUADS,None,('v2f',(*v5, *v6, *v2, *v1)),('c4B/dynamic',c)),
					batch.add(4,GL_QUADS,None,('v2f',(*v2, *v6, *v7, *v3)),('c4B/dynamic',c)),
					batch.add(2,GL_LINES,None,('v2f',(*v1, *v2)),('c3B',(0,0,0, 0,0,0))),
					batch.add(2,GL_LINES,None,('v2f',(*v2, *v3)),('c3B',(0,0,0, 0,0,0))),
					batch.add(2,GL_LINES,None,('v2f',(*v3, *v4)),('c3B',(0,0,0, 0,0,0))),
					batch.add(2,GL_LINES,None,('v2f',(*v4, *v1)),('c3B',(0,0,0, 0,0,0))),
					batch.add(2,GL_LINES,None,('v2f',(*v1, *v5)),('c3B',(0,0,0, 0,0,0))),
					batch.add(2,GL_LINES,None,('v2f',(*v5, *v6)),('c3B',(0,0,0, 0,0,0))),
					batch.add(2,GL_LINES,None,('v2f',(*v6, *v2)),('c3B',(0,0,0, 0,0,0))),
					batch.add(2,GL_LINES,None,('v2f',(*v6, *v7)),('c3B',(0,0,0, 0,0,0))),
					batch.add(2,GL_LINES,None,('v2f',(*v7, *v3)),('c3B',(0,0,0, 0,0,0)))
				]

		return cube

class numeric_bar :

	def __init__ (self,batch,c=(255,255,255),n_max=255) :

		self.batch = batch
		self.c,self.n_max = c,n_max

		self.bar = None

		self.ppos,self.plon = None,None
		self.selec = False
		self.npos = [None,None]
		self.nalt = None

		self.pos_mouse = (0,0)

	def load (self,n=0,pos=None,lon=None) :

		if not pos : pos = self.ppos
		if not lon : lon = self.plon

		self.ppos,self.plon = pos,lon

		self.delete()

		alt=2;col=(255,255,255);v1=(pos[0]-lon/2,pos[1]+alt);v2=(pos[0]+lon/2,pos[1]+alt);v3=(pos[0]+lon/2,pos[1]-alt);v4=(pos[0]-lon/2,pos[1]-alt)
		n_alt=alt*3;n_pos=self.get_pos(n,pos,lon);
		
		if self.selec :
			self.follow_mouse(pos,lon)
			n_pos = copy.copy(self.npos)

		n_v1=(n_pos[0]-n_alt,n_pos[1]+n_alt);n_v2=(n_pos[0]+n_alt,n_pos[1]+n_alt);n_v3=(n_pos[0]+n_alt,n_pos[1]-n_alt);n_v4=(n_pos[0]-n_alt,n_pos[1]-n_alt)

		self.bar = [
						self.batch.add(4,GL_QUADS,None,('v2f',(*v1,*v2,*v3,*v4)),('c3B',(*col,*col,*col,*col))),
						self.batch.add(4,GL_QUADS,None,('v2f',(*n_v1,*n_v2,*n_v3,*n_v4)),('c3B',(*self.c,*self.c,*self.c,*self.c)))
					]

		self.npos = copy.copy(n_pos)
		self.nalt = n_alt

		n = self.get_n(n_pos,pos,lon)

		return n

	def delete (self) :

		if self.bar :
			for b in self.bar : b.delete()
			self.bar = None

	def get_pos (self,n,pos,lon) :

		dp = lon*n/self.n_max
		return [pos[0]-lon/2+dp,pos[1]]

	def get_n (self,n_pos,pos,lon) :

		return round((n_pos[0]-(pos[0]-lon/2))*self.n_max/lon)

	def follow_mouse (self,pos,lon) :

		m = self.pos_mouse[0]

		if m < pos[0]-lon/2 :
			self.npos[0] = pos[0]-lon/2
		elif m > pos[0]+lon/2 :
			self.npos[0] = pos[0]+lon/2
		else :
			self.npos[0] = m

	def on_mouse_drag (self,x,y,dx,dy,button) :

		self.pos_mouse = (x,y)

	def on_mouse_press (self,x,y,button) :

		if self.bar :
			if button == mouse.LEFT :
				if x >= self.npos[0]-self.nalt and x <= self.npos[0]+self.nalt :
					if y >= self.npos[1]-self.nalt and y <= self.npos[1]+self.nalt:
						self.pos_mouse = (x,y)
						self.selec = True

	def on_mouse_release (self,x,y,button) :

		if self.bar :
			if self.selec : self.selec = False

class Inventory :

	def __init__ (self,bath,player) :

		self.batch = bath

		self.player = player

		self.background = None
		self.blocks = None
		self.selector = None
		self.button_color = None
		self.bar_red = numeric_bar(self.batch,c=(255,0,0),n_max=255)
		self.bar_green = numeric_bar(self.batch,c=(0,255,0),n_max=255)
		self.bar_blue = numeric_bar(self.batch,c=(0,0,255),n_max=255)
		self.bar_opacity = numeric_bar(self.batch,c=(0,0,0),n_max=255)
		self.text_color = pyglet.text.Label(text='',
                          		font_name='Times New Roman',
                          		font_size=15,
                         	 	x=0, y=0,
                         	 	anchor_x='left', anchor_y='top')

		self.px,self.py,self.pw,self.ph = None,None,None,None

	def load (self,x=None,y=None,w=None,h=None) :

		if not x : x = self.px
		if not y : y = self.py
		if not w : w = self.pw
		if not h : h = self.ph

		self.px,self.py,self.pw,self.ph = x,y,w,h

		self.delete()

		if not self.player.inventory : return

		v1 = (x-w/2,y+h/2); v2 = (x+w/2,y+h/2); v3 = (x+w/2,y-h/2); v4 = (x-w/2,y-h/2); c = (50,50,50,150)
		self.background = self.batch.add(4,GL_QUADS,None,('v2f',(*v1, *v2, *v3, *v4)),('c4B',(*c, *c, *c, *c)))

		self.blocks = []
		sep = 7; dim = len(self.player.blocks); m = 2*((w/(dim+2))-sep)/3; lg = dim*((3*m/2)+sep)
		for block in self.player.blocks :
			X,Y = x-lg/2 + (block-1)*((3*m/2)+sep),(y-h/2)+h/8; C = cube_color(self.player.blocks[block].c,self.player.blocks[block].o)
			self.blocks.append(cube2d(self.batch,X,Y,C,m))
			if block == self.player.block_selected :
				y_ = Y - 20; alt = 2.5
				s_v1 = (X,y_+alt); s_v2 = (X+3*m/2,y_+alt); s_v3 = (X+3*m/2,y_-alt); s_v4 = (X,y_-alt); col = cube_color((100,200,200),255)
				self.selector = self.batch.add(4,GL_QUADS,None,('v2f',(*s_v1, *s_v2, *s_v3, *s_v4)),('c4B', col))

		m,n = 4*w/10,h/2; bor = 5; X,Y = x-w/2+1.5*w/20,y+h/2-h/8; v1 = (X,Y); v2 = (X+m,Y); v3 = (X+m,Y-n); v4 = (X,Y-n); C = self.player.color_block_selec(); bor_c = (0,0,0)
		self.button_color = [
								self.batch.add(4,GL_QUADS,None,('v2f',(v1[0]+bor,v1[1]-bor, v2[0]-bor,v2[1]-bor, v3[0]-bor,v3[1]+bor, v4[0]+bor,v4[1]+bor)),('c4B',C)),
								self.batch.add(4,GL_QUADS,None,('v2f',(*v1, *v2, v2[0],v2[1]-bor, v1[0],v1[1]-bor)),('c3B',(*bor_c, *bor_c, *bor_c, *bor_c))),
								self.batch.add(4,GL_QUADS,None,('v2f',(*v1, v1[0]+bor,v1[1], v4[0]+bor,v4[1], *v4)),('c3B',(*bor_c, *bor_c, *bor_c, *bor_c))),
								self.batch.add(4,GL_QUADS,None,('v2f',(v2[0]-bor,v2[1], *v2, *v3, v3[0]-bor,v3[1])),('c3B',(*bor_c, *bor_c, *bor_c, *bor_c))),
								self.batch.add(4,GL_QUADS,None,('v2f',(v4[0],v4[1]+bor, v3[0],v3[1]+bor, *v3, *v4)),('c3B',(*bor_c, *bor_c, *bor_c, *bor_c))),
							]

		col = self.player.blocks[self.player.block_selected].c
		op = self.player.blocks[self.player.block_selected].o
		R = self.bar_red.load(col[0],(x+w/4,y+3*h/8-20),w/3)
		G = self.bar_green.load(col[1],(x+w/4,y+h/4-20),w/3)
		B = self.bar_blue.load(col[2],(x+w/4,y+h/8-20),w/3)
		O = self.bar_opacity.load(op,(x+w/4,y-20),w/3)
		self.player.blocks[self.player.block_selected].c = (R,G,B)
		self.player.blocks[self.player.block_selected].o = O

		self.text_color.text = str(R)+","+str(G)+","+str(B)+","+str(O)
		self.text_color.x = x - w/2 + 10
		self.text_color.y = y + h/2 - 10

	def delete (self) :

		if self.background : self.background.delete(); self.background = None
		if self.blocks :
			for block in self.blocks:
				for face in block :
					face.delete()
			self.blocks = None
		if self.selector : self.selector.delete(); self.selector = None
		if self.button_color :
			for i in self.button_color : i.delete(); self.button_color = None
		self.bar_red.delete()
		self.bar_green.delete()
		self.bar_blue.delete()
		self.bar_opacity.delete()

	def on_mouse_drag (self,x,y,dx,dy,button) :

		self.bar_red.on_mouse_drag(x,y,dx,dy,button)
		self.bar_green.on_mouse_drag(x,y,dx,dy,button)
		self.bar_blue.on_mouse_drag(x,y,dx,dy,button)
		self.bar_opacity.on_mouse_drag(x,y,dx,dy,button)

	def on_mouse_press (self,x,y,button) :

		self.bar_red.on_mouse_press(x,y,button)
		self.bar_green.on_mouse_press(x,y,button)
		self.bar_blue.on_mouse_press(x,y,button)
		self.bar_opacity.on_mouse_press(x,y,button)

	def on_mouse_release (self,x,y,button) :

		self.bar_red.on_mouse_release(x,y,button)
		self.bar_green.on_mouse_release(x,y,button)
		self.bar_blue.on_mouse_release(x,y,button)
		self.bar_opacity.on_mouse_release(x,y,button)

	def draw (self) :

		if self.player.inventory : self.text_color.draw()

class Graphics2D :

	def __init__ (self,player) :

		self.batch = pyglet.graphics.Batch()

		self.player = player

		self.reticle = None
		self.reticle_x,self.reticle_y = None,None

		self.cube = None
		self.cube_x,self.cube_y,self.cube_c,self.cube_m = None,None,None,None

		self.lines_cube = None

		self.inventory = Inventory(self.batch,self.player)

	def load_reticle (self,x=None,y=None,m=10) :

		if not x : x = self.reticle_x
		if not y : y  = self.reticle_y

		self.reticle_x,self.reticle_y = x,y

		if self.reticle : self.reticle.delete(); self.reticle = None
		if self.player.pause : return
		self.reticle = self.batch.add(4,GL_LINES,None,('v2f',(x-m,y, x+m,y, x,y-m, x,y+m)),('c3f',(0,0,0, 0,0,0, 0,0,0, 0,0,0)))

	def load_cube (self,x=None,y=None,c=None,m=None) :

		if not x : x = self.cube_x
		if not y : y = self.cube_y
		if not c : c = self.cube_c
		if not m : m = self.cube_m

		self.cube_x,self.cube_y = x,y
		self.cube_c,self.cube_m = c,m

		if self.cube : 
			for face in self.cube : face.delete()
			self.cube = None
		if self.lines_cube : 
			for line in self.lines_cube : line.delete()
			self.lines_cube = None

		if not self.player.CREATIVE : return

		self.cube = cube2d(self.batch,x,y,c,m)

	def on_mouse_drag (self,x,y,dx,dy,button) :

		self.inventory.on_mouse_drag(x,y,dx,dy,button)

	def on_mouse_press (self,x,y,button) :

		self.inventory.on_mouse_press(x,y,button)

	def on_mouse_release (self,x,y,button) :

		self.inventory.on_mouse_release(x,y,button)

	def update (self) :

		self.load_reticle()
		self.load_cube(x=20,y=20,c=self.player.color_block_selec(),m=30)
		self.inventory.load()

	def draw (self) :

		self.update()
		self.batch.draw()
		self.inventory.draw()

class Window (pyglet.window.Window) :

	def set2d (self) : glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluOrtho2D(0,self.width,0,self.height)
	def set3d (self) : glLoadIdentity(); gluPerspective(65,self.width/self.height,0.1,320); glMatrixMode(GL_MODELVIEW); glLoadIdentity()
	def setLock (self,state) : self.set_exclusive_mouse(state); self.mouseLock = state
	mouseLock = False; mouse_lock = property(lambda self:self.mouseLock,setLock)

	def on_resize (self,w,h) :

		glViewport(0,0,w,h)
		self.graphics2d.load_reticle(w/2,h/2)
		self.graphics2d.inventory.load(w/2,h/2,w=3*w/4,h=3*h/4)

	def __init__ (self,Name='Player',*args,**kwargs) :

		super().__init__(*args,**kwargs)
		self.set_minimum_size(600,400)
		w,h = TamPantalla()
		self.set_location(int(w/2-self.width/2),int(h/2-self.height/2))
		pyglet.clock.schedule(self.update)
		self.keys = pyglet.window.key.KeyStateHandler()
		self.push_handlers(self.keys)
		self.keys_mouse = pyglet.window.mouse.MouseStateHandler()
		self.push_handlers(self.keys_mouse)
		self.model = Model("model")
		self.player = Script_Player(self.model.cubes.cubes,pos=(0,10,0),draw_player=False)
		self.player.Name = Name
		self.players = {}
		self.mouse_lock = True
		self.graphics2d = Graphics2D(self.player)
		self.server_ = server(self.model,self.player,self.players)
		self.client_ = client(self.model,self.player,self.players)

		self.players[self.player.Name] = self.player

	def add_player (self,Name) : self.players[Name] = Player(self.model.cubes.cubes); self.players[Name].Name = Name
	def delete_player (self,Name) : 
		if Name in self.players : del self.players[Name]
	def update_players (self) :
		aux = []
		for plr in self.cl.players :
			Name = plr[0]
			if Name == self.player.Name : continue
			if not Name in self.players : self.add_player(Name)
			self.players[Name].pos = plr[1]; self.players[Name].rot[1] = plr[2]
			aux.append(Name)
		aux2 = []
		for p in self.players :
			if not p in aux : aux2.append(p)
		for a in aux2 : self.delete_player(a)

	def update (self,dt) :

		self.player.update(dt,self.keys)
		self.model.update(dt)
		self.player.script_update()

	def on_text(self,text): 
      
		self.player.on_text(text)

	def on_mouse_motion (self,x,y,dx,dy) :

		if self.mouse_lock : self.player.mouse_motion(dx,dy)

	def on_mouse_drag (self,x,y,dx,dy,button,MOD) :

		self.graphics2d.on_mouse_drag(x,y,dx,dy,button)

	def on_mouse_press (self,x,y,button,MOD) :
		
		if not self.player.pause :
			if button == mouse.LEFT :
				block = self.model.cubes.hit_test(self.player.pos,self.player.get_sight_vector())[0]
				if block : self.model.cubes.remove(block)
			elif button == mouse.RIGHT :
				block = self.model.cubes.hit_test(self.player.pos,self.player.get_sight_vector())[1]
				if block : self.model.cubes.add(block,self.player.blocks[self.player.block_selected].c,self.player.blocks[self.player.block_selected].o,True)

		self.graphics2d.on_mouse_press(x,y,button)

	def on_mouse_release (self,x,y,button,MOD) :

		self.graphics2d.on_mouse_release(x,y,button)

	def on_key_press (self,KEY,MOD) :

		if KEY == key.ESCAPE : self.model.save_model("model"); self.dispatch_event('on_close')
		elif KEY == key.E : self.mouse_lock = not self.mouse_lock
		elif KEY == key.F : self.player.flying = not self.player.flying; self.player.dy = 0; self.player.noclip = True
		elif KEY == key.C : self.player.noclip = not self.player.noclip
		elif KEY == key.Q :
			if self.player.CREATIVE or self.player.inventory :
				if self.player.inventory : self.player.inventory = False; self.mouse_lock = True
				else : self.player.inventory = True; self.mouse_lock = False
		elif KEY == key.L : self.server_.start()
		elif KEY == key.O : self.client_.start()

	def on_draw (self) :

		self.clear()
		self.set3d()
		self.player.push()
		self.model.draw()
		for p in self.players :
			self.players[p].load()
			self.players[p].draw()

		block = self.model.cubes.hit_test(self.player.pos,self.player.get_sight_vector())[0]
		if block :
			glPolygonMode(GL_FRONT_AND_BACK,GL_LINE); glColor3d(0,0,0)
			pyglet.graphics.draw(24,GL_QUADS,('v3f/static',flatten(cube_vertices(block,0.52))))
			glPolygonMode(GL_FRONT_AND_BACK,GL_FILL); glColor3d(1,1,1)

		glPopMatrix()
		self.set2d()
		self.graphics2d.draw()


def main () :
	
	window = Window(width=800,height=600,caption='CUBOLAND',resizable=True)
	glClearColor(0.5,0.7,1,1)
	glEnable(GL_DEPTH_TEST); glDepthFunc(GL_LEQUAL); glAlphaFunc(GL_GEQUAL,1)
	glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
	pyglet.app.run()

if __name__ == "__main__" :
	main()