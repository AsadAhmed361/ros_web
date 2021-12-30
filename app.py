from flask import Flask, render_template, url_for,g,jsonify,request, redirect
from sqlite3 import Error
import subprocess
import signal
import os
import time
import sqlite3
import json
import csv
from threading import Thread


active_map=" "
app = Flask(__name__)

class DataStore():
	navigation=False
	navigation_touchgoal=False
	mapping=False
	activeMap=None
	previousMap=None
	send_pose_name=None

def send_pose_th():
        
	os.system( "python3 "+os.path.expanduser('~')+"/catkin_ws/src/send_goal/src/scripts/send_corridor_pose.py -r "+new_data.send_pose_name)

def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE maps
              SET status = ? ,
                  statusTitle = ?

              WHERE name = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO maps(name,status,statusTitle)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def my_join(tpl):
    return ', '.join(x if isinstance(x, str) else my_join(x) for x in tpl)


def deactivateMap(name):
    try:
        mapname=name
        update_task(get_db(), ('warning', 'Inactive', mapname))
    except Error as e:
        print(e)
def activateMap(name):
    try:
        mapname=name
        update_task(get_db(), ('success', 'Activated', mapname))
        new_data.activeMap=name
    except Error as e:
        print(e)


class roslaunch_process():
    @classmethod
    def start_navigation_touchgoal(self,mapname):
        
        self.process_navigation_touchgoal = subprocess.Popen(["roslaunch","--wait", "turtlebot3_navigation", "turtlebot3_navigation_touchgoal.launch","map_file:="+os.getcwd()+"/static/"+mapname+".yaml"])
	
    @classmethod
    def start_navigation(self,mapname):
        
        self.process_navigation = subprocess.Popen(["roslaunch","--wait", "turtlebot3_navigation", "turtlebot3_navigation.launch","map_file:="+os.getcwd()+"/static/"+mapname+".yaml"])


    @classmethod
    def stop_navigation_touchgoal(self):
        self.process_navigation_touchgoal.send_signal(signal.SIGINT)	

    @classmethod
    def stop_navigation(self):
        self.process_navigation.send_signal(signal.SIGINT)	

    @classmethod
    def start_mapping(self):

        self.process_mapping = subprocess.Popen(["roslaunch", "--wait", "turtlebot3_slam", "turtlebot3_slam.launch"])

    @classmethod
    def stop_mapping(self):

        self.process_mapping.send_signal(signal.SIGINT)    


new_data=DataStore()

DATABASE = os.path.join(os.getcwd(), "static", "database.db")
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db





   
   


@app.before_first_request
def create_table():
	column ="name"
	goal="statusTitle"
	constrain="Activated"
    
	subprocess.Popen(["roslaunch", "turtlebot3_navigation", "turtlebot3_bringup.launch"])
	with app.app_context():
	    try:
	        c = get_db().cursor()
	        c.execute("CREATE TABLE IF NOT EXISTS maps (id integer PRIMARY KEY,name text NOT NULL, status text NOT NULL, statusTitle text NOT NULL)")
	        c.close()
	    except Error as e:
	        print(e)

	
	    try:
	        c = get_db().cursor()
	        c.execute("SELECT %s FROM maps where %s=?" % (column, goal), (constrain, ))
        	data = c.fetchall()
	        c.close()
	    except Error as e:
	        print(e)
	        
	    try:
	        mapname=my_join(data)
	        update_task(get_db(), ('warning', 'Inactive', mapname))
	    except Error as e:
	        print(e)
                
@app.route('/')
def index():
	
	with get_db():
	    try:
	        c = get_db().cursor()
	        c.execute("SELECT * FROM maps")
        	data = c.fetchall()
	        c.close()
	    except Error as e:
	        print(e)
	

	return render_template('index.html',map = data)

@app.route('/corridor_poses')
def corridor_poses():
	poses=[]
	for x in os.listdir(os.getcwd()+"/static/"):
	    if x.endswith(".json"):
	        posename=x[:x.index(".")]
	        _posename=posename.replace("_"," ")
	        poses.append(_posename)
	        
	        print(poses)
	

	return render_template('corridor_poses.html', poses=poses)

@app.route('/corridor_poses/deletepose')
def deletemap():
	#mapname = request.get_data().decode('utf-8')
	posename = request.args.get('posename')
	_posename=posename.replace(" ","_")
	os.system("rm -rf"+" "+os.getcwd()+"/static/"+_posename+".json")
	return redirect('/corridor_poses')

@app.route('/index/deletemap')
def deleteposes():
	#mapname = request.get_data().decode('utf-8')
	mapname = request.args.get('mapname')
	print(mapname)
	os.system("rm -rf"+" "+os.getcwd()+"/static/"+mapname+".yaml "+os.getcwd()+"/static/"+mapname+".png "+os.getcwd()+"/static/"+mapname+".pgm "+os.getcwd()+"/static/"+mapname+".csv")

	with get_db():
	    try:
	        c = get_db().cursor()
	        c.execute("DELETE FROM maps WHERE name=?", (mapname,))
	        c.close()
	    except Error as e:
	        print(e)

	with get_db():
	    try:
	        c = get_db().cursor()
	        c.execute("SELECT * FROM maps")
        	data = c.fetchall()
	        c.close()
	    except Error as e:
	        print(e)

	return redirect('/')	


@app.route('/index/start_nav')
def start_nav():
	
	mapname = request.args.get('mapname')
	
	

	

	with get_db():
	    try:
	        c = get_db().cursor()
	        c.execute("SELECT name FROM maps")
        	data = c.fetchall()
	        c.close()
	    except Error as e:
	        print(e)

	maps=data
	

	with get_db():
	    try:
	        c = get_db().cursor()
	        c.execute("SELECT * FROM maps")
        	data = c.fetchall()
	        c.close()
	    except Error as e:
	        print(e)

	

	with get_db():
		try:
			#print(maps)
			for map in maps:
				aMap=my_join(map)
				if(aMap==mapname):
					update_task(get_db(), ('success', 'Activated', mapname))
					new_data.activeMap=mapname
					new_data.previousMap=mapname
					try:
					    roslaunch_process.stop_mapping()
					    new_data.mapping=False
					    time.sleep(2)
					except:
					    pass

					if(new_data.navigation==True):
						roslaunch_process.stop_navigation()
						new_data.navigation=False
						time.sleep(2)

					if new_data.navigation_touchgoal==True:
					    new_data.navigation_touchgoal=False
					    roslaunch_process.stop_navigation_touchgoal()
					    time.sleep(2)
					    roslaunch_process.start_navigation_touchgoal(mapname)
					    new_data.navigation_touchgoal=True
					else:
					    roslaunch_process.start_navigation_touchgoal(mapname)
					    new_data.navigation_touchgoal=True
					#print(active_map)
				else:
				        update_task(get_db(), ('warning', 'inactive', aMap))
		except Error as e:
			print(e)
	
	with get_db():
	    try:
	        c = get_db().cursor()
	        c.execute("SELECT * FROM maps")
        	data = c.fetchall()
	        c.close()
	    except Error as e:
	        print(e)

	return redirect('/')	

@app.route("/navigation/stop" , methods=['POST'])
def stop():
	os.system("rostopic pub /move_base/cancel actionlib_msgs/GoalID -- {}") 
	return("stopped the robot")
	
@app.route('/mapping')
def mapping():
    if new_data.navigation==True:
        roslaunch_process.stop_navigation()
        new_data.navigation=False
        time.sleep(2)

    if new_data.navigation_touchgoal==True:
        roslaunch_process.stop_navigation_touchgoal()
        new_data.navigation_touchgoal=False
        time.sleep(2)

    if(new_data.mapping==True):
        roslaunch_process.stop_mapping()
        new_data.mapping=False
    
    roslaunch_process.start_mapping()
    new_data.mapping=True
	
    return render_template('mapping.html')	

@app.route('/corridor_mapping')
def corridor_mapping():
    if new_data.navigation==True:
        roslaunch_process.stop_navigation()
        new_data.navigation=False
        time.sleep(2)
		
    if new_data.navigation_touchgoal==True:
        roslaunch_process.stop_navigation_touchgoal()
        new_data.navigation_touchgoal=False
        time.sleep(2)

    if(new_data.mapping==True):
        roslaunch_process.stop_mapping()
        new_data.mapping=False
    
    roslaunch_process.start_mapping()
    new_data.mapping=True
	
    return render_template('corridor_mapping.html')	


@app.route("/mapping/savemap" , methods=['POST'])
def savemap():
	mapname_rec = request.get_data().decode('utf-8')
	x = mapname_rec.index("*")
	mapname=mapname_rec[:x]
	_mapname = mapname.replace(" ","_")
	initialpose = mapname_rec[x+2:]
	doc_pose=json.loads(initialpose)
	print(doc_pose["position"])
	pos_x=doc_pose["position"]["x"]
	pos_y=doc_pose["position"]["y"]
	orientation_z=doc_pose["orientation"]["z"]
	orientation_w=doc_pose["orientation"]["w"]
	Header=['frame_id','stamp','pos_x','pos_y','pos_z','orientation_x','orientation_y','orientation_z','orientation_w', 'covariance']
	Data=['map', '0', pos_x,pos_y, '0.0', '0.0', '0.0', orientation_z, orientation_w, "(0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942)"]
	path="/home/asad/ros_web/static/initialposes/"+_mapname+"_initialpose.csv"
	with open(path, 'w', encoding='UTF8') as f:
	    writer = csv.writer(f)
	    writer.writerow(Header)
	    writer.writerow(Data)
	    print(" updated")
	#print(mapname)
	with get_db():
		try:
			task_1 = (_mapname,'warning','Inactive')
			create_task(get_db(), task_1)
		except Error as e:
			print(e) 
	os.system("rosrun map_server map_saver -f"+" "+os.path.join(os.getcwd(),"static",_mapname))
	os.system("convert"+" "+os.getcwd()+"/static/"+_mapname+".pgm"+" "+os.getcwd()+"/static/"+_mapname+".png")
	new_data.mapping=False
	roslaunch_process.stop_mapping()
	if(new_data.activeMap != None):
	    new_data.navigation_touchgoal=True
	    roslaunch_process.start_navigation_touchgoal(new_data.activeMap)
	return("success")
	#return redirect(url_for("index"))
	#return render_template('index.html',map = data)



@app.route("/corridor_mapping/savemap" , methods=['POST'])
def corridor_savemap():
	mapname = request.get_data().decode('utf-8')
	#print(mapname)
	with get_db():
		try:
			task_1 = (mapname,'warning','Inactive')
			create_task(get_db(), task_1)
		except Error as e:
			print(e) 
	os.system("rosrun map_server map_saver -f"+" "+os.path.join(os.getcwd(),"static",mapname))
	os.system("convert"+" "+os.getcwd()+"/static/"+mapname+".pgm"+" "+os.getcwd()+"/static/"+mapname+".png")
	new_data.mapping=False
	roslaunch_process.stop_mapping()
	if(new_data.activeMap != None):
	    new_data.navigation_touchgoal=True
	    roslaunch_process.start_navigation_touchgoal(new_data.activeMap)
	return("success")
	#return redirect(url_for("index"))
	#return render_template('index.html',map = data)




@app.route("/navigation/savepose", methods=['POST'])
def save_pose():
	posename=request.get_data().decode('utf-8')
	#print(posename)
	x = posename.index("*")
	_posename=posename[:x].replace(" ","_")
	python_file = open(os.getcwd()+"/static/"+_posename+".json", "w")
	python_file.write(posename[x+2:])
	if _posename=="Docking_Station":
	    dp=posename[x+2:]
	    doc_pose=json.loads(dp)
	    print(doc_pose["position"])
	    pos_x=doc_pose["position"]["x"]
	    pos_y=doc_pose["position"]["y"]
	    orientation_z=doc_pose["orientation"]["z"]
	    orientation_w=doc_pose["orientation"]["w"]
	    Header=['frame_id','stamp','pos_x','pos_y','pos_z','orientation_x','orientation_y','orientation_z','orientation_w', 'covariance']
	    Data=['map', '0', pos_x,pos_y, '0.0', '0.0', '0.0', orientation_z, orientation_w, "(0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942)"]
	    path="/home/asad/ros_web/static/initialposes/corridor_map_initialpose.csv"
	    with open(path, 'w', encoding='UTF8') as f:
	        writer = csv.writer(f)
	        writer.writerow(Header)
	        writer.writerow(Data)
	        print(" updated")
		#python_file = open(os.getcwd()+"/static/pos.json", "w")
	    #python_file.write(str(doc_pose["position"]))
	return("success")


@app.route('/navigation')
def navigation():
	column ="name"
	goal="statusTitle"
	constrain="Activated"
	try:
		roslaunch_process.stop_mapping()
		time.sleep(2)
	except:
		pass

	if new_data.navigation==True:
		roslaunch_process.stop_navigation()
		new_data.navigation=False
		time.sleep(2)

	if new_data.navigation_touchgoal==False:
		new_data.navigation_touchgoal=True
		roslaunch_process.start_navigation_touchgoal(new_data.activeMap)    
	with get_db():
	    try:
	        c = get_db().cursor()
	        c.execute("SELECT %s FROM maps where %s=?" % (column, goal), (constrain, ))
        	data = c.fetchall()
	        c.close()
	    except Error as e:
	        print(e)
	#data = ["terrace"]
	if(new_data.activeMap != None):
	    return render_template('navigation.html', data=data[0])
	else:
		return render_template('na.html')	


#Operation application part
@app.route('/opindex')
def op_index():
	activateMap('corridor_map')
	if(new_data.previousMap != None):
	        deactivateMap(new_data.previousMap)

	if new_data.mapping==True:
		roslaunch_process.stop_mapping()
		new_data.mapping=False
		
	if new_data.navigation_touchgoal == True:
		roslaunch_process.stop_navigation_touchgoal()
		new_data.navigation_touchgoal=False

		roslaunch_process.start_navigation("corridor_map")
		new_data.navigation=True
	else:
		roslaunch_process.start_navigation("corridor_map")
		new_data.navigation=True
	return render_template('op_index.html')

@app.route('/selectpose')
def select_pose():
	
	poses=[]
	for x in os.listdir(os.getcwd()+"/static/"):
	    if x.endswith(".json"):
	        posename=x[:x.index(".")]
	        _posename=posename.replace("_"," ")
	        poses.append(_posename)
	        
	        #print(poses)
	

	return render_template('select_pose.html', poses=poses)

@app.route('/selectpose/sendpose')
def sendpose():
	
	posename = request.args.get('posename')
	_posename=posename.replace(" ","_")
	new_data.send_pose_name=_posename
	send_pose_thread = Thread(target=send_pose_th, )
	send_pose_thread.start()
	return render_template("nav_pose.html", posename=posename)

@app.route('/corridor_poses/sendpose',  methods=['POST'])
def sendposee():
	posename=request.get_data().decode('utf-8')
	_posename=posename.replace(" ","_")
	new_data.send_pose_name=_posename
	send_pose_thread = Thread(target=send_pose_th, )
	send_pose_thread.start()
	

	return ("success")

@app.route('/reached')
def reached():
	return redirect('/success')	

@app.route('/success')
def success():
	return render_template("new.html")	



if __name__ == '__main__':
	#app.run(debug=False)
	app.run(host='0.0.0.0', port=5000, debug=True, threaded=False)    
