import numpy as np
import ivisit.matplotlib as ivml

# ***********************************************************************************
# Useful auxiliary functions 
# *************************************************************************
def getNearestNeighbor(X,x):
    """
    simple nearest neighbor search; returns index of nearest neighbor of x in X[1],X[2],...
    """
    dist = [np.linalg.norm(xi-x) for xi in X] # list of distances between x and X[i] 
    return np.argmin(dist)                    # return index idxNN of nearest neighbor X[idxNN] 

def computeGrid2D(f,xrange,yrange=None,f_mode='matrix'):
    """
    evaluate function f on 2D grid defined by xrange and yrange having format [min,max,delta]
    if f_mode is 'matrix' then f can process f(X,Y) for matrixes X,Y
    if f_mode is 'vector' then f can process f(X.flat,Y.flat) for matrixes X,Y
    if f_mode is 'scalar' then f can only process individual values f(x,y) for scalar values x,y
    returns X,Y,Z as matrixes each having the size of the grid
    """
    xmin,xmax,dx = xrange[0],xrange[1],xrange[2]
    if yrange is None: ymin,ymax,dy=xmin,xmax,dx
    else: ymin,ymax,dy = yrange[0],yrange[1],yrange[2]
    arange_x, arange_y = np.arange(xmin,xmax,dx), np.arange(ymin,ymax,dy)
    X,Y = np.meshgrid(arange_x, arange_y)
    if f_mode=='scalar':
        Z=np.array([[f([xj,yi]) for xj in arange_x] for yi in arange_y])
    elif f_mode=='vector':
        Z=f(X.flat,Y.flat)
        Z=Z.reshape(X.shape)
    elif f_mode=='matrix':
        Z=f(X,Y)
    return X,Y,Z

# ***********************************************************************************
# SimpleScope: a simple/fast oscilloscope-like class to display signals in x/y plots
#              independent of Matplotlib
# *************************************************************************
class SimpleScope:        # simple/fast oscilloscope-like class to display signals in x/y plots
    def __init__(self,im_width=100,im_height=100,min_x=0,max_x=100, min_y=0, max_y=100,
                 flagRGB=0, flag_line_x0=1, flag_line_y0=1,col_bkgr=0,col_frgr=255):
        self.configure(im_width,im_height,min_x,max_x,min_y,max_y,flagRGB,flag_line_x0,flag_line_y0,col_bkgr,col_frgr)

    def configure(self,im_width=None, im_height=None, min_x=None,max_x=None,min_y=None,max_y=None,
                  flagRGB=None,flag_line_x0=None,flag_line_y0=None,col_bkgr=None,col_frgr=None):
        # (i) set new parameters
        if not im_width     is None: self.im_width    =im_width
        if not im_height    is None: self.im_height   =im_height
        if not min_x        is None: self.min_x       =min_x
        if not max_x        is None: self.max_x       =max_x
        if not min_y        is None: self.min_y       =min_y
        if not max_y        is None: self.max_y       =max_y
        if not flagRGB      is None: self.flagRGB     =flagRGB
        if not flag_line_x0 is None: self.flag_line_x0=flag_line_x0
        if not flag_line_y0 is None: self.flag_line_y0=flag_line_y0
        if not col_bkgr     is None: self.col_bkgr    =col_bkgr
        if not col_frgr     is None: self.col_frgr    =col_frgr
        
        # (ii) allocate new image matrix im_data for data?
        if not im_width  is None or not im_height is None or not flagRGB is None:
            if self.flagRGB<=0: self.im_data=np.zeros((self.im_height,self.im_width)  ,'uint8') # gray image
            else              : self.im_data=np.zeros((self.im_height,self.im_width,3),'uint8') # RGB color image
            self.im_data[:,:]=self.col_bkgr    # initialize with background color

        # (iii) set transformation coefficients
        self.dx_inv_width  = self.im_width /(self.max_x-self.min_x)
        self.dy_inv_height = self.im_height/(self.max_y-self.min_y)
        self.i0=self.im_height-1-int((0-self.min_y)*self.dy_inv_height+0.5)%self.im_height # row index for y=0 line
        if self.flag_line_y0>0: self.im_data[self.i0,:]=self.col_frgr     # set y=0 line ?
        self.last_j,self.last_jp1=-1,0                                    # set dummy value for last_j (= last time position) and last_jp1 (=last x=0 line)

        return self.im_data   # return data image; assign this to ivisit data array

    def set_data(self,x,y_from,y_to=None,col=None,erase_x=1):  # draw at current time x point at x,y with color col (y,col may be lists)
        if col is None: col=self.col_frgr                           # default color is foreground
        j=int((x-self.min_x)*self.dx_inv_width+0.5)%self.im_width   # column/time index for data point
        jp1=(j+1)%self.im_width                                     # one column right of j (for new x=0 line)
        if erase_x>0 and j!=self.last_j: self.im_data[:,j]=self.col_bkgr  # erase column j ? (do not erase if j hasn't changed!)
        if self.flag_line_x0>0 and j!=self.last_j and j!=self.last_jp1: self.im_data[:,self.last_jp1]=self.col_bkgr  # erase old x=0 line if new j has leaped over 
        if self.flag_line_x0>0: self.im_data[:,jp1]=self.col_frgr   # draw line for x=0 ?
        if self.flag_line_y0>0: self.im_data[self.i0,j]=self.col_frgr     # restore y0=0 point
        if not isinstance(y_from,(list,tuple)): y_from,y_to,col=[y_from],[y_to],[col]  # cast y_from,y_to, and col as lists
        for ii in range(len(y_from)):
            i_from=self.im_height-1-int((y_from[ii]-self.min_y)*self.dy_inv_height+0.5)%self.im_height   # row index for data point
            if y_to is None: i_to=i_from
            else: i_to=self.im_height-1-int((y_to[ii]-self.min_y)*self.dy_inv_height+0.5)%self.im_height # row index for data point
            if i_from>i_to: i_to,i_from=i_from,i_to               # swap
            self.im_data[i_from:i_to+1,j]=col[ii]                 # set data point
        self.last_j=j                                             # keep last j (=last time position)
        self.last_jp1=jp1                                         # keep last j+1 (=position where the x=0 line has been drawn and should be deleted)


# *****************************************************************************************
# ClickDragEventAutomaton: Event handler automaton that can handle click and drag actions 
# *****************************************************************************************
class ClickDragEventAutomaton:
    def __init__(self, sim, var_action_name=None, handle_action=None, dict_action_type=None, button_no=1, flagMatplotlib=0):
        """
        :param sim: reference to IVISIT simulation object 
        :param var_action_name: name of the action variable defining the current action; must be attribute of self.sim.parameters
        :param handle_action: this function will be called to handle actions after click/drag events
                              handle_action should be a function of the simulation class (self.sim) and have the signature
                              def handle_action(self.sim,action,pos,pos_init   
        :param dict_action2type: dict defining for each action name (given by var_action_name) its type: either 'click' or 'drag' action
                                 example: dict_action2type={'New':'click', 'Delete':'click', 'Move':'drag'} defines that 
                                          actions "New" and "Delete" are click-actions (reuquire only one click), whereas
                                          action "Move" is a drag-action (requires initial-click, moving, releasing)
                                 if None or 'click' then all actions are interpreted as simple "click"-actions!
                                 if 'drag' then all actions are interpreted as drag actions!
        :param button_no: button number (either 1=left,2=middle,3=right button)
        :param flagMatplotlib: if >0 then click positions are transformed into Matplotlib coordinates (for clicking on Matplotlib figures!)
        """
        self.sim              = sim
        self.var_action_name  = var_action_name
        self.handle_action    = handle_action
        self.button_no        = str(button_no)
        self.dict_action_type = dict_action_type
        self.flagMatplotlib   = flagMatplotlib
        self.state            = 'IDLE'  # initialize state variable with IDLE (state can be either 'IDLE' or 'DRAG')
        self.pos, self.pos_init, self.pos_prev = None, None, None  # current, intial, and previous positions (of clicks or moves)
        self.action, self.action_type = None, None  # action (either "click", "drag_init", "drag_move", or "drag_finish") and action type (either "click" or "drag")

    def bind(self, display, img_var_name, img_widget_name, img_axis_name=None, img_widget_canvas_name="imgcanvas"):
        """
        :param display: display (usually a IVisitRawDisplay object) holding widgets to bind to
        :param img_var_name: name of the image matrix variable (typically a numpy array); must be attribute of self.sim.data
        :param img_widget_name: name of the IVISIT IMAGE widget where the the image is displayed (typically a TIVisitImageWidget)
        :param img_axis_name: name of the Matplotlib axis where the data points are drawn into (only for flagMatplotlib>0)
        :param img_widget_canvas_name: name of the canvas of the IVISIT IMAGE widget (default "imgcanvas" for TIVisitImageWidget) 
        """
        self.display                = display
        self.img_var_name           = img_var_name
        self.img_widget_name        = img_widget_name
        self.img_axis_name          = img_axis_name
        self.img_widget_canvas_name = img_widget_canvas_name
        if not display is None:
            display.bind2Widget(img_widget_name,"<Button-"+self.button_no+">"       ,self.onPressedButton ,img_widget_canvas_name)
            display.bind2Widget(img_widget_name,"<B"+self.button_no+"-Motion>"      ,self.onMovedButton   ,img_widget_canvas_name)
            display.bind2Widget(img_widget_name,"<ButtonRelease-"+self.button_no+">",self.onReleasedButton,img_widget_canvas_name)

    def getImgPos(self,event,flagCont=0,pad=1):
        """
        transform canvas positions event.x/y into image positions
        :param event: tkinter event with canvas positions event.x, event.y
        :param flagCont: if >0 then use continuous positions (e.g., to get Matplotlib positions)
        :param pad: tkinter canvas is usually larger than image matrix by pad in each direction (left, right, top, bottom)
        """
        canv = getattr(self.display.getWidget(self.img_widget_name),self.img_widget_canvas_name) # canvas of widget where mouse click ocurred
        canv_w,canv_h = canv.winfo_width()-2*pad, canv.winfo_height()-2*pad   # canvas size (without padding)
        img = getattr(self.sim.data,self.img_var_name)            # reference to image object
        x,y=max(0,(event.x-pad+0.5)*img.shape[1]/canv_w),max(0,(event.y-pad+0.5)*img.shape[0]/canv_h)  # continuous image position
        if flagCont<=0:          # discretize to image array indexes
            x,y=min(img.shape[1]-1,int(x)),min(img.shape[0]-1,int(y))
        return x,y
        
    def onPressedButton(self,event):  # called when clicking mouse button (button_no) on data widget
        if self.state=='IDLE':        # click on IMAGE only relevant in state IDLE
            self.sim.lock.acquire()   # make mouse processing thread-safe
            p,d=self.sim.parameters,self.sim.data # short hands to simulation parameters and data
            x,y=self.getImgPos(event,self.flagMatplotlib) # get image pixel position (note that canvas may be scaled compared to image)
            if self.flagMatplotlib>0: # get clicked position in Matplotlib coordinates?
                x,y=ivml.getDataPos_from_PixelPos(x,y,getattr(d,self.img_var_name).shape[0],getattr(self.sim,self.img_axis_name)) # Yes!
            self.pos=[x,y]            # store clicked position (in either image or Matplotlib coordinates)
            if self.dict_action_type is None: self.action_type="click"                       # per default action-type is click-action
            elif self.dict_action_type=='drag': self.action_type="drag"                      # drag action?
            else: self.action_type = self.dict_action_type[getattr(p,self.var_action_name)]  # get action-type from dict!
            if self.action_type=='click':
                self.action='click'        # if type is "click" then only action "click"
            elif self.action_type=='drag':                       
                self.action='drag_init'    # if type is "drag" then start drag sequence
                self.pos_init=[x,y]        # initial position 
                self.pos_prev=[x,y]        # previous position
                self.state='DRAG'          # change state to 'DRAG'
            else:
                assert 0, "unknown action_type="+str(self.action_type)+" (expected either 'click' or 'drag'!)"
            getattr(self.sim,self.handle_action)(self.action, self.pos, self.pos_init, self.pos_prev) # call to handle_action in simulation object
            self.sim.lock.release()   # release lock
        
    def onMovedButton(self,event):    # called when moved mouse while pressing button on data widget
        if self.state=='DRAG':        # moving mouse on IMAGE only relevant if in state DRAG
            self.sim.lock.acquire()   # make processing of mouse events thread-safe
            d=self.sim.data           # short hands to simulation parameters and data
            x,y=self.getImgPos(event,self.flagMatplotlib) # get image pixel position (note that canvas may be scaled compared to image)
            if self.flagMatplotlib>0: # get clicked position in Matplotlib coordinates?
                x,y=ivml.getDataPos_from_PixelPos(x,y,getattr(d,self.img_var_name).shape[0],getattr(self.sim,self.img_axis_name)) # Yes!
            self.pos_prev=self.pos    # previous position
            self.pos=[x,y]            # store clicked position
            self.action='drag_move'   # action 'drag_move' means the mouse has been moved to new position
            getattr(self.sim,self.handle_action)(self.action, self.pos, self.pos_init, self.pos_prev)  # call to handle_action in simulation object
            self.sim.lock.release()   # release lock
        
    def onReleasedButton(self,event): # called when releasing mouse button on data widget
        if self.state=='DRAG':        # releasing mouse on IMAGE only relevant if in state DRAG
            self.sim.lock.acquire()   # make processing of mouse events thread-safe
            self.action='drag_finish' # action 'drag_finish' means that mouse has been released and action should be finished
            getattr(self.sim,self.handle_action)(self.action, self.pos, self.pos_init, self.pos_prev) # call to handle_action in simulation object
            self.state='IDLE'         # change state back to 'IDLE'
            self.sim.lock.release()   # release lock
       
