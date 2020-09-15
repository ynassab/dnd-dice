
# Version of the simulator with few or no gifs

# Required imports

from tkinter import Canvas, Frame, Button, Label, Tk, Toplevel, ttk
from PIL import Image, ImageTk, ImageSequence
from random import randint
from copy import copy



# Set up the dice GUI

diceRoot = Tk()

diceRoot.title("Dungeons & Dragons Dice Simulator with Gifs")

windowWidth = 900
windowHeight = 600
diceRoot.geometry("{}x{}".format(windowWidth, windowHeight))

# Create some frames for organization

leftFrame = Frame(diceRoot)
leftFrame.pack(side = "left", fill = "both")

middleFrame = Frame(diceRoot)
middleFrame.pack(side = "left", fill = "both")

rightFrame = Frame(diceRoot)
rightFrame.pack(side = "right", fill = "both", expand = True)


# Unbinds the spacebar from every button (creates a dummy button that doesn't appear on the root)
no_space_button = ttk.Button(diceRoot)
no_space_button.unbind_class("TButton", "<Key-space>")


# To close the app
def finished():
	global diceRoot
	diceRoot.destroy()
	diceRoot.quit()
	return

exit_button = ttk.Button(rightFrame, text = "Exit", command = finished)
exit_button.pack(side = "bottom", anchor = "e")

# Set up canvas for gif

gifCanvas = Canvas(rightFrame)
gifCanvas.pack(side = "top", anchor = "n", fill = "both", expand = True)


class Gif:
	def __init__(self, filepath, speed = 75):
        
		self.filepath = filepath # filepath for gif
		self.speed = speed # how fast the gif will play
		self.parent = diceRoot
        
		# Create a list of each frame in the gif
		self.true_image = Image.open(self.filepath)
		self.old_image_iteration = ImageSequence.Iterator(self.true_image)
        
		# Aspect ratio needed for appropriate size adjustment
		width, height = self.true_image.size
		self.im_aspect_ratio = height / width

		return
    
	def __call__(self, stillImage = None):
		
		self.stillImage = stillImage
		
		# Clear the canvas of the old image
		gifCanvas.delete("all")
		
		# To be populated when frames are resized:
		new_image_iteration = []
		
		# Find the current aspect ratio of the canvas (based on user's window adjustment)
		width, height = gifCanvas.winfo_width(), gifCanvas.winfo_height()
		canv_aspect_ratio = height / width
		
		# Matching height or width of image to canvas dimensions depends on difference in their aspect ratios
		if canv_aspect_ratio > self.im_aspect_ratio:
			# Match image and canvas width
			image_dimensions = ( width, round( width * self.im_aspect_ratio ) )
		else:
			# Match image and canvas height
			image_dimensions = ( round( height / self.im_aspect_ratio ), height )
		
		# Prevents the old iteration from being altered
		iteration_copy = copy(self.old_image_iteration)

		# Resize the frames to fit the canvas
		for frame in iteration_copy:
			frame = frame.resize(image_dimensions, Image.ANTIALIAS)
			new_image_iteration.append(frame)
		
		# Create a new sequence with the resized frames
		self.sequence = [ImageTk.PhotoImage(frame) for frame in new_image_iteration]
		
		# Add the new image to the canvas
		self.image = gifCanvas.create_image(0, 0, image = self.sequence[0], anchor = "nw")
		
		self.animate(1)
		
		return
	
	# Loops through the sequence of images until the gif runs completely once, then destroys it
	def animate(self, counter):
		
		# Displays the frame in the gif
		gifCanvas.itemconfig(self.image, image = self.sequence[counter])
		
		if counter < (len(self.sequence) - 1):
			# Calls animate( counter + 1 ) in "self.speed" milliseconds intervals recursively
			self.parent.after(self.speed, self.animate, counter + 1 )
		
		elif counter == (len(self.sequence) - 1):
			# Clear the canvas of the old image
			gifCanvas.delete("all")
			# Shows the still image
			if self.stillImage != None:
				self.stillImage()
		
		return

	
# Initiates respective gif when called (gifs are initiated in alphabetical order)

batmanFacepalm =			Gif(r'gifs\batman_facepalm.gif')
drakeDancing = 				Gif(r'gifs\drake_dancing.gif', speed = 100)
interestingManClap =		Gif(r'gifs\interesting_man_clap.gif')
kevinHeartBlink =			Gif(r'gifs\kevin_heart_blink.gif', speed = 100)
ohNoPanda = 				Gif(r'gifs\oh_no_panda.gif')
shaqShimmy =				Gif(r'gifs\shaq_shimmy.gif', speed = 25)
simonCowellFacepalm =		Gif(r'gifs\simon_cowell_facepalm.gif')
tonyStarkExplosion =		Gif(r'gifs\tony_stark_explosion.gif')
vinDieselCritical =			Gif(r'gifs\vin_diesel_critical.gif')

    
class StillImage:
	def __init__(self, filepath):
		
		self.true_image = Image.open(filepath)
		
		width, height = self.true_image.size
		self.im_aspect_ratio = height / width

		return
	
	def __call__(self):
		
		# Find the current aspect ratio of the canvas (based on user's window adjustment)
		width, height = gifCanvas.winfo_width(), gifCanvas.winfo_height()
		canv_aspect_ratio = height / width
		
		# Matching height or width of image to canvas dimensions depends on difference in their aspect ratios
		if canv_aspect_ratio > self.im_aspect_ratio:
			# Match image and canvas width
			image_dimensions = ( width, round( width * self.im_aspect_ratio ) )
		else:
			# Match image and canvas height
			image_dimensions = ( round( height / self.im_aspect_ratio ), height )
		
		resize_image = self.true_image.resize(image_dimensions, Image.ANTIALIAS)
		self.photoImage = ImageTk.PhotoImage(resize_image)
		
		image = gifCanvas.create_image(0, 0, anchor = "nw", image = self.photoImage)
		
		return


# Functionality for each die

class Die:
	# You can add *args here for special gifs
	def __init__(self, die_size, name):
		
		self.die_size = die_size
		self.name = name
		self.running_total = 0
		self.count = [i+1 for i in range(die_size)] # Create a list from "1" to "size"

		return
	
	def __call__(self): 
		
		result = randint(1, self.die_size)
		
		# Update running total (except for d20)
		if self.name == "D20":
			totalLabel["text"] = "Rolling d20's"
		elif self.name in totalLabel['text']:
			self.running_total = self.running_total + result
			totalLabel['text'] = self.name + " Total: " + str(self.running_total)
		# Reset the running total if this die was not that last one rolled
		else:
			self.running_total = result
			totalLabel['text'] = self.name + " Total: " + str(self.running_total)
		
		# Reset the log if a new die is rolled
		if self.name not in logLabel['text'] and logLabel['text'] != "Log:":
			logLabel['text'] = "Log:"
		# Then update the log
		logLabel['text'] += " \n" + self.name + " result: " + str(result)
		
		# Play special gifs
		if self.die_size == 20 and result == 20:
			chosen_gif = randint(1, 5)
			if chosen_gif == 1:
				vinDieselCritical()
			elif chosen_gif == 2:
				tonyStarkExplosion()
			elif chosen_gif == 3:
				interestingManClap()
			elif chosen_gif == 4:
				drakeDancing()
			elif chosen_gif == 5:
				shaqShimmy()
		elif self.die_size == 20 and result == 1:
			chosen_gif = randint(1, 4)
			if chosen_gif == 1:
				kevinHeartBlink()
			elif chosen_gif == 2:
				simonCowellFacepalm()
			elif chosen_gif == 3:
				batmanFacepalm()
			elif chosen_gif == 4:
				ohNoPanda()
		
		return

# Initiate each die

d4 = Die(4, "D4")
d6 = Die(6, "D6")
d8 = Die(8, "D8")
d10 = Die(10, "D10")
d12 = Die(12, "D12")
d20 = Die(20, "D20")

# Create GUI buttons for each die

for die in [ ["D4", d4],
			["D6", d6],
			["D8", d8],
			["D10", d10],
			["D12", d12],
			["D20", d20]]:
				button = ttk.Button(leftFrame, text = die[0], command = die[1])
				button.pack(side = "top", anchor = "w")


# Bind keyboard letters to each die

# "Helper function" that makes keys bind properly 
def make_lambda(command):
	return lambda event: command()

for pair in [[ "a" , "A", d4 ],
			[ "s" , "S", d6 ],
			[ "d" , "D", d8 ],
			[ "f" , "F", d10 ],
			[ "g" , "G", d12 ],
			[ "h" , "H", d20 ]]:
				
				# Bind lowercase letters
				diceRoot.bind( pair[0], make_lambda(pair[2]) )
				# Bind capital letters (in case caps lock is on)
				diceRoot.bind( pair[1], make_lambda(pair[2]) )

# Button to reset the log
def resetLog():
	logLabel["text"] = "Log:"
	totalLabel["text"] = "Total:"
	return
resetLogButton = ttk.Button(leftFrame, text = "Reset Log", command = resetLog)
resetLogButton.pack(side = "top", anchor = "w")

# Bind escape key to reset log
diceRoot.bind("<Escape>", lambda event: resetLog())

# Running total for die of one type rolled
totalLabel = Label(middleFrame, text = "Total:", fg = "red", font = "Times 22")
totalLabel.pack(side = "top", anchor = "w")

# A log of the previous outputs
# Note: log text happily travels off the window when large
logLabel = Label(middleFrame, text = "Log:", font = "Times 16")
logLabel.pack(side = "top", anchor = "w")

# Keeps the GUI open until the user closes it
diceRoot.mainloop()