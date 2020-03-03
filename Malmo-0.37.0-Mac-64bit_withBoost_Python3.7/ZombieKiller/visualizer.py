import tkinter as tk
from past.utils import old_div

class Visualizer:

    def __init__(self, arena_width=20, arena_breadth=20, canvas_border=20, canvas_width=400):
        
        self.arena_width = arena_width
        self.arena_breadth = arena_breadth

        self.canvas_border = canvas_border
        self.canvas_width = canvas_width
        self.canvas_height = canvas_border + ((self.canvas_width - self.canvas_border) 
                                             * self.arena_breadth / self.arena_width)

        self.canvas_scalex = old_div((self.canvas_width- self.canvas_border),self.arena_width)
        self.canvas_scaley = old_div((self.canvas_height- self.canvas_border),self.arena_breadth)
        self.canvas_orgx = old_div(-self.arena_width,self.canvas_scalex)
        self.canvas_orgy = old_div(-self.arena_breadth,self.canvas_scaley)

        self.mob_type = 'Zombie'

        self.root = tk.Tk()
        self.root.wm_title("Kill or dodge the " + self.mob_type + "s!")

        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, 
                      borderwidth=0, highlightthickness=0, bg="black")

        self.canvas.pack()
        self.root.update()
        #self.root = None
    """Draw tkinter window for statistic information"""
    # def drawStats(self, cur_scores=None,num_zombies=None,iteration=None):
    #     if self.root is None:
    #         self.root = tk.Tk()
    #         self.root.wm_title("Current Stats")
    #         self.root.update()
    #     if cur_scores != None and num_zombies != None and iteration != None:
    #         self.score_stats = tk.Label(self.root, text="Current Scores: %d" %cur_scores)
    #         self.zombie_stats = tk.Label(self.root, text="Zombie Remains: %d" % num_zombies)
    #         self.iteration = tk.Label(self.root,text="Iteration: %d" % iteration)
    #         self.iteration.grid(row=0,column=0)
    #         self.score_stats.grid(row=1,column=0)
    #         self.zombie_stats.grid(row=1,column=1)
    #     self.root.update()

    def canvasX(self, x):
        return (old_div(self.canvas_border,2)) + (0.5 + old_div(x,float(self.arena_width))) * (self.canvas_width-self.canvas_border)

    def canvasY(self, y):
        return (old_div(self.canvas_border,2)) + (0.5 + old_div(y,float(self.arena_breadth))) * (self.canvas_height-self.canvas_border)

    def drawMobs(self, entities, flash):
        self.canvas.delete("all")
        if flash:
            self.canvas.create_rectangle(0,0,self.canvas_width,self.canvas_height,fill="#ff0000") # Pain.
        self.canvas.create_rectangle(self.canvasX(old_div(-self.arena_width,2)), self.canvasY(old_div(-self.arena_breadth,2)), 
                                     self.canvasX(old_div(self.arena_width,2)), self.canvasY(old_div(self.arena_breadth,2)), 
                                     fill="#888888")
        for ent in entities:
            if ent["name"] == self.mob_type:
                print("zombie!!")
                print(f'x : {ent["x"]}')
                print(f'z : {ent["z"]}')
                print(f'x : {self.canvasX(ent["x"])}')
                print(f'z : {self.canvasY(ent["z"])}')
                self.canvas.create_oval(self.canvasX(ent["x"]-5), self.canvasY(ent["z"]-5), 
                                        self.canvasX(ent["x"]+5), self.canvasY(ent["z"]+5), 
                                        fill="#4422ff")
            elif ent["name"] == 'ZombieKiller':
                print("Myself!!")
                print(f'x : {ent["x"]}')
                print(f'z : {ent["z"]}')
                self.canvas.create_oval(self.canvasX(ent["x"]-5), self.canvasY(ent["z"]-5), 
                                        self.canvasX(ent["x"]+5), self.canvasY(ent["z"]+5),
                                        fill="#22ff44")
        self.root.update()