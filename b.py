#importing 
from Tkinter import *
import os
import MySQLdb
import csv
import tkMessageBox
from tkFileDialog import askopenfilename

#global declarations
root = Tk()

file_path =''
#both are two entery from sql to excel
s=''
t=''
v = StringVar()
w= StringVar()
#entries from excel to sql
db=StringVar()
dbnew=StringVar()
dbn=''
d=''


#main transfer1
def transfer1():
	global file_path,d,dbn
	d=db.get()
	dbn=dbnew.get()
	print dbn,d
	
	#try:
		
			
	database = MySQLdb.connect (host="localhost", user = "root", passwd ="" , db = "phpgang")
	cursor = database.cursor()
		
			
		
	f=open(file_path,'r+')
	csv_data = csv.reader(f)
	ncol=len(next(csv_data))
	# Create table tablename (atrribute1,attribute2,attribute3) 
	#insert table tablename( attrbsd) values (actual values)
		#creating query
	create_query='CREATE TABLE '+dbn+' ('
	f.seek(0)
	j=0
	for row in csv_data:
		if(j==0):
			for k in range(ncol):
				create_query+=str(row[k])+ ' VARCHAR(50) NOT NULL'
				if(k!=ncol-1):
					create_query+=', '
			
			create_query+=')'
			j+=1
		else:
			
			break

	if(dbn!=""):
		d=dbn
			#with warnings.catch_warnings():
				#warnings.simplefilter('ignore')
				#cursor.execute('DROP TABLE IF EXISTS sdfdsfds')
			#cursor.execute("DROP TABLE IF EXISTS "+dbn.upper())
			
		cursor.execute(create_query)
			
			
			
	query1='INSERT INTO '+d+'('
	query2='VALUES('
	f.seek(0)
	i=0
		#inserting into sql
	for row in csv_data:
		if(i==0):
			for k in range(ncol):
				query1+=str(row[k])
				print str(row[k])
				query2+='%s'
				if(k!=ncol-1):
					query1+=','
					query2+=','
			
			query1+=')'
			query2+=')'
			i+=1
		else:
		#cursor.execute('INSERT INTO testcsv(names,classes, mark )VALUES("%s", "%s", "%s")', row)
			cursor.execute(query1+query2, row)
			#print query1+query2
			i+=1
#close the connection to the database.
		
	cursor.close()
		#print "Done"
	database.commit()

		# Close the database connection
	
	tkMessageBox.showinfo( "Sucessful", "Done")
	exit
	#except:
	#	e=sys.exc_info()[0]
		#e="Something went wrong"
	#	tkMessageBox.showinfo("Oh Shit!",e)'''
		
#main transfer2	
def transfer2():
	global s,t
	s+=v.get()
	t+=w.get()
	t=t+'.csv'
	#print s,t
	try:
		conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "",db = "phpgang")
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM "+str(s))
		num_fields = len(cursor.description)
		field_names = [i[0] for i in cursor.description]
		print num_fields,field_names,"hi"
		with open(t, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(field_names)
			while True:
				row = cursor.fetchone()	
				if row is None:
					break
				#elif row=="  ":
				#	continue
				else:
				
					writer.writerow(row)
		s=""
		t=""
		f.close()
		tkMessageBox.showinfo( "Successful", "Transfer Successful")
	except:
		e=sys.exc_info()[0]
		e=str(e)
		#e="Table Does Not Exist"
		tkMessageBox.showinfo("Unsuccessful",e)
		#pass
		
		
		

#on button 2	
def action2():
	#global s,t
	#v = StringVar()
	#w= StringVar()
	top2 = Toplevel()
	#top2 = Frame(frame, width=600, height=250)
	
	l = Label(top2, text="Table Name:")
	m = Label(top2, text="Excel file:")
	e1 = Entry(top2,textvariable=v)
	e2 = Entry(top2,textvariable=w)
	#s+=v.get()
	#t+=w.get()
	l.grid(row=0, sticky=E)
	m.grid(row=1, sticky=E)
	e1.grid(row=0, column=1)
	e2.grid(row=1, column=1)
	Button(top2, text="Transfer", command=transfer2).grid(row=2, column=1, sticky='ew', padx=8, pady=4)

		
#on button 1
def action1():
	top1=Toplevel()
	def open_file():
		global file_path
	
		
		filename = askopenfilename()
		#infile = open(filename, 'r+')
		#content = infile.read()
		file_path = os.path.abspath(filename)
		
		entry.delete(0, END)
		entry.insert(0, file_path)
		#infile.close()
		#return content
	f1 = Frame(top1, width=600, height=250)
	f1.pack(fill=X)
	f2 = Frame(top1, width=600, height=250)
	f2.pack()
	file_path = StringVar
	Label(f1,text="Select File:").grid(row=0, column=0, sticky='e')
	entry = Entry(f1, width=50, textvariable=file_path)
	entry.grid(row=0,column=1,padx=2,pady=2,sticky='we',columnspan=25)
	Button(f1, text="Browse", command=open_file).grid(row=0, column=27, sticky='ew', padx=8, pady=4)
	dbname = Label(f1, text="Table Name(if already exist):")
	dbname1 = Label(f1, text="Table Name(create new):")
	e = Entry(f1,width=50,textvariable=db)
	new = Entry(f1,width=50,textvariable=dbnew)
	Button(f1, text="Transfer", command=transfer1).grid(row=3, column=15, sticky='ew', padx=8, pady=4)
	dbname.grid(row=1, sticky=E)
	dbname1.grid(row=2, sticky=E)
	e.grid(row=1,column=1,padx=2,pady=2,sticky='we',columnspan=25)
	new.grid(row=2,column=1,padx=2,pady=2,sticky='we',columnspan=25)
	
	
#frames	
frame = Frame(root,height=800,width=800)
frame.pack()

button1 = Button(frame, text="EXCEL TO MYSQL",command = action1)
button1.pack()

button2 = Button(frame, text="MYSQL TO EXCEL",command = action2)
button2.pack( side = BOTTOM )


root.title('SQL-Bridge')
root.geometry("598x120+250+100")
root.mainloop()